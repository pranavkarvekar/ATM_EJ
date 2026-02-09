from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard (summary cards)
    path('', views.dashboard_home, name='dashboard_home'),

    # Transactions table
    path('transactions/', views.transaction_list, name='transaction_list'),

    # Single transaction timeline
    path('timeline/<str:txn_id>/', views.transaction_timeline, name='transaction_timeline'),

    # Failed / error transactions
    path('errors/', views.error_list, name='error_list'),

    # Reconciliation report
    path('reconciliation/', views.reconciliation_report, name='reconciliation_report'),

    # Denomination / cash audit
    path('cash-audit/', views.cash_audit, name='cash_audit'),
]
