from django.db import models


# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=30)
    
class tbl_category(models.Model):
    category_name=models.CharField(max_length=30)

class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=30)
    admin_email=models.CharField(max_length=30)
    admin_password=models.CharField(max_length=10)

class tbl_place(models.Model):
    place_name=models.CharField(max_length=30)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_subcategory(models.Model):
    sub_name=models.CharField(max_length=30)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)

class tbl_insurance(models.Model):
    insurance_name=models.CharField(max_length=30)
    insurance_details=models.CharField(max_length=10)
    insurance_amount=models.CharField(max_length=30)
    insurance_file=models.FileField(upload_to='Assets/file/User')
    insurance_status=models.IntegerField(default=0)

class tbl_machine(models.Model):
    machine_name=models.CharField( max_length=30)
    machine_details=models.CharField(max_length=200)
    machine_photo=models.FileField(upload_to='Assets/file/User')
    machine_price=models.CharField(max_length=30)





    