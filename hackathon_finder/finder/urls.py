from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='finder/login.html',
        redirect_authenticated_user=True  # Prevent logged-in users from accessing login page
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login',
        template_name='finder/logged_out.html'  # Optional custom template
    ), name='logout'),
    
    # Profiles
    path('', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Messages
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('message/send/<int:receiver_pk>/', views.send_message, name='send_message'),

    # Password Reset (improved with success_url where needed)
    path('password-reset/',  # Fixed typo from 'resest' to 'reset'
         auth_views.PasswordResetView.as_view(
             template_name='finder/password_reset.html',
             email_template_name='finder/password_reset_email.html',
             subject_template_name='finder/password_reset_subject.txt',  # Optional
             success_url='password-reset-done'  # Explicit success URL
         ),
         name='password-reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='finder/password_reset_done.html'
         ),
         name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='finder/password_reset_confirm.html',
             success_url='password-reset-complete'  # Fixed typo from 'complete' to 'complete'
         ),
         name='password-reset-confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='finder/password_reset_complete.html'
         ),
         name='password-reset-complete'),
]