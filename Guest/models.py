from django.db import models
from Admin.models import*

class tbl_user(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=25)
    user_password=models.CharField(max_length=30)
    user_contact=models.CharField(max_length=30)
    user_address=models.CharField(max_length=100)
    user_gender=models.CharField(max_length=30)
    user_dob=models.DateField()
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_status=models.IntegerField(default=0)
    user_photo=models.FileField(upload_to="Assets/File/User")

class tbl_farmer(models.Model):
    farmer_id=models.CharField(max_length=30)
    farmer_name=models.CharField(max_length=30)
    farmer_email=models.CharField(max_length=30)
    farmer_contact=models.CharField(max_length=30)
    farmer_address=models.CharField(max_length=30)
    farmer_photo=models.FileField(upload_to="Assets/File/User")
    farmer_proof=models.FileField(upload_to="Assets/File/User")
    farmer_password=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    farmer_status=models.IntegerField(default=0)
    farmer_bank=models.CharField(max_length=50, null=True)
    farmer_account=models.CharField(max_length=20, null=True)
    farmer_ifsc=models.CharField(max_length=15, null=True)

class tbl_officer(models.Model):
    officer_name=models.CharField(max_length=30)
    officer_email=models.CharField(max_length=30)
    officer_contact=models.CharField(max_length=30)
    officer_address=models.CharField(max_length=30)
    officer_photo=models.FileField(upload_to="Assets/Flile/User")
    officer_proof=models.FileField(upload_to="Assets/File/User")
    officer_password=models.CharField(max_length=30) 
    officer_status=models.IntegerField(default=0)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)

