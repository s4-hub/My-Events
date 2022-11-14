from django.urls import path
from .views import profile, update_profile_2

urlpatterns = [
    path('<str:pk>', profile, name='profile'),
    path('htmx/<str:pk>', update_profile_2, name="update_profile")
]
