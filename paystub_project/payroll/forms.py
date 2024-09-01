from django import forms
from .models import Employee, Location

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position','location']
class EmployeePayForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['location','fortnight_start', 'fortnight_end', 'regular_hours', 'overtime_hours',
                  'housing_deduction_rate', 'transportation_deduction_rate', 'miscellaneous_deduction_rate']
        widgets = {
            'fortnight_start': forms.DateInput(attrs={'type': 'date'}),
            'fortnight_end': forms.DateInput(attrs={'type': 'date'}),
            'regular_hours': forms.NumberInput(attrs={'step': '0.01'}),
            'overtime_hours': forms.NumberInput(attrs={'step': '0.01'}),
            'regular_hour_rate': forms.NumberInput(attrs={'step': '0.01'}),
            'overtime_hour_rate': forms.NumberInput(attrs={'step': '0.01'}),
            'housing_deduction_rate': forms.NumberInput(attrs={'step': '0.01'}),
            'transportation_deduction_rate': forms.NumberInput(attrs={'step': '0.01'}),
            'miscellaneous_deduction_rate': forms.NumberInput(attrs={'step': '0.01'}),
        }
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
