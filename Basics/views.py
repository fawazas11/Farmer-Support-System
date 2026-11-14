from django.shortcuts import render

# Create your views here.
def Sum(request):
    if request.method=="POST":
        a=int(request.POST.get('txt1'))
        b=int(request.POST.get('txt2'))
        c=a+b
        return render(request,'Basics/Sum.html',{'result':c})
    else:
        return render(request,'Basics/Sum.html')

def Largest(request):
    if request.method=="POST":
        a=int(request.POST.get('txtnum1'))
        b=int(request.POST.get('txtnum2'))
        if(a>b):
            return render(request,'Basics/Largest.html',{'result':a})
        else:
            return render(request,'Basics/Largest.html',{'result':b})
    else:
        return render(request,'Basics/Largest.html')
def Calculator(request):
    if request.method=="POST":
        a=int(request.POST.get('txtnum1'))
        b=int(request.POST.get('txtnum2'))
        z=request.POST.get('btn')
        if z=='+':
            c=a+b
            return render(request,'Basics/Calculator.html',{'result':c})
        elif z=='-':
            c=a-b
            return render(request,'Basics/Calculator.html',{'result':c})
        elif z=='*':
            c=a*b
            return render(request,'Basics/Calculator.html',{'result':c})
        elif z=='/':
            c=a/b
            return render(request,'Basics/Calculator.html',{'result':c})
    else:
        return render(request,'Basics/Calculator.html')
def Smallest(request):
    if request.method=="POST":
        a=int (request.POST.get('txt1'))
        b=int (request.POST.get('txt2'))
        if (a<b):
            return render(request,'Basics/Smallest.html',{'result':a})
        else:
            return render (request,'Basics/Smallest.html',{'result':b})
    else:
        return render( request,'Basics/Smallest.html')

