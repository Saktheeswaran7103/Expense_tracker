from django.urls import path
from . import views

urlpatterns = [
    # UI routes
    path('', views.dashboard, name='dashboard'),
    path('expenses/ui', views.expense_ui_list, name='expense_ui_list'),
    path('expenses/add', views.expense_add, name='expense_add'),

    # API routes
    path('expenses', views.expense_list),
    path('expenses/<int:id>', views.expense_detail),
    path('reports/category-summary', views.category_summary),
    path('reports/excel', views.excel_report),
    path('reports/pdf', views.pdf_report),
]
