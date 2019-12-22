from django.contrib import admin
from .models import RateList, AgentsLog, AgentsState
# Register your models here.

class RateAdmin(admin.ModelAdmin):
    list_display = ('id', 'usd')

class LogAdmin(admin.ModelAdmin):
    list_display = ('day', 'test_case', 'name')

admin.site.register(RateList, RateAdmin)
admin.site.register(AgentsLog, LogAdmin)
admin.site.register(AgentsState, LogAdmin)
