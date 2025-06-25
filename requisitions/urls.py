from django.urls import path
from .views import * 

app_name = 'requisitions'

urlpatterns = [
    path('employee/', employee_dashboard, name='employee_dashboard'),
    path('manager/', manager_dashboard, name='manager_dashboard'),
    path('new/', new_requisition, name='new_requisition'),
    path('edit/<int:id>/', edit_requisition, name='edit_requisition'),
    path('cancel/<int:id>/', cancel_requisition, name='cancel_requisition'),
    path('approve/<int:id>/', approve_requisition, name='approve_requisition'),
    path('reject/<int:id>/', reject_requisition, name='reject_requisition'),
    path('detail/<int:id>/', requisition_detail, name='requisition_detail'),
]

