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
from rest_framework.views import APIView
from rest_framework import generics , mixins , viewsets ,filters
from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import BasePermission
#---------------------------------------------


def list_url(request) : 
   listUrl = [
      "all-guests/", 
      "pk-guests/<str:pk>/",
      "all-guests-cbv/",
      "pk-guests-cbv/<str:pk>/",
      "all-guests-mixins/" ,
      "pk-guests-mixins/<str:pk>/",
      "all-guests-generics/",
      "pk-guests-generics/<str:pk>/",
      "viewsets/"

   ]
   return JsonResponse(listUrl , safe=False)

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


@api_view(['DELETE','PUT','GET']) 
def FBV_pk(request, pk) : 
   try :
      guest = Guest.objects.get(id = pk )

   except Guest.DoesNotExist : 
      return Response({"msg" : "error exists !"})

   if request.method == "GET" : 
      serializer  =  GuestSerializer(guest , many  = False)
      return Response(serializer.data)


   if request.method == "PUT" : 
      serializer  =  GuestSerializer(guest , data = request.data)
      if serializer.is_valid() : 
         serializer.save()
         return Response(serializer.data)
      return Response({"msg" : "An update operation was not successful !"})

   if request.method == "DELETE" : 
      guest.delete()
      return Response({"msg" : "Deletion operation completed successfully !"})
   

''' using Class based view '''

class CBV_list(APIView):
   
   def get(self , request) : 
      guests = Guest.objects.all()
      serializer = GuestSerializer(guests , many = True)
      return Response(serializer.data)

   def post(self , request) : 
      serializer = GuestSerializer(data= request.data)
      if serializer.is_valid() : 
         serializer.save()
         return Response({"msg" :"The creation process was successfully completed ! "} , status=status.HTTP_201_CREATED)
      return Response({"msg" : "There's a mistake in creating !"} , status=status.HTTP_400_BAD_REQUEST)
   
class CBV_pk(APIView):
  
   def get(self , request , pk , format=None) : 
      try :
          guest = Guest.objects.get(id = pk )
      except Guest.DoesNotExist : 
          return Response({"msg" : "error exists !"})
      
      serializer = GuestSerializer(guest , many = False)
      return Response(serializer.data)
   
   def delete(self , request , pk , format=None) : 
      try :
          guest = Guest.objects.get(id = pk )
      except Guest.DoesNotExist : 
          return Response({"msg" : "error exists !"})
      
      guest.delete()
      return Response({"msg" :"Deletion operation completed successfully !"})
   
   def put(self , request , pk , format=None) : 
      try :
          guest = Guest.objects.get(id = pk )
      except Guest.DoesNotExist : 
          return Response({"msg" : "error exists !"})
      serializer  =  GuestSerializer(guest , data = request.data)
      if serializer.is_valid() : 
         serializer.save()
         return Response(serializer.data)
      return Response({"msg" : "An update operation was not successful !"})


''' using Mixins '''     

class MIXINS_list(mixins.ListModelMixin , mixins.CreateModelMixin , generics.GenericAPIView) : 
   
   queryset = Guest.objects.all()
   serializer_class = GuestSerializer

   def get(self , request) : 
      return self.list(request)
   def post(self , request) : 
      return self.create(request)
   
class MIXINS_pk(mixins.RetrieveModelMixin , mixins.UpdateModelMixin, mixins.DestroyModelMixin , generics.GenericAPIView) : 
   
   queryset = Guest.objects.all()
   serializer_class = GuestSerializer   

   def get(self , request , pk) : 
      return self.retrieve(request ,pk)
   
   def put(self , request , pk) : 
      return self.update(request ,pk)   
   
   def delete(self , request , pk) : 
      return self.destroy(request,pk)   
   
''' using Generics '''   

class Generics_list(generics.ListCreateAPIView) :
   queryset = Guest.objects.all()
   serializer_class = GuestSerializer
   authentication_classes = [BasicAuthentication]
   pagination_class = [BasePermission]

class Generics_pk(generics.RetrieveUpdateDestroyAPIView) :
   queryset = Guest.objects.all()
   serializer_class = GuestSerializer

''' using viewsets '''     
class viewsets_guests(viewsets.ModelViewSet) : 
   queryset = Guest.objects.all()
   serializer_class = GuestSerializer   


class viewsets_movies(viewsets.ModelViewSet) : 
   queryset = Movie.objects.all()
   serializer_class = MovieSerializer
   filter_backends = [filters.SearchFilter]
   search_fields = ["movie"]

class viewsets_reservation(viewsets.ModelViewSet) : 
   queryset = Reservation.objects.all()
   serializer_class = ReservationSerializer

''' main '''    

@api_view(['GET'])
def find_movie(request) : 
   movies = Movie.objects.filter(
      hall = request.data['hall'] , 
      movie = request.data['movie']
   )
   serializer = MovieSerializer(movies , many = True )
   return Response(serializer.data)

@api_view(['POST'])
def new_reservation(request) :
   #movie = request.data['movie']
   #guest = request.data['guest']
   
   movie = Movie.objects.get(
      hall= request.data['hall'] , 
      movie = request.data['movie']
   )
   guest = Guest()
   guest.name = request.data['name']
   guest.mobile = request.data['mobile']
   guest.save()

   reservation = Reservation()
   reservation.guest = guest 
   reservation.movie = movie
   reservation.save()

   return Response({"msg" : "operation successful !"})
