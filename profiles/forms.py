from django import forms
from .models import userProfile


class editProfile(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ("nama_perusahaan","nama","no_hp","posisi")
        widgets = {
            'nama_perusahaan':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'nama':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'no_hp':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'posisi':forms.TextInput(attrs={
                'class':'form-control',
            })
        }