from django.contrib import admin
from django_calendar.models import Event


class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
