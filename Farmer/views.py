from django.shortcuts import render,redirect
from Guest.models import*
from Officer.models import*
from Farmer.models import*
from Admin.models import*

from django.http import JsonResponse
import os
import joblib
import numpy as np
from PIL import Image
from skimage.io import imread
from keras.models import load_model
from django.http import JsonResponse
from keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

# Load the model once when the server starts
# Load the model
MODEL_PATH = os.path.join("Assets", "updated.h5")
MODEL_PATH = os.path.join("Assets", "38classdisease.h5")
model = load_model(MODEL_PATH)

MODEL2_PATH = os.path.join("Assets", "disease_nlp_model.joblib")
modelcure = joblib.load(MODEL2_PATH)

# Create your views here.
def logout(request):
    del request.session['fid']
    return redirect("Guest:Login")

def HomePage(request):
    return render(request,'Farmer/HomePage.html')
def Myprofile(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        farmerdata=tbl_farmer.objects.get(id=request.session['fid'])
        return render(request,'Farmer/Myprofile.html',{'data':farmerdata})

def Editprofile(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        farmerdata=tbl_farmer.objects.get(id=request.session['fid'])
        if request.method=="POST":
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            contact=request.POST.get('contact_no')
            address=request.POST.get('txt_address')
            bank=request.POST.get('txt_bank')
            account=request.POST.get('txt_account')
            ifsc=request.POST.get('txt_ifsc')
            farmerdata.farmer_name=name
            farmerdata.farmer_email=email
            farmerdata.farmer_contact=contact
            farmerdata.farmer_address=address
            farmerdata.farmer_bank=bank
            farmerdata.farmer_account=account
            farmerdata.farmer_ifsc=ifsc
            farmerdata.save() 
            return render(request,'Farmer/Myprofile.html',{'msg':'Updated', 'data':farmerdata})
        else:
            return render(request,'Farmer/Editprofile.html',{'data':farmerdata})


def Changepassword(request):
    farmerdata=tbl_farmer.objects.get(id=request.session['fid'])
    if request.method=="POST":
        oldpassword=request.POST.get('old_pass')
        newpassword=request.POST.get('new_pass')
        repassword=request.POST.get('re_pass')
        password=farmerdata.farmer_password
        if(password == oldpassword):
            if(newpassword == repassword):
                farmerdata.farmer_password=newpassword
                farmerdata.save()
                return render(request,'Farmer/Myprofile.html',{'msg':'updated'})
            else:   
                return render(request,'Farmer/Changepassword.html',{'msg':'new password missmatch'})
        else:
            return render(request,'Farmer/Changepassword.html',{'msg':'old password incorrect '})
    else:
        return render(request,'Farmer/Changepassword.html')


def Viewnotifications(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        viewnot=tbl_notification.objects.all()
        return render(request,'Farmer/Viewnotifications.html',{'view':viewnot})

def Viewproduct(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        product=tbl_product.objects.all()
        return render(request,'Farmer/Viewproduct.html',{'prod':product})

from django.shortcuts import render, redirect, get_object_or_404

def AddCart(request, pid):

    if "fid" not in request.session:
        return redirect("Guest:Login")

    farmer = get_object_or_404(tbl_farmer, id=request.session['fid'])
    productData = get_object_or_404(tbl_product, id=pid)

    # Check already purchased
    bookingDatacheck = tbl_booking.objects.filter(
        farmer=farmer,
        booking_status=2
    ).first()

    if bookingDatacheck:
        alreadypurchase = tbl_cart.objects.filter(
            booking=bookingDatacheck,
            product=productData
        ).exists()

        # if alreadypurchase:
        #     return render(request, 'Farmer/Viewproduct.html', {'msg': 'Already Purchased'})

    # Get or create active booking (status = 0)
    bookingData, created = tbl_booking.objects.get_or_create(
        farmer=farmer,
        booking_status=0
    )

    # Check already in cart
    cartExists = tbl_cart.objects.filter(
        booking=bookingData,
        product=productData
    ).exists()

    if cartExists:
        return render(request, 'Farmer/Viewproduct.html', {'msg': 'Already Added'})
    else:
        tbl_cart.objects.create(
            booking=bookingData,
            product=productData
        )
        return render(request, 'Farmer/Viewproduct.html', {'msg': 'Added to Cart'})
        

def Mycart(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        if request.method=="POST":
            bookingdata=tbl_booking.objects.get(id=request.session["bookingid"])
            bookingdata.booking_amount=request.POST.get("carttotalamt")
            bookingdata.booking_status=1
            bookingdata.save()
            cart = tbl_cart.objects.filter(booking=bookingdata)
            for i in cart:
                i.cart_status = 1
                i.save()
            return redirect("Farmer:Payment")
        else:
            bookcount = tbl_booking.objects.filter(farmer=request.session["fid"],booking_status=0).count()
            if bookcount > 0:
                book = tbl_booking.objects.get(farmer=request.session["fid"],booking_status=0)
                request.session["bookingid"] = book.id
                cart = tbl_cart.objects.filter(booking=book)
                return render(request,"Farmer/MyCart.html",{'cartdata':cart})
            else:
                return render(request,"Farmer/MyCart.html")

def Payment(request):
    if request.method == "POST":
        return redirect("Farmer:loader")
    return render(request,"Farmer/Payment.html")

def CartQty(request):
   qty=request.GET.get('QTY')
   cartid=request.GET.get('ALT')
   cartdata=tbl_cart.objects.get(id=cartid)
   cartdata.cart_quantity=qty
   cartdata.save()
   return redirect("Farmer:Mycart")   
   
def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("Farmer:Mycart")

def MyBooking(request):
    bookingdata = tbl_booking.objects.filter(farmer=request.session['fid'],booking_status__gt=0)
    return render(request,'Farmer/MyBooking.html',{'bookingdata':bookingdata})


def ViewInsurance(request):
    scheme=tbl_insurance.objects.all()
    return render(request,'Farmer/ViewInsurance.html',{'data':scheme})

def Apply(request,sid):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    count=tbl_request.objects.filter(farmer=request.session['fid'],insurance=sid).count()
    if count>0:
        return render(request,'Farmer/ViewInsurance.html',{'msg':"Your are Already Applied or Claimed this Insurance"})
    else:
        farmerdata=tbl_farmer.objects.get(id=request.session['fid'])
        try:
            officer = tbl_officer.objects.filter(place=farmerdata.place).first()
        except tbl_officer.DoesNotExist:
            officer = None
        insurance=tbl_insurance.objects.get(id=sid)
        req=tbl_request.objects.all()
        if request.method=="POST":
            file=request.FILES.get('file')
            amount=request.POST.get('amount')
            details=request.POST.get('txt_details')

            tbl_request.objects.create(request_file=file,request_amount=amount,request_details=details,farmer=farmerdata ,officer=officer,insurance=insurance)
            return redirect("Farmer:MyInsurance")
        else:
            return render(request,'Farmer/Apply.html',{'data':req,'sid':sid})
    
def MyInsurance(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        req=tbl_request.objects.filter(farmer=request.session['fid'])
        return render(request,'Farmer/MyInsurance.html',{'data':req})

def Delins(request,did):
    tbl_request.objects.get(id=did).delete()
    req=tbl_request.objects.all()
    return render(request,'Farmer/MyInsurance.html',{'msg':'Deleted'})

def ViewMachine(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        products=tbl_machine.objects.all()
        ar = [1, 2, 3, 4, 5]

        parry = []

        for i in products:
            ratecount = tbl_rating.objects.filter(machine=i.id).count()
            tot = 0
            if ratecount > 0:
                ratedata = tbl_rating.objects.filter(machine=i.id)
                for j in ratedata:
                    tot += j.rating_data
                avg = tot // ratecount
                parry.append(avg)
            else:
                parry.append(0)

        datas = zip(products, parry)
        return render(request,'Farmer/ViewMachine.html',{'products':datas,'ar':ar})

def BookMachine(request,bid):
     machine=tbl_machine.objects.get(id=bid)
     farmer=tbl_farmer.objects.get(id=request.session['fid'])
     count = tbl_machinebooking.objects.filter(machine=machine,farmer=farmer).count()
     if count > 0:
        return render(request,'Farmer/ViewMachine.html',{'msg':"Already booked","status":1})
     else:
         tbl_machinebooking.objects.create(machine=machine,farmer=farmer)
         return render(request,'Farmer/ViewMachine.html',{'msg':"booked"})

def MyMachineBooking(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        machine=tbl_machinebooking.objects.filter(farmer_id=request.session['fid'])
        return render(request,'Farmer/MyMachineBooking.html',{'data':machine})

def MachinePayment(request):
    if "fid" not in request.session:
        return redirect("Guest:Login")
    else:
        machine=tbl_machinebooking.objects.get(farmer=request.session['fid'],bookingmachine_status=1)
        if request.method=="POST":
            machine.bookingmachine_status=2
            machine.save()
            return redirect('Farmer:loader')
        else:
            return render(request,'Farmer/MachinePayment.html',{"machine":machine})
        
def loader(request):
    if 'fid' not in request.session:
        return redirect('Guest:login')
    return render(request,"Farmer/Loader.html")

def paymentsuc(request):
    if 'fid' not in request.session:
        return redirect('Guest:login')
    return render(request,"Farmer/Paymentsuc.html")
        
def Claim(request,inid):
    if request.method=="POST":
        req=tbl_request.objects.get(id=inid)
        req.request_status=5
        req.save()
        details=request.POST.get('txt_details')
        file=request.FILES.get('file')
        tbl_claim.objects.create(request=tbl_request.objects.get(id=inid),claim_details=details,claim_file=file)
        return render(request,'Farmer/ClaimApplication.html',{'msg':'Claim Request Sended'})
    else:
        return render(request,'Farmer/ClaimApplication.html')
    

def MyClaimRequest(request):
     claim=tbl_claim.objects.all()
    
     return render(request,'Farmer/MyClaimRequest.html',{'data':claim})

def Complaint(request):
    userdata=tbl_farmer.objects.get(id=request.session['fid'])
    comdata=tbl_complaint.objects.filter(farmer=userdata)
    if request.method=="POST":
        title=request.POST.get('txt_title')
        content=request.POST.get('txt_content')
        tbl_complaint.objects.create(complaint_content=content,complaint_title=title,farmer=userdata)
        return render(request,'Farmer/Complaint.html',{'msg':"Complaint Added"})
    else:
        return render(request,'Farmer/Complaint.html',{'comdata':comdata})
def delcomp(request,cid):
    tbl_complaint.objects.get(id=cid).delete()
    return render(request,'Farmer/Complaint.html',{'msg':"Complaint deleted"})


def Feedback(request):
    userdata=tbl_farmer.objects.get(id=request.session['fid'])
    feeddata = tbl_feedback.objects.filter(farmer=userdata)
    if request.method=="POST":
        content=request.POST.get('txt_name')
        tbl_feedback.objects.create(feedback_content=content,farmer=userdata)
        return render(request,'Farmer/Feedback.html',{'msg':"Feedback"})
    else:
        return render(request,'Farmer/Feedback.html',{'feeddata':feeddata})

def delfeed(request,feid):
  tbl_feedback.objects.get(id=feid).delete()
  return render(request,'Farmer/Feedback.html',{'msg':'Feedback deleted'})
            


def rating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
    # wdata=tbl_booking.objects.get(id=mid)
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(machine=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(machine=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        # print(avg)
        return render(request,"Farmer/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"Farmer/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    
    farmer_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(farmer=tbl_farmer.objects.get(id=request.session['fid']),farmer_review=farmer_review,rating_data=rating_data,machine=tbl_machine.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(machine=pid).order_by('-datetime')
    return render(request,"Farmer/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(machine=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(machine=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)
def Collected(request,coid):
    collect=tbl_machinebooking.objects.get(id=coid)
    collect.bookingmachine_status=4
    collect.save()
    return render(request,'Farmer/MyMachineBooking.html',{'msg':"Collected"})

def About(request):
    return render(request,'Farmer/About.html')
    

#ml section

# Define class labels
class_names = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',     
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 
    'Tomato___healthy'
]

def PredictDisease(request):    
    predicted_class = "No prediction made"

    if request.method == "POST" and request.FILES.get("image"):
        uploaded_image = request.FILES["image"]
        try:
            # Read and preprocess the image
            from PIL import Image
            img = Image.open(uploaded_image)
            img = img.convert('L')
            img = img.convert('RGB')
            img = img.resize((224, 224))  # Resize image to match model input
            img_array = img_to_array(img)  # Convert to array
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array = preprocess_input(img_array)  # Preprocess for the model
            img_array /= 255.0
            # Make prediction
            predictions = model.predict(img_array)
            pred_index = np.argmax(predictions)
            confidence = float(np.max(predictions))  # Confidence score
            predicted_class = class_names[pred_index]
            predicted_class=predicted_class.replace("_", " ")
            print(predicted_class.lower)
            pred_cure_label, cure_confidence = predict_disease(predicted_class)
            # Render the result
            confidence=confidence*100

            print(confidence)
            
            if confidence>80:
                return render(
                    request, 
                    "Farmer/PredictDisease.html", 
                    {"prediction": predicted_class,'med':pred_cure_label}
                )
            else:
                return render(
                    request, 
                    "Farmer/PredictDisease.html", 
                    {'error':"No prediction made Please Provide Real Disease Image",
                    'reason':"Your Image is not clear",
                    'reason2':"Your Image is not related to plant disease",
                    'reason3':"Your Image Contains Multiple Diseases",
                    'reason4':"Your Image Contains Multiple Plants/Leaves",
                    }
                )
        except Exception as e:
            return render(
                request, 
                "Farmer/PredictDisease.html", 
                {"error": f"An error occurred: {str(e)}"}
            )
    else:
        return render(request, "Farmer/PredictDisease.html")

    
def predict_disease(text):
    label = modelcure.predict([text])[0]
    prob = modelcure.predict_proba([text]).max()
    return label, prob

    

