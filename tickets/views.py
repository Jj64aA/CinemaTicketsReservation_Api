#-------- Django -----------------------------
from django.shortcuts import render
from django.http.response import JsonResponse 

#--------- APP -------------------------------
from .models import Movie , Guest , Reservation 
from .serializers import GuestSerializer , ReservationSerializer , MovieSerializer
#--------- REST ------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#---------------------------------------------


def test(request) : 
   data  = Guest.objects.all()
   response = {
      "Guests" : list(data.values())
   }
       
   return JsonResponse(response , safe= False)

''' using Function based view '''

@api_view(['GET','POST'])
def FBV_list(request):
   if request.method == 'GET' : 
      guests = Guest.objects.all()
      serializer  = GuestSerializer(guests , many  = True)
      return Response(serializer.data)

   if request.method == 'POST' : 
      serializer  = GuestSerializer(data = request.data) 
      if serializer.is_valid()  :
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)