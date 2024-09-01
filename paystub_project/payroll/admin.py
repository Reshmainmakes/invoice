from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Employee,Location

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'regular_hours', 'overtime_hours', 'final_pay']
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
