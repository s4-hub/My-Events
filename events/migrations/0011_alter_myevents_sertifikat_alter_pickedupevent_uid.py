# Generated by Django 4.1.2 on 2022-11-23 01:33

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_pickedupevent_event_alter_pickedupevent_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myevents',
            name='sertifikat',
            field=models.FileField(blank=True, null=True, upload_to=events.models.path_sertifikat, validators=[events.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='pickedupevent',
            name='uid',
            field=models.UUIDField(default='6c557801e6734f068813077bb0a2dad4'),
        ),
    ]
