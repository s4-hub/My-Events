# Generated by Django 4.1.2 on 2022-11-22 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_pickedupevent_participant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickedupevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='events.myevents'),
        ),
        migrations.AlterField(
            model_name='pickedupevent',
            name='uid',
            field=models.UUIDField(default='d649e2318e6745498f9379b314502e87'),
        ),
    ]