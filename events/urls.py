from django.urls import path
from .views import (list_event,detail_event,active_events, register_event,
                    profile_event, detail_event_uid, certificate, certificate_view, name_tag,
                    GenerateSertifikat, genCert)


urlpatterns = [
    path('', list_event, name='event-list'),
    path('profile/', profile_event,name='profile-event'),
    path('<int:pk>/',detail_event, name='detail-event'),
    path('<str:uuid>/event/',detail_event_uid,name='detail-event-uid'),
    path('active/',active_events, name="active"),
    path('registrasi/',register_event, name="registrasi-event"),
    path('<int:pk>/certificate', certificate, name="certificate"),
    # path('certificate/<str:pk>/',GenerateSertifikat.as_view(), name='certificate-view'),
    path('certificate/<str:pk>/',genCert, name='certificate-view'),
    path('idcard/<int:pk>/',name_tag, name='id-card'),
]
