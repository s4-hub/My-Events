from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from .forms import NewUserForm, regisUserForm
from profiles.models import userProfile
from django.db.models import Subquery, OuterRef, Q, Count
from events.models import myEvents,pickedupEvent,run_down

def information_front(request):
    if(request.user.is_authenticated):
        return redirect('homepage')
    obj = myEvents.objects.all().annotate(jlh_peserta=Count('event'))
    
    # obj = myEvents.objects.all().annotate(jlh_peserta=Count('pickedupevent__participant')).annotate(events=Subquery(run_down.objects.filter(event=OuterRef('pk')).values_list('jadwal','nama_acara').values('nama_acara').values('jadwal')))
    # print(obj)
    return render(request, 'informations.html', {'obj':obj})

def details_event(request,pk):
    datas = run_down.objects.filter(event=pk)
    obj = myEvents.objects.filter(pk=pk).annotate(jlh_peserta=Count('event'))
    
    # print(datas)
    return render(request, 'details_event.html',{'obj':obj})

def home_page(request):
    user = request.user
    if user.is_superuser:
        pass
    else:
        get_user = userProfile.objects.get(user__username=user)
        if (get_user.nama == "") or (get_user.no_hp == "") or (get_user.posisi == ""):
            messages.error(request, "Silahkan Lengkapi Data Anda Terlebih dahulu")
    datas = myEvents.objects.all().order_by('-tgl_acara')
    return render(request, 'index.html',{'datas':datas})

def newUser(request):
    
    # form = NewUserForm(request.POST)
    
    if request.method == 'POST':
        form = regisUserForm(request.POST)
        if form.is_valid():
            form.save()
            # post = form.save(commit=False)
            # post.password = form.cleaned_data['password']
            
            # post.save()
            messages.success(request, 'User Anda Berhasil Terdaftar')
            # return JsonResponse({'msg':'success'})
    else:
        messages.error(request, 'Coba Kembali!')
        form = form = regisUserForm()
            
    return render(request, 'signup.html', {'form':form})


def loginUser(request):
    return render(request, 'login.html')

def loginUser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'Anda berhasil login!')
    else:
        messages.error(request, 'Login Anda Gagal!')
        

def userLogout(request):
    logout(request)
    return redirect('/')