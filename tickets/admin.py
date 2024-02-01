from django.contrib import admin
from .models import Movie , Guest , Reservation
# Register your models here.

admin.site.register(Movie)
admin.site.register(Guest)
admin.site.register(Reservation)