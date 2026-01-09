from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from .models import Expense
import json
import pandas as pd
from reportlab.pdfgen import canvas


def dashboard(request):
    total = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'dashboard.html', {'total': total})


def expense_ui_list(request):
    expenses = Expense.objects.all().order_by('-created_at')
    return render(request, 'expense_list.html', {'expenses': expenses})


def expense_add(request):
    if request.method == 'POST':
        Expense.objects.create(
            date=request.POST.get('date'),
            category=request.POST.get('category'),
            amount=request.POST.get('amount'),
            description=request.POST.get('description'),
            payment_mode=request.POST.get('payment_mode'),
            merchant_name=request.POST.get('merchant_name'),
            location=request.POST.get('location'),
            notes=request.POST.get('notes', ''),
            created_by=request.POST.get('created_by')
        )
        return redirect('expense_ui_list')

    return render(request, 'expense_form.html')


@csrf_exempt
def expense_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Expense.objects.create(**data)
        return JsonResponse({'message': 'Expense created'})

    expenses = list(Expense.objects.values())
    return JsonResponse(expenses, safe=False)


@csrf_exempt
def expense_detail(request, id):
    expense = Expense.objects.get(id=id)

    if request.method == 'PUT':
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(expense, key, value)
        expense.save()
        return JsonResponse({'message': 'Expense updated'})

    if request.method == 'DELETE':
        expense.delete()
        return JsonResponse({'message': 'Expense deleted'})

    return JsonResponse(expense.__dict__)


def category_summary(request):
    data = Expense.objects.values('category').annotate(total=Sum('amount'))
    return JsonResponse(list(data), safe=False)


def excel_report(request):
    df = pd.DataFrame(Expense.objects.values())
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=expense_report.xlsx'
    df.to_excel(response, index=False)
    return response


def pdf_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=expense_report.pdf'

    p = canvas.Canvas(response)
    p.drawString(200, 820, "Expense Report (₹ INR)")
    y = 780

    for e in Expense.objects.all():
        p.drawString(50, y, f"{e.date} | {e.category} | ₹{e.amount}")
        y -= 20

    p.showPage()
    p.save()
    return response
