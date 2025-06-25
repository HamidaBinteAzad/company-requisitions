from django.urls import path
from . views import *

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("registration/", registration, name='registration'),
    path("user_login/", user_login, name='user_login'),
    path("user_logout/", user_logout, name='user_logout'),
    # path("common_dashboard/", common_dashboard, name='common_dashboard'),
    path('profile/', update_profile, name='profile'),
    path('forget_password/', forget_password, name='forget_password'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('reset_password/', reset_password, name='reset_password'),
]
