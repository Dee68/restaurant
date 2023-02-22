from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
# from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from .forms import RegisterForm, UserProfileForm
import json


# Create your views here.


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        field_vals = request.POST
        username = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        passw1 = request.POST['password1']
        passw2 = request.POST['password2']
        context = {'field_vals': field_vals, 'reg_form': reg_form}
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken,choose another.')
        elif len(username) < 2 or len(username) > 8:
            messages.error(request, 'username must be between 2 and 8 characters')
        elif len(fname) == 0 or len(lname) == 0 or len(username) == 0:
            messages.error(request, 'All fields are required.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken, choose another.')
        elif not username.isalnum() or not fname.isalnum() or not lname.isalnum():
            messages.error(request, 'Only alpha-numeric characters allowed.')
        elif passw1 != passw2:
            messages.error(request, 'Passwords do not match.')
        if reg_form.is_valid():
            user = User.objects.create_user(username=username, email=email, first_name=fname, last_name=lname,password=passw1)
            user.set_password(passw1)
            user.save()
            messages.success(request, 'Account successfully created. you can now log in.')
            return redirect('meal:home')

        return render(request, 'account/register.html', context)
    return render(request, 'account/register.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, mark_safe('Welcome ' + user.username))
                return redirect('meal:home')
            else:
                messages.error(request, 'Invalid credentials,try again.')
                return render(request, 'account/signin.html')
        else:
            messages.error(request, 'All fields are required.')
            return render(request, 'account/signin.html')
    return render(request, 'account/login.html')


def logout_page(request):
    logout(request)
    return redirect('meal:home')


def validate_username(request):
    data = json.loads(request.body)
    err_str = 'Username should contain only alphanumeric characters.'
    err_str1 = 'Username must be between 2 and 8 characters.'
    err_str2 = 'Sorry username already in use, choose another.'
    username = data['username']
    if not str(username).isalnum():
        return JsonResponse({'username_error': err_str}, status=400)
    if len(data['username']) <= 1 or len(data['username']) >= 9:
        return JsonResponse({'username_error': err_str1}, status=406)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'username_error': err_str2}, status=409)
    return JsonResponse({'username_valid': True}, status=200)


def validate_email(request):
    data = json.loads(request.body)
    err_str = 'Sorry,email already taken, choose another one'
    err_str1 = 'Email is invalid.'
    email = data['email']
    if User.objects.filter(email=email):
        return JsonResponse({'email_error': err_str}, status=409)
    if not validate_email(email):
        return JsonResponse({'email_error': err_str1}, status=400)
    else:
        return JsonResponse({'email_valid': True}, status=200)
    # try:
    #     validate_email(email)
    #     return JsonResponse({'email_valid': True}, status=200)
    # except ValidationError:
    #     return JsonResponse({'email_error': 'Email is invalid'}, status=400)


@login_required(login_url='account/signin')
def update_profile(request):
    current_user = request.user
    userprofile = Profile.objects.get(user_id=current_user.id)
    profile_form = UserProfileForm(instance=request.user.profile)
    context = {'profile_form': profile_form }
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('meal:home')
        else:
            pass
    return render(request, 'account/update_profile.html', context)