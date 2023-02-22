from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

# Create your models here.


class Meal(models.Model):
    CATEGORY = (
        ('breakfast', 'breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, upload_to='meals/')
    category = models.CharField(max_length=9, choices=CATEGORY)
    slug = models.SlugField(max_length=200)
    number_of_persons = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def image_tag(self):
        if self.image:
            img_html = '<img src="%s" height="50" width="50">'
            return mark_safe(img_html %self.image.url)
        return "No image found"
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name


class RestaurantTable(models.Model):
    Table_TYPE = (
        ('single', 'single'),
        ('double', 'double'),
        ('group', 'group'),
    )
    number = models.IntegerField()
    table_type = models.CharField(max_length=6, choices=Table_TYPE)
    seats = models.IntegerField()
    is_available = models.BooleanField(default=True)
    capacity = models.IntegerField(default=1)

    def __str__(self):
        return str(f'{self.number} {self.table_type} table with {self.capacity} capacity.')


class Reservation(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    reserv_stime = models.DateTimeField()
    reserve_etime = models.DateTimeField()

    def __str__(self):
        return str(f'{self.customer} booked {self.table.number} for {self.reserv_date} by {self.reserv_stime}')