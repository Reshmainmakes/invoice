from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # Default path
    path('employee_list/', views.employee_list, name='employee_list'),
    path('new/', views.employee_create, name='employee_create'),
    path('detail/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('table/', views.employee_table, name='employee_table'),
path('export_employees_to_excel/', views.export_employees_to_excel, name='export_employees_to_excel'),
path('export_employees_to_pdf/', views.export_employees_to_pdf, name='export_employees_to_pdf'),
    # URL for employee_table
path('create_invoice_pdf/<int:employee_id>/', views.create_invoice_pdf, name='create_invoice_pdf'),
path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
]
