from django.contrib import admin
from . import models
# Register your models here.

class CountyAdmin(admin.ModelAdmin):
    search_fields = ["name"]

admin.site.register(models.County, CountyAdmin)

class CountyInfectionInline(admin.TabularInline):
    model = models.CountyInfection

class WeeklyDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Infection date", {"fields" : ["date"]})
    ]
    inlines = [CountyInfectionInline]
    
admin.site.register(models.WeeklyData, WeeklyDataAdmin)