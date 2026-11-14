from django.db import models
from Guest.models import*
from Officer.models import*
from Admin.models import*
# Create your models here.
class tbl_booking(models.Model):
    booking_date=models.DateField(auto_now_add=True)
    booking_amount=models.CharField(max_length=20)
    booking_status=models.IntegerField(default=0)
    farmer=models.ForeignKey(tbl_farmer,on_delete=models.CASCADE,null=True)
    officer=models.ForeignKey(tbl_officer,on_delete=models.CASCADE,null=True)

class tbl_cart(models.Model):
    cart_quantity=models.IntegerField(default=1)
    cart_status=models.IntegerField(default=0)
    booking=models.ForeignKey(tbl_booking,on_delete=models.CASCADE)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)

class tbl_request(models.Model):
    request_file=models.FileField(upload_to='Assets/file/User')
    request_amount=models.CharField(max_length=30)
    claim_amount=models.CharField(max_length=100,null=True)
    request_details=models.CharField(max_length=30)
    request_date=models.DateField(auto_now_add=True)
    request_status=models.IntegerField(default=0)
    farmer=models.ForeignKey(tbl_farmer,on_delete=models.CASCADE,null=True)
    officer=models.ForeignKey(tbl_officer,on_delete=models.CASCADE,null=True)
    insurance=models.ForeignKey(tbl_insurance,on_delete=models.CASCADE,null=True)

class tbl_machinebooking(models.Model):
    bookingmachine_date=models.DateField(auto_now_add=True)
    bookingmachine_amount=models.CharField(max_length=20,null=True)
    bookingmachine_status=models.IntegerField(default=1)
    farmer=models.ForeignKey(tbl_farmer,on_delete=models.CASCADE,null=True)
    machine=models.ForeignKey(tbl_machine,on_delete=models.CASCADE,null=True)

class tbl_claim(models.Model):
    claim_name=models.CharField(max_length=30)
    claim_details=models.CharField(max_length=30)
    claim_amount=models.CharField(max_length=30)
    claim_file=models.FileField(upload_to='Assests/file/User')
    claim_status=models.IntegerField(default=0)
    request=models.ForeignKey(tbl_request,on_delete=models.CASCADE)

class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=30)
    complaint_content=models.CharField(max_length=30)
    complaint_replay=models.CharField(max_length=30)
    complaint_status=models.IntegerField(default=0)
    complaint_date=models.DateField(auto_now_add=True)
    farmer=models.ForeignKey(tbl_farmer,on_delete=models.CASCADE)

class tbl_feedback(models.Model):
    feedback_id=models.CharField(max_length=30)
    feedback_content=models.CharField(max_length=100)
    feedback_date=models.DateField(auto_now_add=True)
    farmer=models.ForeignKey(tbl_farmer,on_delete=models.CASCADE)

   



class tbl_rating(models.Model):
    rating_data=models.IntegerField()
    farmer=models.ForeignKey(tbl_farmer,on_delete=models.CASCADE)
    farmer_review=models.CharField(max_length=500)
    machine=models.ForeignKey(tbl_machine,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)
