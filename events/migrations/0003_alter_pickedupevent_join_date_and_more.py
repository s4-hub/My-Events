# Generated by Django 4.1.2 on 2022-11-15 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_pickedupevent_uid_alter_run_down_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickedupevent',
            name='join_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pickedupevent',
            name='uid',
            field=models.UUIDField(default='fcc1fcb931c4424396ebaadf56a4a340'),
        ),
    ]
