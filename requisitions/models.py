from django.db import models
from accounts.models import User, Department
from catalog.models import Product
from decimal import Decimal

# Create your models here.

class Requisition(models.Model):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    FULFILLED = 'FULFILLED'
    CANCELLED = 'CANCELLED'
    
    STATUS_CHOICES = [
        (PENDING, 'PENDING'),
        (APPROVED, 'APPROVED'),
        (REJECTED, 'REJECTED'),
        (FULFILLED, 'FULFILLED'),
        (CANCELLED, 'CANCELLED'),
    ]
    
    # Priority Choices
    # LOW = 'LOW'
    # MEDIUM = 'MEDIUM'
    # HIGH = 'HIGH'
    
    PRIORITY_CHOICES = [
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requisitions')
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='PENDING')
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES, default='MEDIUM')
    notes = models.TextField(blank=True, null=True, help_text="Additional information about the requisition")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Req #{self.id} by {self.requester.username}"
    
    # Calculate total value of requisition
    # @property
    # def total_value(self):
    #     return sum(item.total_price for item in self.items.all())

    

    @property
    def total_value(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.total_price  
        return total



class RequisitionItem(models.Model):
    requisition = models.ForeignKey(Requisition, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True,help_text="Price at time of requisition")

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
    
    # Save unit price automatically when created
    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.unit_price
        super().save(*args, **kwargs)
    
    # Calculate total price for this line item
    # @property
    # def total_price(self):
    #     if self.unit_price:
    #         return self.quantity * float(self.unit_price)
    #     return self.quantity * float(self.product.unit_price)

    @property
    def total_price(self):
        price = self.unit_price if self.unit_price else self.product.unit_price
        return self.quantity * price



class Approval(models.Model):
    APPROVE = 'APPROVE'
    REJECT = 'REJECT'
    
    DECISIONS = [
        (APPROVE, 'Approve'),
        (REJECT, 'Reject'),
    ]

    requisition = models.ForeignKey(Requisition,related_name='approvals', on_delete=models.CASCADE)
    approver = models.ForeignKey(User,on_delete=models.CASCADE)
    decision = models.CharField(max_length=10, choices=DECISIONS)
    comments = models.TextField(blank=True,help_text="Approver comments or feedback")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_decision_display()} by {self.approver.username}"