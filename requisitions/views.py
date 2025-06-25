from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Requisition, RequisitionItem
from catalog.models import Product
from .models import Approval
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

# view funciton for employee

@login_required(login_url='user_login')
def employee_dashboard(request):
    requisitions = Requisition.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'requisitions/employee_dashboard.html', {
        'requisitions': requisitions
    })


@login_required(login_url='user_login')
def new_requisition(request):
    if request.method == 'POST':
        req = Requisition.objects.create(
            requester=request.user,
            department=request.user.department,
            status='PENDING',
            priority=request.POST.get('priority', 'MEDIUM'),
            notes=request.POST.get('notes', '')
        )
        
        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        
        for i in range(len(product_ids)):
            try:
                if not product_ids[i] or not quantities[i]:
                    continue
                    
                product = Product.objects.get(id=product_ids[i])
                quantity = int(quantities[i])
                
                RequisitionItem.objects.create(
                    requisition=req,
                    product=product,
                    quantity=quantity
                )
            except (Product.DoesNotExist, ValueError):
                continue
        
        messages.success(request, 'Requisition created successfully!')
        return redirect('requisitions:employee_dashboard')
    
    # Handle pre-selected products
    preselected_product = None
    preselected_quantity = 1
    notes = ""
    
    if 'product_id' in request.GET:
        try:
            preselected_product = Product.objects.get(id=request.GET.get('product_id'))
            preselected_quantity = int(request.GET.get('quantity', 1))
            notes = request.GET.get('notes', '')
        except (Product.DoesNotExist, ValueError):
            pass
    
    products = Product.objects.all()
    return render(request, 'requisitions/new_requisition.html', {
        'product_list': products,
        'preselected_product': preselected_product,
        'preselected_quantity': preselected_quantity,
        'preselected_notes': notes
    })


@login_required(login_url='user_login')
def edit_requisition(request, id):
    req = get_object_or_404(
        Requisition,
        id=id,
        requester=request.user,
        status=Requisition.PENDING
    )

    if request.method == 'POST':
        req.items.all().delete()
        req.priority = request.POST.get('priority', 'MEDIUM')
        req.notes = request.POST.get('notes', '')
        req.save()
        
        for pid, qty in zip(request.POST.getlist('product'), request.POST.getlist('quantity')):
            if not (pid and qty): 
                continue
            try:
                product = Product.objects.get(id=pid)
                qty = int(qty)
                if qty > 0:
                    RequisitionItem.objects.create(
                        requisition=req,
                        product=product,
                        quantity=qty
                    )
            except (Product.DoesNotExist, ValueError):
                continue
        
        messages.success(request, 'Requisition updated successfully!')
        return redirect('requisitions:employee_dashboard')

    products = Product.objects.all()
    existing = req.items.all()
    return render(request, 'requisitions/edit_requisition.html', {
        'products': products,
        'requisition': req,
        'existing_items': existing
    })


@login_required(login_url='user_login')
def cancel_requisition(request, id):
    req = get_object_or_404(
        Requisition,
        id=id,
        requester=request.user,
        status=Requisition.PENDING
    )
    req.status = Requisition.CANCELLED
    req.save()
    messages.success(request, 'Requisition cancelled successfully!')
    return redirect('requisitions:employee_dashboard')


# views functions for manager

@login_required(login_url='user_login')
def manager_dashboard(request):
    if request.user.role != 'Manager':
        return HttpResponseForbidden("You must be a manager to view this.")

    pending = Requisition.objects.filter(status=Requisition.PENDING, department=request.user.department).order_by('created_at')
    return render(request, 'requisitions/manager_dashboard.html', {
        'pending_list': pending
    })


@login_required(login_url='user_login')
def approve_requisition(request, id):
    if request.user.role != 'Manager':
        return HttpResponseForbidden("You must be a manager to view this.")
    
    if request.method == 'POST':
        req = get_object_or_404(Requisition, id=id, status=Requisition.PENDING, department=request.user.department)
        comments = request.POST.get('comments', '')
        
        Approval.objects.create(
            requisition=req,
            approver=request.user,
            decision=Approval.APPROVE,
            comments=comments
        )
        req.status = Requisition.APPROVED
        req.save()
        
        return redirect('requisitions:manager_dashboard')


@login_required(login_url='user_login')
def reject_requisition(request, id):
    if request.user.role != 'Manager':
        return HttpResponseForbidden("You must be a manager to view this.")
    
    if request.method == 'POST':
        req = get_object_or_404(Requisition, id=id, status=Requisition.PENDING, department=request.user.department)
        comments = request.POST.get('comments', '')
        
        # Require comments for rejection
        if not comments:
            messages.error(request, "Please provide a reason for rejection")
            return redirect('requisitions:requisition_detail', id=id)
            
        Approval.objects.create(
            requisition=req,
            approver=request.user,
            decision=Approval.REJECT,
            comments=comments
        )
        req.status = Requisition.REJECTED
        req.save()
        
        return redirect('requisitions:manager_dashboard')


@login_required(login_url='user_login')
def requisition_detail(request, id):
    req = get_object_or_404(Requisition, id=id)
    
    # Permission checks
    if request.user.role == 'Employee' and req.requester != request.user:
        return HttpResponseForbidden("You can only view your own requisitions")
        
    if request.user.role == 'Manager' and req.department != request.user.department:
        return HttpResponseForbidden("You can only view requisitions from your department")
    
    # if request.user.role == 'Manager':
    #     # Managers can see all requisitions - no department restriction
    #     pass

    approvals = req.approvals.order_by('timestamp')
    return render(request, 'requisitions/requisition_detail.html', {
        'req': req,
        'approvals': approvals
    })


# @login_required(login_url='user_login')
# def fulfill_requisition(request, id):
#     if request.user.role != 'Inventory Officer':
#         return HttpResponseForbidden("You must be an Inventory Officer to perform this action.")


#     req = get_object_or_404(Requisition,id=id,status=Requisition.APPROVED)
#     for item in req.items.all():
#         prod = item.product
#         prod.current_stock = max(prod.current_stock - item.quantity, 0)
#         prod.save()
#     req.status = Requisition.FULFILLED
#     req.save()
#     return redirect('inventory:dashboard')

