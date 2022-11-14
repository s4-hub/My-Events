from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

from .views import home_page, newUser, information_front, userLogout, details_event

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', information_front, name="info_front"),
    path('details/<int:pk>', details_event, name="details_event"),
    path('dashboard/', home_page, name="homepage"),
    path('registrasi/', newUser, name="registrasi"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', userLogout, name='logout'),
    path('profile/', include('profiles.urls')),
    path('events/',include('events.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
