from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import*
from Farmer.models import*
from Officer.models import*

# Create your views re.

def logout(request):
    del request.session['aid']
    return redirect("Guest:Login")


def District(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        dis=tbl_district.objects.all()
        if request.method== "POST":
            name=request.POST.get('txt_district')
            tbl_district.objects.create(district_name=name)
            return render(request,'Admin/District.html',{'msg':'updated'})
        else:
            return render(request,'Admin/District.html',{"district":dis})

def deldistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return render(request,'Admin/District.html',{'msg':'deleted'})
def editdistrict(request,eid):
    edit=tbl_district.objects.get(id=eid)
    if request.method=="POST":
        name=request.POST.get('txt_district')
        edit.district_name=name
        edit.save() 
        return render(request,'Admin/District.html',{'msg':'updated'})
    else:
        return render(request,'Admin/District.html',{'editdata':edit})
def Category(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        cat=tbl_category.objects.all()
        if request.method=="POST":
            name=request.POST.get('category_name')
            tbl_category.objects.create(category_name=name)
            return render(request,'Admin/Category.html',{'msg':'Added'})
        else:
            return render(request,'Admin/Category.html',{"category":cat})
def delcategory(request,cid):
    tbl_category.objects.get(id=cid).delete()
    return render(request,'Admin/Category.html')
def editcategory(request,eid):
    edit=tbl_category.objects.get(id=eid)
    if request.method=="POST":
        name=request.POST.get('category_name')
        edit.category_name=name
        edit.save() 
        return render(request,'Admin/Category.html',{'msg':'updated'})
    else:
        return render(request,'Admin/Category.html',{'editdata':edit})
def Registration(request):
    reg=tbl_admin.objects.all()
    if request.method=="POST":
        name=request.POST.get('txt_registration_1')
        email=request.POST.get('txt_email_1')
        password=request.POST.get('txt_password')
        tbl_admin.objects.create(admin_name=name,admin_email=email,admin_password=password)
        return render(request,'Admin/Registration.html',{'msg':'Successfull'})
    else:   
        return render(request,'Admin/Registration.html',{"Admin":reg})
def delreg(request,rid):
    tbl_admin.objects.get(id=rid).delete()
    return render(request,'Admin/Registration.html',{'msg':"Deleted"})

def editreg(request,eid):
    edit=tbl_admin.objects.get(id=eid)
    if request.method=="POST":
        name=request.POST.get('txt_registration_1')
        email=request.POST.get('txt_email_1')
        password=request.POST.get('txt_password')
        edit.admin_name=name
        edit.admin_email=email
        edit.admin_password=password
        edit.save() 
        return render(request,'Admin/Registration.html',{'msg':'updated'})
    else:
        return render(request,'Admin/Registration.html',{'editdata':edit})

def Place(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        dis=tbl_district.objects.all()
        placedata=tbl_place.objects.all()
        if request.method=="POST":
            name=request.POST.get('txt_name')
            districtid=tbl_district.objects.get(id=request.POST.get('sel_district'))
            tbl_place.objects.create(place_name=name,district=districtid)
            return render(request,'Admin/Place.html')
        else: 
            return render(request,'Admin/Place.html',{'district':dis,'plc':placedata})
def delplace(request,pid):
    tbl_place.objects.get(id=pid).delete()
    return render(request,'Admin/Place.html',{'msg':"Deleted"})
def editplace(request,peid):
    dis=tbl_district.objects.all()
    edit=tbl_place.objects.get(id=peid)
    if request.method=="POST":
        name=request.POST.get('txt_name')
        edit.place_name=name
        edit.save() 
        return render(request,'Admin/Place.html',{'msg':'updated'})
    else:
        return render(request,'Admin/Place.html',{'editdata':edit,"district":dis})

            

def Subcategory(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        sub=tbl_category.objects.all()
        subdata=tbl_subcategory.objects.all()
        if request.method=="POST":
            name=request.POST.get('txt_name')
            categoryid=tbl_category.objects.get(id=request.POST.get('sel_category'))
            tbl_subcategory.objects.create(sub_name=name,category=categoryid)
            return render(request,'Admin/Subcategory.html')
        else:
            
            return render(request,'Admin/Subcategory.html',{'subdata':subdata,'sub':sub})
def delsub(request,sid):
        tbl_subcategory.objects.get(id=sid).delete()
        return render(request,'Admin/Subcategory.html',{'msg':"Deleted"})
def editsub(request,seid):
    sub=tbl_category.objects.all()
    edit=tbl_subcategory.objects.get(id=seid)
    if request.method=="POST":
        name=request.POST.get('txt_name')
        edit.sub_name=name
        edit.save() 
        return render(request,'Admin/Subcategory.html',{'msg':'updated'})
    else:
        return render(request,'Admin/Subcategory.html',{'editdata':edit,"sub":sub})

def Homepage(request):
    return render(request,'Admin/HomePage.html')
def Userlist(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        userss=tbl_user.objects.filter(user_status=0)
        accuser=tbl_user.objects.filter(user_status=1)
        rejuser=tbl_user.objects.filter(user_status=2)

        return render(request,'Admin/Userlist.html',{'view':userss,'accuser':accuser,'rejuser':rejuser})

def Accept(request,aid):
    acUser=tbl_user.objects.get(id=aid)
    acUser.user_status=1
    acUser.save()
    return render(request,'Admin/Userlist.html',{'msg':"Accepted"})
    
def Reject(request,rid):
    acUser=tbl_user.objects.get(id=rid)
    acUser.user_status=2
    acUsser.save()
    return render(request,'Admin/Userlist.html',{'msg':"Rejected"})

def Viewcomplaint(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        complaints=tbl_complaint.objects.all()
        return render(request,'Admin/Viewcomplaint.html',{'comp':complaints})

def Reaplay(request,reid):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        complaints=tbl_complaint.objects.get(id=reid)
        if request.method=="POST":
            name=request.POST.get('txt_replay')
            complaints.complaint_replay=name
            complaints.complaint_status=1
            complaints.save()
            return render(request,'Admin/Reaplay.html',{'msg':"Replayed"})
        else:
            return render(request,'Admin/Reaplay.html',{'msg':"Replayed"})
        
def ViewFeedback(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        feedback=tbl_feedback.objects.all()
        return render(request,'Admin/ViewFeedback.html',{'feed':feedback})

def Farmerlist(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        Farmers=tbl_farmer.objects.filter(farmer_status=0)
        acFarmer=tbl_farmer.objects.filter(farmer_status=1)
        reFarmer=tbl_farmer.objects.filter(farmer_status=2)

    return render(request,'Admin/Farmerlist.html',{'view':Farmers,'acfarmer':acFarmer,'reFarmer':reFarmer})


def AcceptFarmer(request,aid):
    acFarmer=tbl_farmer.objects.get(id=aid)
    acFarmer.farmer_status=1
    acFarmer.save()
    return render(request,'Admin/Farmerlist.html',{'msg':"Accepted"})
def RejectFarmer(request,rid):
    acFarmer=tbl_farmer.objects.get(id=rid)
    acFarmer.farmer_status=2
    acFarmer.save()
    return render(request,'Admin/Farmerlist.html',{'msg':"Rejected"})


def Officerlist(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        Officers=tbl_officer.objects.filter(officer_status=0)
        acOfficer=tbl_officer.objects.filter(officer_status=1)
        reOfficer=tbl_officer.objects.filter(officer_status=2)
        return render(request,'Admin/Officerlist.html',{'view':Officers,'acOfficer':acOfficer,'reOfficer':reOfficer})


def AcceptOfficer(request,aid):
    acOfficer=tbl_officer.objects.get(id=aid)
    acOfficer.officer_status=1
    acOfficer.save()
    return render(request,'Admin/Officerlist.html',{'msg':"Accepted"})
def RejectOfficer(request,rid):
    acOfficer=tbl_officer.objects.get(id=rid)
    acOfficer.officer_status=2
    acOfficer.save()
    return render(request,'Admin/Officerlist.html',{'msg':"Rejected"})


def InsuranceSchemes(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        data=tbl_insurance.objects.all()
        if request.method=="POST":
            name=request.POST.get("txt_name")
            details=request.POST.get('txt_details')
            amount=request.POST.get('amount')
            file=request.FILES.get('file')
            tbl_insurance.objects.create(insurance_name=name,insurance_details=details,insurance_amount=amount,insurance_file=file)
            return render(request,'Admin/InsuranceSchemes.html',{'msg':'Added'})
        else:
            return render(request,'Admin/InsuranceSchemes.html',{'insu':data,})
    
def delins(request,sid):
    tbl_insurance.objects.get(id=sid).delete()
    return render(request,'Admin/InsuranceSchemes.html',{'msg':"Deleted"})

def Machine(request):
    data=tbl_machine.objects.all()
    if request.method=="POST":
        name=request.POST.get("txt_name")
        details=request.POST.get("txt_details")
        photo=request.FILES.get("photo")
        price=request.POST.get('price')
        tbl_machine.objects.create(machine_name=name,machine_details=details,machine_photo=photo,machine_price=price)
        return render(request,'Admin/Machine.html',{'msg':'Added'})
    else:
        return render(request,'Admin/Machine.html',{'machine':data})
    
def delmechine(request,did):
    tbl_machine.objects.get(id=did).delete()
    return render(request,'Admin/Machine.html',{'msg':'Deleted'})

def Bookinglist(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        farmer=tbl_machinebooking.objects.all()
        return render(request,'Admin/Bookinglist.html',{'data':farmer})
         
def RequestClaimlist(request):
    farmer=tbl_request.objects.all()
    return render(request,'Admin/RequestClaimlist.html',{'data':farmer})

def AcceptClaim(request,acid):
    accept=tbl_request.objects.get(id=acid)
    accept.request_status=3
    accept.save()
    return render(request,'Admin/RequestClaimlist.html',{'msg':"Accepted"})

def RejectClaim(request,reid):
    reject=tbl_request.objects.get(id=reid)
    reject.request_status=2
    reject.save()
    return render(request,'Admin/RequestClaimlist.html',{'msg':"Rejected"})

def Amount(request,aid):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        amount=tbl_request.objects.get(id=aid)
        if request.method=="POST":
            claim=request.POST.get('amount')
            amount.claim_amount=claim
            amount.request_status=4
            amount.save()
  
            return render(request,'Admin/Amount.html',{'msg':'Amount Added'})
        else:
            return render(request,'Admin/Amount.html',{'Claim':amount})
        
def Pay(request,pid):
    payed=tbl_request.objects.get(id=pid)
    payed.request_status=6
    payed.save()
    return render(request,'Admin/RequestClaimlist.html',{'msg':"Amount Payed"})

def viewclaimdetails(request,rid):
    data=tbl_claim.objects.filter(request=rid).first()
    return render(request,'Admin/ViewClaimDetails.html',{'claims':data})

def SendNotifications(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        data=tbl_notification.objects.all()
        officerdata=tbl_officer.objects.get(id=request.session['oid'])

        if request.method=="POST":
            title=request.POST.get('txt_title')
            details=request.POST.get('txt_details')
            tbl_notification.objects.create(notification_title=title,notification_details=details,)
            return render(request,'Admin/SendNotifications.html',{'msg':'Notification sended'})
        else:
            return render(request,'Admin/SendNotifications.html',{'Officer':data})
        
def Delnot(request,did):
    tbl_notification.objects.get(id=did).delete()
    return render(request,'Admin/SendNotifications.html',{'msg':'Deleted'})

    
         
