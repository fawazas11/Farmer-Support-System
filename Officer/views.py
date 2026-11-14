from django.shortcuts import render,redirect
from Guest.models import*
from Officer.models import*
from Farmer.models import*
from Admin.models import*
# Create your views here.
def logout(request):
    del request.session['oid']
    return redirect("Guest:Login")

def HomePage(request):
    return render(request,'Officer/HomePage.html')
def Myprofile(request):
    if "oid" not in request.session:
        return redirect("Guest:Login")
    else:
        officerdata=tbl_officer.objects.get(id=request.session['oid'])
        return render(request,'Officer/Myprofile.html',{'data':officerdata})
def Changepassword(request):
    if "oid" not in request.session:
        return redirect("Guest:Login")
    officerdata=tbl_officer.objects.get(id=request.session['oid'])
    if request.method=="POST":
        oldpassword=request.POST.get('old_pass')
        newpassword=request.POST.get('new_pass')
        repassword=request.POST.get('re_pass')
        password=officerdata.officer_password
        if(password == oldpassword):
            if(newpassword == repassword):
                officerdata.officer_password=newpassword
                officerdata.save()
                return render(request,'Officer/Myprofile.html',{'msg':'updated', 'data':officerdata})
            else:   
                return render(request,'Officer/Changepassword.html',{'msg':'new password missmatch'})
        else:
            return render(request,'Officer/Changepassword.html',{'msg':'old password incorrect '})
    else:
        return render(request,'Officer/Changepassword.html')


def Editprofile(request):
    if "oid" not in request.session:
        return redirect("Guest:Login")
    else:
        officerdata=tbl_officer.objects.get(id=request.session['oid'])
        if request.method=="POST":
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            contact=request.POST.get('contact_no')
            address=request.POST.get('txt_address')
            officerdata.officer_name=name
            officerdata.officer_email=email
            officerdata.officer_contact=contact
            officerdata.officer_address=address
            officerdata.save() 
            return render(request,'Officer/Myprofile.html',{'msg':'Updated', 'data':officerdata})
        else:
            return render(request,'Officer/Editprofile.html',{'data':officerdata})

def Notifications(request):
    if "oid" not in request.session:
        return redirect("Guest:Login")
    else:
        data=tbl_notification.objects.all()
        officerdata=tbl_officer.objects.get(id=request.session['oid'])

        if request.method=="POST":
            title=request.POST.get('txt_title')
            details=request.POST.get('txt_details')
            tbl_notification.objects.create(notification_title=title,notification_details=details,officer=officerdata)
            return render(request,'Officer/Notifications.html',{'msg':'Notification sended'})
        else:
            return render(request,'Officer/Notifications.html',{'Officer':data})
        
def Delnot(request,did):
    tbl_notification.objects.get(id=did).delete()
    return render(request,'Officer/Notifications.html',{'msg':'Deleted'})

def Addproduct(request):
    if "oid" not in request.session:
        return redirect("Guest:Login")
    else:
        officerdata=tbl_officer.objects.get(id=request.session['oid'])
        category=tbl_category.objects.all()
        product=tbl_product.objects.all()
        if request.method=="POST":
            name=request.POST.get('txt_name')
            details=request.POST.get('txt_details')  
            price=request.POST.get('price') 
            photo=request.FILES.get('photo')
            categoryid=tbl_category.objects.get(id=request.POST.get('sel_category'))
            tbl_product.objects.create(product_name=name,product_details=details,product_photo=photo,product_price=price,
                                    category=categoryid,officer=officerdata)
            return render(request,'Officer/Addproduct.html',{'msg':'Product added'})
        else:
            return render(request,'Officer/Addproduct.html',{'Officer':product,'category':category} )
    
def ViewBooking(request):
    bookings = tbl_booking.objects.filter(tbl_cart__product__officer=request.session['oid'],booking_status__gt=0)
    return render(request, 'Officer/ViewBooking.html', {'bookings': bookings})
     

def collect(request,bid):
    bookingdata = tbl_booking.objects.get(id=bid)
    bookingdata.booking_status=2
    bookingdata.save()
    return redirect("Officer:ViewBooking")

def ViewRequest(request):
    if "oid" not in request.session:
        return redirect("Guest:Login")
    else:
        officer = tbl_officer.objects.get(id=request.session['oid'])
        req=tbl_request.objects.filter(officer=officer)
        return render(request,'Officer/ViewRequest.html',{'farmer':req})

def Accept(request,aid):
    officer = tbl_officer.objects.get(id=request.session['oid'])
    accept=tbl_request.objects.get(id=aid, officer=officer)
    accept.request_status=1
    accept.save()
    req=tbl_request.objects.filter(officer=officer)
    return render(request,'Officer/ViewRequest.html',{'farmer':req, 'msg':"Accepted"})

def Reject(request,rid):
    officer = tbl_officer.objects.get(id=request.session['oid'])
    reject=tbl_request.objects.get(id=rid, officer=officer)
    reject.request_status=2
    reject.save()
    req=tbl_request.objects.filter(officer=officer)
    return render(request,'Officer/ViewRequest.html',{'farmer':req, 'msg':"Rejected"})

def ViewMachineBooking(request):
    if "oid" not in request.session:
        return redirect("Guest:Login")
    else:
        farmer=tbl_machinebooking.objects.all()
        return render(request,'Officer/ViewMachineBooking.html',{'data':farmer})

def Alert(request,nid):
    noti=tbl_machinebooking.objects.get(id=nid)
    noti.bookingmachine_status=3
    noti.save()
    return render(request,'Officer/ViewMachineBooking.html',{'msg':'Alert Sended'})

def ClaimRequest(request):
    if "oid" not in request.session:
        return redirect("Guest:Login")
    else:
        claim=tbl_claim.objects.all()
        return render(request,'Officer/ClaimRequest.html',{'data':claim})
    
def RequestClaimlist(request):
    farmer=tbl_claim.objects.all()
    return render(request,'Officer/ClaimRequest.html',{'data':farmer})


def AcceptClaim(request,acid):
    accept=tbl_claim.objects.get(id=acid)
    accept.claim_status=1
    accept.save()
    return render(request,'Officer/ClaimRequest.html',{'msg':"Accepted"})

def RejectClaim(request,reid):
    reject=tbl_claim.objects.get(id=reid)
    reject.claim_status=2
    reject.save()
    return render(request,'Officer/ClaimRequest.html',{'msg':"Rejected"})




         

