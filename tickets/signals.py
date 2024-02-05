#-------- Django -----------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.conf import settings
from django.contrib.auth.models import User
#--------- REST ------------------------------
from rest_framework.authtoken.models import Token



# @receiver(post_save , sender = User)
# def TokenCreate(sender ,instance ,created,  **kwargs) : 
#    if created : 
#       Token.objects.create( user = instance)