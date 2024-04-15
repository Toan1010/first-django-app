from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.

def home(req):
    records = Record.objects.all()
    if req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']
        # authenticate
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, "You have been login")
            return redirect('home')
        else:
            messages.success(req, "There was an err Login")
            return redirect('home')
    return render(req, 'home.html', {"records": records})


def logout_user(req):
    logout(req)
    messages.success(req, "You have been logout")
    return redirect('home')


def register_user(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(req, user)
            messages.success(req, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(req, 'registe.html', {"form": form})
    return render(req, 'registe.html', {"form": form})


def customer_record(req, pk):
    if req.user.is_authenticated:
        customerRecord = Record.objects.get(id=pk)
        return render(req, "record.html", {"record": customerRecord})
    else:
        messages.success(req, "You must Logged to see this record")
        return redirect('home')


def delete_record(req, pk):
    if req.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(req, "Record delete Successfully")
        return redirect("home")
    else:
        messages.success(req, "you need Logged to delete the Record")
        return redirect("home")


def create_record(req):
    form = AddRecordForm(req.POST or None)
    if req.user.is_authenticated:
        if req.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(req, "You have create the new record successfully")
                return redirect('home')
        return render(req, 'create.html', {"form": form})
    else:
        messages.success(req, "you need Logged to create record")
        return redirect("home")


def update_record(req, pk):
    if req.user.is_authenticated:
        current_record  = Record.objects.get(id=pk)
        form = AddRecordForm(req.POST or None, instance=current_record)
        if req.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(req, "You have update the new record successfully")
                return redirect('home')
        return render(req, 'update_record.html', {"form": form})
    else:
        messages.success(req, "you need Logged to create record")
        return redirect("home")

