from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm, EmployeePayForm

from django.shortcuts import render
from .models import Employee,Location


from django.shortcuts import render
from .models import Location

def employee_list(request):
    location = request.GET.get('location')  # Get the selected location from the request

    if location:
        employees = Employee.objects.filter(location__name=location)  # Filter by location name
    else:
        employees = Employee.objects.all()  # No location selected, show all

    unique_employees = {}

    for employee in employees:
        key = (employee.name, employee.position)
        if key not in unique_employees:
            unique_employees[key] = employee

    locations = Location.objects.values_list('name', flat=True).distinct()

    return render(request, 'payroll/employee_list.html', {
        'employees': unique_employees.values(),
        'selected_location': location,
        'locations': locations,  # Populate location dropdown
    })



def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'payroll/employee_form.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Employee
from .forms import EmployeePayForm


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeePayForm(request.POST, instance=employee)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.pk = None  # Ensure it's a new instance
            new_employee.save()
            return redirect('employee_table')
    else:
        form = EmployeePayForm(instance=employee)

    return render(request, 'payroll/employee_detail.html', {'employee': employee, 'form': form})

def employee_table(request):
    employees = Employee.objects.all()  # Fetch all employee data
    return render(request, 'payroll/employee_table.html', {'employees': employees})


import openpyxl
from django.http import HttpResponse


def export_employees_to_excel(request):
    selected_location_id = request.GET.get('location', '')
    if selected_location_id:
        employees = Employee.objects.filter(location_id=selected_location_id)
    else:
        employees = Employee.objects.all()

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Employee List'

    headers = [
        'Name', 'Position', 'Total Regular Hours', 'Total Overtime Hours', 'Total Regular Pay',
        'Total Overtime Pay', 'Total Pay', 'Housing Deduction', 'Transportation Deduction',
        'Miscellaneous Deduction', 'Total Deductions', 'Final Pay'
    ]
    worksheet.append(headers)

    for employee in employees:
        worksheet.append([
            employee.name, employee.position, employee.regular_hours, employee.overtime_hours,
            employee.regular_pay, employee.overtime_pay, employee.total_pay,
            employee.housing_deduction_rate, employee.transportation_deduction_rate,
            employee.miscellaneous_deduction_rate, employee.total_deductions, employee.final_pay
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employee_list.xlsx'
    workbook.save(response)

    return response

from django.http import HttpResponse
from reportlab.lib.pagesizes import A2
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import Employee


def export_employees_to_pdf(request):
    selected_location_id = request.GET.get('location', '')
    if selected_location_id:
        employees = Employee.objects.filter(location_id=selected_location_id)
    else:
        employees = Employee.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=employee_list.pdf'

    # Create a PDF document with A3 size
    doc = SimpleDocTemplate(response, pagesize=A2)

    # Define column headers
    headers = [
        'Name', 'Position', 'Total Regular Hours', 'Total Overtime Hours', 'Total Regular Pay',
        'Total Overtime Pay', 'Total Pay', 'Housing Deduction', 'Transportation Deduction',
        'Miscellaneous Deduction', 'Total Deductions', 'Final Pay'
    ]

    # Create data for the table
    data = [headers]
    for employee in employees:
        data.append([
            employee.name,
            employee.position,
            str(employee.regular_hours),
            str(employee.overtime_hours),
            str(employee.regular_pay),
            str(employee.overtime_pay),
            str(employee.total_pay),
            str(employee.housing_deduction_rate),
            str(employee.transportation_deduction_rate),
            str(employee.miscellaneous_deduction_rate),
            str(employee.total_deductions),
            str(employee.final_pay)
        ])

    # Define reduced column widths
    col_widths = [1.3 * inch] * len(headers)  # Adjusted to fit more data on the page

    # Create a Table object with adjusted column widths
    table = Table(data, colWidths=col_widths)

    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
    ])
    table.setStyle(style)

    # Build the PDF document
    doc.build([table])

    return response


from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import datetime

def create_invoice_pdf(request, employee_id):
    # Fetch employee details
    employee = get_object_or_404(Employee, id=employee_id)

    # Define the time period (fortnight_start and fortnight_end)
    fortnight_start = employee.fortnight_start.strftime("%m/%d/%Y")
    fortnight_end = employee.fortnight_end.strftime("%m/%d/%Y")

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{employee.name}_invoice.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 18
    title_style.alignment = TA_CENTER  # Centered
    title_style.textColor = colors.HexColor("#004080")  # Dark blue color

    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.alignment = TA_LEFT

    # Company Information
    company_info = [
        ["STAFFING SOLUTION R US LLC", ""],
        ["8735 DUNWOODY PLACE #4618", ""],
        ["ATLANTA, GA 30350", ""]
    ]

    # Content list to hold the elements of the document
    content = []

    # Company Information Table
    company_table = Table(company_info, colWidths=[4 * inch, 2 * inch])
    company_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004080")),  # Dark blue header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # White background
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
    ]))
    content.append(company_table)
    content.append(Spacer(1, 0.5 * inch))  # Add space below the company info

    # Title
    content.append(Paragraph("Earnings Statement", title_style))
    content.append(Spacer(1, 0.25 * inch))  # Add space below the title

    # Employee Information Table
    employee_info = [
        ["Employee Info", "Pay Date", "Time Period"],
        [f"{employee.name}\n{employee.position}\n{employee.location}",
         datetime.now().strftime("%m/%d/%Y"),
         f"{fortnight_start} - {fortnight_end}"]
    ]
    employee_table = Table(employee_info, colWidths=[3 * inch, 1.5 * inch, 2.5 * inch])
    employee_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004080")),  # Dark blue header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#E6F2FF")),  # Very light blue rows
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#004080")),  # Dark blue gridlines
    ]))
    content.append(employee_table)
    content.append(Spacer(1, 0.5 * inch))  # Add space below the employee info

    # Table Data for Pay Information
    table_data = [
        ["Description", "Amount"],
        ["Total Regular Hours", f"{employee.regular_hours:.2f}"],
        ["Rate per Hour", f"${employee.regular_hour_rate:.2f}"],
        ["Total Regular Pay", f"${employee.regular_pay:.2f}"],
        ["Total Overtime Hours", f"{employee.overtime_hours:.2f}"],
        ["Rate per Hour", f"${employee.overtime_hour_rate:.2f}"],
        ["Total Overtime Pay", f"${employee.overtime_pay:.2f}"],
        ["Total Pay", f"${employee.total_pay:.2f}"],
        ["", ""],  # Blank row for spacing
        ["Deductions", ""],
        ["Housing Deduction", f"${employee.housing_deduction_rate:.2f}"],
        ["Transportation Deduction", f"${employee.transportation_deduction_rate:.2f}"],
        ["Miscellaneous Deduction", f"${employee.miscellaneous_deduction_rate:.2f}"],
        ["Total Deductions", f"${employee.total_deductions:.2f}"],
        ["Final Pay", f"${employee.final_pay:.2f}"]
    ]

    # Create a table
    table = Table(table_data, colWidths=[4 * inch, 2 * inch])

    # Style the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#CCE5FF")),  # Light blue header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#004080")),  # Dark blue text
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Font size for headers
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#E6F2FF")),  # Very light blue rows
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#004080")),  # Dark blue gridlines
    ]))

    content.append(table)
    content.append(Spacer(1, 0.5 * inch))  # Add space below the table

    # Add a footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,  # Centered
        textColor=colors.HexColor("#004080"),  # Dark blue color
    )
    content.append(Paragraph("Thank you for your hard work!", footer_style))

    # Build the PDF
    doc.build(content)

    return response

from django.urls import reverse
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect(reverse('employee_table'))
    return render(request, 'payroll/confirm_delete.html', {'employee': employee})


def login(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == 'veq*8seddch8.WHcM4Bn':
            return redirect('employee_list') # Replace with your actual URL name

        else:
            return render(request, 'payroll/login.html', {'error_message': 'Invalid code. Please try again.'})

    return render(request, 'payroll/login.html')
