from django.urls import path , include
from . import views
#---------------Rest---------------
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('guests',views.viewsets_guests)
router.register('movies',views.viewsets_movies)
router.register('reservation',views.viewsets_reservation)

urlpatterns = [
   path('urls/',views.list_url),
   path('testjson/',views.test),
   path('all-guests/',views.FBV_list),
   path('pk-guests/<str:pk>/',views.FBV_pk),
   path('all-guests-cbv/',views.CBV_list.as_view()),
   path('pk-guests-cbv/<str:pk>/',views.CBV_pk.as_view()),
   path('all-guests-mixins/',views.MIXINS_list.as_view()),
   path('pk-guests-mixins/<str:pk>/',views.MIXINS_pk.as_view()),
   path('all-guests-generics/',views.Generics_list.as_view()),
   path('pk-guests-generics/<str:pk>/',views.Generics_pk.as_view()),
   path('viewsets/', include(router.urls)),
   path('find-movie/', views.find_movie),
   path('new-reservation/', views.new_reservation) , 
   path('api-auth', include('rest_framework.urls')), 
   path('api-auth-token/' , obtain_auth_token) , 
   path('post_pk/<str:pk>/', views.Post_pk.as_view())
]
