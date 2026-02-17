from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view-orders/', views.view_orders, name='view_orders'),
    path('help/', views.help_view, name='help'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_confirm, name='logout'),
    path('products/', views.product_view, name='products'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('update-orders/', views.update_orders, name='update_orders'),
    path('update-order/<int:order_id>/', views.update_order, name='update_order'),



    path('refund-orders/', views.refund_orders, name='refund_orders'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
]
