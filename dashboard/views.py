from django.shortcuts import render,redirect,get_object_or_404
from . models import Flood_report
from . forms import FloodForm
import folium

# Create your views here.
def home(request):
    if request.method=="POST":
        form=FloodForm(request.POST)
        

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form= FloodForm()
    report=Flood_report.objects.all()
    

    return render(request,"dashboard.html",{"form":form,"reports":report})

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

    

