from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    
    # Password Reset (Simplified)
    path('forgot-password/', views.forgot_password, name='password_reset'),


    path('logout/', views.logout_confirm, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('help/', views.help_view, name='help'),
    path('add-purchase/', views.add_purchase, name='add_purchase'),
    path('view-purchases/', views.view_purchases, name='view_purchases'),
    path('return-request/', views.return_request, name='return_request'),
    path('refund-management/', views.refund_management, name='refund_management'),
    path('update-status/<int:pk>/<str:status>/', views.update_refund_status, name='update_refund_status'),
    path('refund-history/', views.refund_history, name='refund_history'),
    path('customer-records/', views.customer_records, name='customer_records'),
    path('reports/', views.reports, name='reports'),
    path('profile/', views.profile_settings, name='profile'),
]
