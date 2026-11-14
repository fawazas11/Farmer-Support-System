from django.urls import path
from Officer import views
app_name='Officer'

urlpatterns = [
    path('HomePage/',views.HomePage,name='HomePage'),
    path('Myprofile/',views.Myprofile,name='Myprofile'),
    path('Changepassword/',views.Changepassword,name='Changepassword'),
    path('Editprofile/',views.Editprofile,name='Editprofile'),
    path('Notifications/',views.Notifications,name='Notifications'),
    path('Delnot/<int:did>',views.Delnot,name='Delnot'),
    path('Addproduct/',views.Addproduct,name='Addproduct'),
    path('ViewBooking/',views.ViewBooking,name='ViewBooking'),
    path('collect/<int:bid>',views.collect,name='collect'),
    path('ViewRequest/',views.ViewRequest,name='ViewRequest'),
    path('Accept/<int:aid>',views.Accept,name='Accept'),
    path('Reject/<int:rid>',views.Reject,name='Reject'),
    path('ViewMachineBooking/',views.ViewMachineBooking,name='ViewMachineBooking'),
    path('Aler/<int:nid>',views.Alert,name='Alert'),
    path('ClaimRequest/',views.ClaimRequest,name='ClaimRequest'),
    path('logout/',views.logout,name='logout'),
    path('AcceptClaim/<int:acid>',views.AcceptClaim,name='AcceptClaim'),
    path('RejectClaim/<int:reid>',views.RejectClaim,name='RejectClaim'),
   

  ]