from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('delete/',   views.delete_view,   name='delete_account'),
       # Use form_class parameter to specify your custom form
    path('profile/', views.profile, name='profile'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email_view, name='verify_email'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('changeusername/', views.changeusername, name='changeusername'),
    path('changefnamelname/', views.changefnamelname, name='changefnamelname'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('reset-password-token/<str:uidb64>/<str:token>/', views.checkresetpasswordtoken, name='checkresetpasswordtoken'),

    path('reset-password/<int:pk>', views.resetpassword, name='reset-password'),
    path('changeemail/', views.changeemail, name='changeemail'),
    path('verifyotp/<str:email>/', views.verifyotp, name='verifyotp')
]