
#-------- Django -----------------------------
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.conf import settings
from django.contrib.auth.models import User
#--------- REST ------------------------------
from rest_framework.authtoken.models import Token
# Create your models here.


class Movie(models.Model) : 
   hall = models.CharField(max_length = 10)
   movie = models.CharField(max_length = 30)
   date = models.DateField()
   def __str__(self) : 
      return self.movie
class Guest(models.Model) : 
   name = models.CharField(max_length = 30)
   mobile = models.CharField(max_length = 15)
   def __str__(self) : 
      return self.name
class Reservation(models.Model):
   
   guest = models.ForeignKey(Guest , related_name = "reservation" , on_delete = models.CASCADE)
   movie = models.ForeignKey(Movie , related_name = "reservation" , on_delete = models.CASCADE)
   def __str__(self) : 
      return f"{self.guest.name}//{self.movie.movie}"
   

@receiver(post_save , sender = User)
def TokenCreate(sender ,instance ,created,  **kwargs) : 
   if created : 
      Token.objects.create( user = instance)   