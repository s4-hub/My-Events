from django.contrib import admin
from .models import myEvents, pickedupEvent, run_down
# Register your models here.

# @admin.register(run_down)

class rundownAdmin(admin.TabularInline):
    model = run_down

class EventAdmin(admin.ModelAdmin):
    inlines = [
        rundownAdmin,
    ]
    class Meta:
        model = myEvents

admin.site.register(myEvents, EventAdmin)

# @admin.register(myEvents)
# class AdminEvents(admin.ModelAdmin):
#     list_display = ('nama_event','lokasi','tgl_acara','selisih_tgl')

# @admin.register(run_down)
# class runDownAdmin(admin.ModelAdmin):
#     list_display = ('event','nama_acara','jadwal')

@admin.register(pickedupEvent)
class AdminPickedupEvent(admin.ModelAdmin):
    list_display = ('participant', 'event','status','serial_num')