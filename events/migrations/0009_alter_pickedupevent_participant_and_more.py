# Generated by Django 4.1.2 on 2022-11-22 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('events', '0008_alter_pickedupevent_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickedupevent',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peserta', to='profiles.userprofile'),
        ),
        migrations.AlterField(
            model_name='pickedupevent',
            name='uid',
            field=models.UUIDField(default='c430f27a303245fea709bf311a0b916f'),
        ),
    ]