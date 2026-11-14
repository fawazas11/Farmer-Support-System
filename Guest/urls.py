from django.urls import path,include 
from Guest import views
app_name='Guest'

urlpatterns = [
    path('Signup/',views.Signup,name='Signup'),
    path('ajaxplace/',views.ajaxplace,name='ajaxplace'),
    path('Login/',views.Login,name='Login'),
    path('FarmerRegistration/',views.FarmerRegistration,name='FarmerRegistration'),
    path('Officer/',views.Officer,name='Officer'),
    path('',views.index,name='index')

  ]