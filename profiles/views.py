from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from .models import userProfile
from .forms import editProfile

from django.urls import reverse


import requests

API_KEY = '5644982761:AAEVn3itxbBw2a3N9kjjDr29mxkpW34RaU4'

@login_required()
def profile(request, pk):
    data = userProfile.objects.get(user__username=pk)
    print(data)
    return render(request, 'profiles/pages-user-profile.html',{'data':data})

@login_required()
def update_profile(request, pk):
    data = userProfile.objects.get(user_id__username=pk)
    form = editProfile(request.POST or None, instance=data, initial={'nama_perusahaan':data.nama_perusahaan, 'user':data.user.username})

    # if request.method == 'POST':
    #     if form.is_valid():
    #         form.save()
            # return redirect("profile", pk=data.user.username)
    if request.method == 'PUT':
        qd = QueryDict(request.body).dict()
        print(qd)
        form = editProfile(qd, instance=data)
        if form.is_valid():
            form.save()
            return redirect("profile", data.user.username)
    
    context = {
        'form':form,
        'data':data
    }
    return render(request, "profiles/my-profile.html", context)

@login_required()
def update_profile_2(request, pk):
    data = userProfile.objects.get(user_id__username=pk)
    form = editProfile(request.POST or None, instance=data, initial={'nama_perusahaan':data.nama_perusahaan, 'user':data.user.username})

    
    if request.method == 'POST':
        form = editProfile(request.POST, instance=data)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('homepage'))
    
    context = {
        'form':form,
        'data':data
    }
    return render(request, "profiles/my-profile.html", context)

