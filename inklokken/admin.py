from django.contrib import admin, messages

from .models import CompanyNews, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "description", "event_type", "event_from", "event_to")
    list_filter = ["user", "event_type"]


class CompanyNewsAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_on")


admin.site.register(Event, EventAdmin)
admin.site.register(CompanyNews, CompanyNewsAdmin)
