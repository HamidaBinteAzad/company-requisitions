from django.shortcuts import render, redirect
from . models import User, Department
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from requisitions.views import *

# Create your views here.

# def common_dashboard(request):
#     return render(request, 'common_dashboard.html')

def registration(request):
    # if request.user.is_authenticated:
    #     messages.success(request, "You are Already Logged In.")
    #     return redirect('common_dashboard')
    if request.user.is_authenticated:
        # Redirect to role-specific dashboard if already logged in
        if request.user.role == User.EMPLOYEE:
            return redirect('requisitions:employee_dashboard')
        elif request.user.role == User.MANAGER:
            return redirect('requisitions:manager_dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        department_id = request.POST.get('department')
        role = request.POST.get('role')

        if not all([username, email, password1, password2, department_id, role]):
            messages.error(request, "All fields are required.")
            return redirect('registration')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('registration')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('registration')

        # user = User(
        #     username=username,
        #     email=email,
        #     role=role,
        #     department=Department.objects.get(id=department_id),
        #     password=make_password(password1)  
        # )

        if password1 == password2:
            # user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, image=image, password=password1 )
            user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name,last_name=last_name,image=image, role=role, department=Department.objects.get(id=department_id))
            user.save()
            return redirect('user_login')
        messages.success(request, "Registration successful. Please log in.")
        return redirect('user_login')

    departments = Department.objects.all()
    roles = User.ROLE_CHOICES
    return render(request, 'accounts/registration.html', {
        'departments': departments,
        'roles': roles
    })



def user_login(request):
    if request.user.is_authenticated:
        return redirect('common_dashboard')  # or a common dashboard
    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # role-based redirect
            if user.role == User.EMPLOYEE:
            # if user.role == 'Employee':
                # return redirect('employee_dashboard')
                return redirect('requisitions:employee_dashboard')
            if user.role == User.MANAGER:
                return redirect('requisitions:manager_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'accounts/login.html') 
    return render(request, 'accounts/login.html')
        
def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('user_login')


# @login_required(login_url='login')
# def user_dashboard(request):
#     # Check if user is authenticated
#     if not request.user.is_authenticated:
#         return redirect('login')
    
#     # Check if user is verified
#     if not request.user.is_verified:
#         return redirect('registration')
    
#     # Use request.user directly; no need to query the database again
#     user_data = request.user
    
#     return render(request, 'auth/user_dashboard.html', {'user_data': user_data})

from django.contrib.auth import update_session_auth_hash
@login_required(login_url='login')
# def update_profile(request, id):
#     user = get_object_or_404(User, id=id)

#     # Ensure user can only update their own profile
#     if request.user.id != user.id:
#         messages.error(request, "You can only update your own profile.")
#         return redirect('user_dashboard')

#     if request.method == 'POST':
#         user.first_name = request.POST.get('first_name', user.first_name)
#         user.last_name = request.POST.get('last_name', user.last_name)
#         image = request.POST.get('image', user.image)
#         user.email = request.POST.get('email', user.email)
        
#         password = request.POST.get('password')
#         if password:
#             user.set_password(password)
#             user.save()
#             update_session_auth_hash(request, user)  # Keeps the user logged in after password change
#         else:
#             user.save()

#         messages.success(request, "Profile updated successfully.")
#         return redirect('user_dashboard')

#     return render(request, 'auth/edit_profile.html', {'user': user})
@login_required
def update_profile(request):
    # Get the current user
    user = request.user
    
    if request.method == 'POST':
        # Update user details
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        # Handle image upload
        if 'image' in request.FILES:
            user.image = request.FILES['image']
        
        # Handle password change
        password = request.POST.get('password')
        if password:
            # Only change password if confirmation matches
            password_confirm = request.POST.get('password_confirm')
            if password == password_confirm:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, "Password updated successfully.")
            else:
                messages.error(request, "Passwords do not match. Password not changed.")
        else:
            user.save()
            messages.success(request, "Profile updated successfully.")
        
        return redirect('profile') 
    
    # For GET request, render the profile page
    return render(request, 'accounts/my_profile.html', {'user': user}) 


import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# OTP Email Function
def send_otp_email(email, otp):
    subject = 'Password Reset OTP'
    message = f'Your OTP for password reset is: {otp}. This OTP is valid for 10 minutes.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

# Forget Password View
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Store OTP and timestamp in session
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            request.session['otp_created'] = str(timezone.now())
            request.session['otp_attempts'] = 0  # Track OTP attempts
            
            # Send OTP email
            send_otp_email(email, otp)
            
            messages.success(request, "OTP has been sent to your email.")
            return redirect('verify_otp')
            
        except User.DoesNotExist:
            messages.info(request, "If your email is registered, you'll receive an OTP shortly.")
    
    return render(request, 'accounts/forget_password.html')

# OTP Verification View
def verify_otp(request):
    # Check if session has reset data
    if 'reset_email' not in request.session:
        messages.error(request, "Invalid request. Please start the password reset process again.")
        return redirect('forget_password')
    
    # Check OTP attempts
    attempts = request.session.get('otp_attempts', 0)
    if attempts >= 3:
        messages.error(request, "Too many failed attempts. Please start again.")
        return redirect('forget_password')
    
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('reset_otp')
        email = request.session.get('reset_email')
        created_time = request.session.get('otp_created')
        
        # Check OTP expiration (10 minutes)
        if created_time:
            created_time = timezone.datetime.fromisoformat(created_time)
            if timezone.now() > created_time + timedelta(minutes=10):
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect('forget_password')
        
        # Verify OTP
        if user_otp == stored_otp:
            request.session['verified'] = True
            # Reset attempts on success
            request.session['otp_attempts'] = 0
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            # Increment attempt count
            request.session['otp_attempts'] = attempts + 1
    
    return render(request, 'accounts/verify_otp.html')

# Password Reset View
def reset_password(request):
    # Check if session has verified flag
    if 'reset_email' not in request.session or not request.session.get('verified'):
        messages.error(request, "Invalid request. Please start the password reset process again.")
        return redirect('forget_password')
    
    email = request.session.get('reset_email')
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')
        
        try:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            
            # Clean up session
            keys = ['reset_otp', 'reset_email', 'otp_created', 'otp_attempts', 'verified']
            for key in keys:
                if key in request.session:
                    del request.session[key]
            
            messages.success(request, "Password reset successfully. You can now login with your new password.")
            return redirect('user_login')
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect('forget_password')
    
    return render(request, 'accounts/reset_password.html')