from enum import unique
import os
from uuid import uuid4,uuid3
from django.db import models
from PIL import Image
from profiles.models import userProfile
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

def path_and_rename(instance, filename):
    upload_to = 'events'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

def path_sertifikat(instance, filename):
    upload_to = 'events/sertifikat'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class myEvents(models.Model):
    nama_event = models.CharField(max_length=200)
    narasumber = models.CharField(max_length=200)
    lokasi = models.CharField(max_length=300)
    deskripsi = models.TextField()
    tgl_acara = models.DateTimeField()
    tgl_selesai = models.DateTimeField()
    img_event = models.ImageField(upload_to=path_and_rename, blank=True, null=True)
    sertifikat = models.ImageField(upload_to=path_sertifikat, blank=True, null=True)

    def __str__(self):
        return f'{self.nama_event}'

    def selisih_tgl(self):
        if(self.tgl_selesai < timezone.now()):
            return 'selesai'
        elif (self.tgl_acara > timezone.now()):
            return 'mendatang'
        else:
            return 'sedang berlangsung'

    def save(self):
        # if not self.img_event:
        #     return

        super(myEvents, self).save()
        img_event = Image.open(self.img_event)
        (width, height) = img_event.size
        size = (1920,1080)
        
        img_event = img_event.resize(size, Image.ANTIALIAS)
        img_event.save(self.img_event.path)

class pickedupEvent(models.Model):
    participant = models.ForeignKey(userProfile, on_delete=models.CASCADE, related_name='participant')
    event = models.ForeignKey(myEvents, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid4().hex)
    status = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)
    
    def serial_num(self):
        dt = self.join_date.strftime('%d%m%Y%H%M%S%f')
        sn = hex(int(dt))
        return sn[2:]

    def __str__(self):
        return f'{self.participant.nama} - {self.event.nama_event}'

    

    # def save(self):
    #     super(pickedupEvent, self).save()
    #     uid = str(self.uid).split('-','')
    #     uid.save(self.uid)

class run_down(models.Model):
    event = models.ForeignKey(myEvents, on_delete=models.CASCADE, related_name='event_rundown')
    nama_acara = models.CharField(max_length=300, blank=True, null=True)
    jadwal = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return self.event.nama_event

# @receiver(post_save, sender=myEvents, dispatch_uid="create_rundown")
# def create_profile(sender, created, instance, **kwargs):
#     if created:
#         run_down.objects.create(event=instance)