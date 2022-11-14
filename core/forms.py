from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username","email","password")

        widgets = {
            'username':forms.TextInput(attrs={
                'class':'form-control radius-30 ps-5',
                'placeholder':'Masukkan NPP Anda',
                'id':'inputName'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control radius-30 ps-5',
                'placeholder':'Masukkan Email Anda',
                'id':'inputEmailAddress'
            }),
            'password':forms.PasswordInput(attrs={
                
                'class':'form-control radius-30 ps-5',
                'placeholder':'Masukkan Password Anda',
                'id':'inputChoosePassword'
            }),
            
        }

class regisUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control radius-30 ps-5','placeholder':'Masukan Username Anda','id':'inputUsername'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control radius-30 ps-5','placeholder':'Masukan Email Anda','id':'inputEmailAddress'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control radius-30 ps-5','placeholder':'Masukkan Password','id':'inputChoosePassword'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control radius-30 ps-5','placeholder':'Masukkan Password','id':'Konfirmasi'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']