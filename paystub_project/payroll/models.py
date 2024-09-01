from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # ForeignKey to Location
    regular_hour_rate = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    overtime_hour_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    fortnight_start = models.DateField(null=True, blank=True)
    fortnight_end = models.DateField(null=True, blank=True)
    regular_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    housing_deduction_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    transportation_deduction_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    miscellaneous_deduction_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    @property
    def regular_pay(self):
        return self.regular_hours * self.regular_hour_rate

    @property
    def overtime_pay(self):
        return self.overtime_hours * self.overtime_hour_rate

    @property
    def total_pay(self):
        return self.regular_pay + self.overtime_pay

    @property
    def total_deductions(self):
        return self.housing_deduction_rate + self.transportation_deduction_rate + self.miscellaneous_deduction_rate

    @property
    def final_pay(self):
        return self.total_pay - self.total_deductions

    def __str__(self):
        return self.name
