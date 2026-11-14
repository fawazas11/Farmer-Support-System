from django.shortcuts import render,redirect
from Guest.models import *
def Signup(request):
    si=tbl_district.objects.all()
    if request.method== "POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        password=request.POST.get('password')
        contact=request.POST.get('contact_no')
        address=request.POST.get('txt_address')
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        photo=request.FILES.get('photo')
        retypepassword=request.POST.get('repassword')
        if(password==retypepassword):
            tbl_user.objects.create(user_name=name,user_email=email,
            user_address=address,user_contact=contact,user_gender=gender,user_password=password,
            user_dob=dob,user_photo=photo,place=place)
            return render(request,'Guest/Signup.html')
        else:
            return render(request,'Guest/Signup.html',{'msg':'Password not match'})
    else:
        return render(request,'Guest/Signup.html',{'district':si})

def ajaxplace(request):
    districtid=tbl_district.objects.get(id=request.GET.get('did'))
    place=tbl_place.objects.filter(district=districtid)
    return render(request,"Guest/AjaxPlace.html",{'place':place})

def Login(request):
    if request.method=="POST":
        email=request.POST.get('txt_email')
        password=request.POST.get('txt_password')
        admincount=tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        usercount=tbl_user.objects.filter(user_email=email,user_password=password).count()
        officercount=tbl_officer.objects.filter(officer_email=email,officer_password=password).count()
        farmercount=tbl_farmer.objects.filter(farmer_email=email,farmer_password=password).count()
    
        if admincount>0:
            admindata=tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session['aid']=admindata.id
            return redirect('Admin:Homepage')
        elif usercount>0:
            userdata=tbl_user.objects.get(user_email=email,user_password=password)
            request.session['uid']=userdata.id
            return redirect('User:Homepage')
        elif  farmercount>0:
            farmerdata=tbl_farmer.objects.get(farmer_email=email,farmer_password=password)
            if farmerdata.farmer_status==1:
                request.session['fid']=farmerdata.id
                return redirect('Farmer:HomePage')
            elif  farmerdata.farmer_status==2:
                return render(request,"Guest/Login.html",{'msg':'verification rejected'})
            elif farmerdata.farmer_status==0:
                return render(request,"Guest/Login.html",{'msg':'verification pending'})
        elif officercount>0:
            Officerdata=tbl_officer.objects.get(officer_email=email,officer_password=password)
            request.session['oid']=Officerdata.id
            if Officerdata.officer_status == 2:
                return render (request,"Guest/Login.html",{'msg':'verification rejected'})
            elif Officerdata.officer_status == 0:
                return render (request,"Guest/Login.html",{'msg':'verification pending'})
            else:
                return redirect('Officer:HomePage')
        else:
            return render(request,"Guest/Login.html",{'msg':'Invalid Email or Password'})
    else:
        return render(request,"Guest/Login.html")


def FarmerRegistration(request):
    district=tbl_district.objects.all()
    if request.method=="POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('contact_no')
        address=request.POST.get('txt_address')
        photo=request.FILES.get('photo')
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        idproof=request.FILES.get('id_proof')
        password=request.POST.get('password')
        confrimpass=request.POST.get('re_password')
        bank=request.POST.get('txt_bank')
        account=request.POST.get('txt_account')
        ifsc=request.POST.get('txt_ifsc')
        if(password==confrimpass):
            tbl_farmer.objects.create(farmer_name=name ,farmer_email=email,
            farmer_contact=contact,farmer_address=address ,farmer_photo=photo,
            #district=district,
            place=place,farmer_proof=idproof,farmer_password=password,
            farmer_bank=bank,farmer_account=account,farmer_ifsc=ifsc)
            return render(request,"Guest/FarmerRegistration.html",{'msg':'Registration Successfull Please Wait For Verification'})
        else:
            return render(request,"Guest/FarmerRegistration.html",{'msg':'password not match'})
    else:
        return render(request,"Guest/FarmerRegistration.html",{'district':district})


def Officer(request):
        district=tbl_district.objects.all()
        if request.method=="POST":
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            contact=request.POST.get('contact_no')
            address=request.POST.get('txt_address')
            photo=request.FILES.get('photo')
            place=tbl_place.objects.get(id=request.POST.get('sel_place'))
            idproof=request.FILES.get('id_proof')
            password=request.POST.get('password')
            confrimpass=request.POST.get('re_password')
            count=tbl_officer.objects.filter(place=place).count()
            if count>0:
                return render(request,"Guest/Officer.html",{'msg':'Place Already Have Agriculture Officer, Try Another Place'})
            if(password==confrimpass):
                tbl_officer.objects.create(officer_name=name ,officer_email=email,
                officer_contact=contact,officer_address=address ,officer_photo=photo,
                place=place,officer_proof=idproof,officer_password=password)
                return render(request,"Guest/Officer.html",{'msg':'Registration Successfull Please Wait For Verification'})
            else:
                return render(request,"Guest/Officer.html",{'msg':'password not match'})
        else:
            return render(request,"Guest/Officer.html",{'district':district})
        
        
def index(request):
    return render(request,'Guest/index.html')


    