from django.shortcuts import render,redirect,get_object_or_404
from . models import Flood_report
from . forms import FloodForm
import folium
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from datetime import datetime
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render (request,"dashboard.html")

@login_required
def add_report(request):
    return render (request,"add_reports.html")

@login_required
def reports(request):
    return render(request,"reports.html")


# Create your views here.
def signup_view(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    return render(request, 'signup.html', {'form': form})



def login_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate (request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect ('login')
 
 
    



def update_report(request,id):
    report=get_object_or_404(Flood_report,id=id)
    if request.method=="POST":
        form=FloodForm(request.POST,instance=report)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=FloodForm(instance=report)
    return render(request,"update.html",{'form':form})

def delete_report(request,id):
    report=get_object_or_404(Flood_report,id=id)
    report.delete()
    return redirect('home')





# 🏠 DASHBOARD (MAIN PAGE)
def dashboard(request):

    reports = Flood_report.objects.all()

    # 📊 Stats
    total = reports.count()
    high = reports.filter(severity='High').count()
    low = reports.filter(severity='Low').count()

    # 🚨 High risk alert
    high_risk = reports.filter(severity='High').first()

    return render(request, "dashboard.html", {
        "total": total,
        "high": high,
        "low": low,
        "high_risk": high_risk,
        "last_updated": datetime.now()
    })


# 📄 REPORTS PAGE (WITH SEARCH)
def reports(request):

    query = request.GET.get('q')

    if query:
        data = Flood_report.objects.filter(location__icontains=query)
    else:
        data = Flood_report.objects.all()

    return render(request, "reports.html", {
        "reports": data
    })


# ➕ ADD REPORT
def add_report(request):

    form = FloodForm()

    if request.method == "POST":
        form = FloodForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('reports')

    return render(request, "add_report.html", {
        "form": form
    })


# ✏️ UPDATE REPORT
def update_report(request, id):

    report = get_object_or_404(Flood_report, id=id)

    if request.method == "POST":
        form = FloodForm(request.POST, instance=report)

        if form.is_valid():
            form.save()
            return redirect('reports')

    else:
        form = FloodForm(instance=report)

    return render(request, "update.html", {
        "form": form
    })


# 🗑️ DELETE REPORT
def delete_report(request, id):

    report = get_object_or_404(Flood_report, id=id)
    report.delete()

    return redirect('reports')

# 📄 REPORTS PAGE
def reports(request):
    query = request.GET.get('q')

    if query:
        data = Flood_report.objects.filter(region__icontains=query)
    else:
        data = Flood_report.objects.all()

    return render(request, "reports.html", {
        "reports": data
    })


# ➕ ADD REPORT
def add_report(request):
    form = FloodForm()

    if request.method == "POST":
        form = FloodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reports')

    return render(request, "add_reports.html", {
        "form": form
    })
def statistics(request):

    reports = Flood_report.objects.all()

    total = reports.count()
    high = reports.filter(severity='High').count()
    medium = reports.filter(severity='Medium').count()
    low = reports.filter(severity='Low').count()


    top_regions = (
        Flood_report.objects
        .values('region')
        .annotate(count=Count('region'))
        .order_by('-count')[:5]
    )

   
    return render(request, "statistics.html", {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "top_regions": top_regions
        
    })
import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import base64

# your credentials
CONSUMER_KEY = "your_key"
CONSUMER_SECRET = "your_secret"
SHORTCODE = "174379"  # test shortcode
PASSKEY = "your_passkey"

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json()['access_token']


@csrf_exempt
def stk_push(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")

        access_token = get_access_token()

        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S') 

       
        password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": "https://yourdomain.com/callback/",
            "AccountReference": "Donation",
            "TransactionDesc": "Support Donation"
        }

        response = requests.post(url, json=payload, headers=headers)
        return JsonResponse(response.json())

    