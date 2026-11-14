from django.db import models
from Guest.models import*
from Farmer.models import*
# Create your models here.

class tbl_notification(models.Model):
    notification_title=models.CharField(max_length=30)
    notification_details=models.CharField(max_length=250)
    notification_date=models.DateField(auto_now_add=True)
    notification_status=models.IntegerField(default=0)
    officer=models.ForeignKey(tbl_officer,on_delete=models.CASCADE)

class tbl_product(models.Model):
    product_name=models.CharField(max_length=20)
    product_details=models.CharField(max_length=200)
    product_photo=models.FileField(upload_to='Assets/file/User')
    product_price=models.CharField(max_length=30)
    product_status=models.IntegerField(default=0)
    officer=models.ForeignKey(tbl_officer,on_delete=models.CASCADE)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)




