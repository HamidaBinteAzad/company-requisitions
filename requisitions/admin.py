from django.contrib import admin
from .models import Requisition, RequisitionItem, Approval

# Register your models here.

class RequisitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'department', 'status', 'priority', 'total_value', 'created_at')
    search_fields = ('requester__username', 'notes')

class RequisitionItemAdmin(admin.ModelAdmin):
    list_display = ('requisition', 'product', 'quantity', 'unit_price', 'total_price')
    search_fields = ('product__name',)

class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('requisition', 'approver', 'decision', 'timestamp')
    search_fields = ('requisition__id', 'approver__username')

admin.site.register(Requisition, RequisitionAdmin)
admin.site.register(RequisitionItem, RequisitionItemAdmin)
admin.site.register(Approval, ApprovalAdmin)
