from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class userProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_perusahaan = models.CharField(max_length=300)
    nama = models.CharField(max_length=200)
    posisi = models.CharField(max_length=200)
    no_hp = models.CharField(max_length=13)
    id_telegram = models.CharField(max_length=9, null=True, blank=True)

    def __str__(self):
        if self.nama is None:
            return self.pk
        else:
            return self.nama


@receiver(post_save, sender=User, dispatch_uid="create_profile")
def create_profile(sender, created, instance, **kwargs):
    if created:
        userProfile.objects.create(user=instance)
