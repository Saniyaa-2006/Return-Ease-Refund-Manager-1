from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from .models import Purchase, ReturnRequest, Customer
from .forms import CustomerForm, PurchaseForm, ReturnRequestForm, ProfileUpdateForm
from django.db.models import Count, Sum
from django.contrib import messages
import datetime

def home(request):
    """
    Landing page: Redirect to dashboard if already logged in,
    otherwise show the home page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def signup(request):
    """
    Signup page: Redirect to dashboard if already logged in.
    On successful signup, redirect to the login page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Multi-admin setup: Every new user is a staff & superuser
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, 'Account created! You are now an administrator. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    total_purchases = Purchase.objects.count()
    total_returns = ReturnRequest.objects.count()
    active_refunds = ReturnRequest.objects.filter(status__in=['Pending', 'Approved']).count()
    completed_refunds = ReturnRequest.objects.filter(status='Completed').count()
    recent_requests = ReturnRequest.objects.order_by('-return_date')[:5]
    
    context = {
        'total_purchases': total_purchases,
        'total_returns': total_returns,
        'active_refunds': active_refunds,
        'completed_refunds': completed_refunds,
        'recent_requests': recent_requests
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_purchase(request):
    if request.method == 'POST':
        c_form = CustomerForm(request.POST)
        p_form = PurchaseForm(request.POST)
        
        if c_form.is_valid() and p_form.is_valid():
            phone = c_form.cleaned_data.get('phone')
            name = c_form.cleaned_data.get('name')
            # Check if customer exists
            customer, created = Customer.objects.get_or_create(phone=phone, defaults={'name': name})
            
            purchase = p_form.save(commit=False)
            purchase.customer = customer
            purchase.save()
            messages.success(request, 'Purchase added successfully!')
            return redirect('dashboard')
    else:
        c_form = CustomerForm()
        p_form = PurchaseForm()
        
    return render(request, 'add_purchase.html', {'c_form': c_form, 'p_form': p_form})

@login_required
def view_purchases(request):
    purchases = Purchase.objects.order_by('-purchase_date').prefetch_related('returnrequest_set')
    return render(request, 'view_purchases.html', {'purchases': purchases})

@login_required
def return_request(request):
    # For simplicity, we search purchase by bill_number
    bill_number = request.GET.get('bill_number') or ''
    if request.method == 'POST':
        bill_number = request.POST.get('bill_number')
        try:
            purchase = Purchase.objects.get(bill_number=bill_number)
            r_form = ReturnRequestForm(request.POST, request.FILES)
            if r_form.is_valid():
                ret_req = r_form.save(commit=False)
                ret_req.purchase = purchase
                ret_req.refund_amount = purchase.price # Default refund to full price
                ret_req.save()
                messages.success(request, 'Return request submitted successfully!')
                return redirect('dashboard')
        except Purchase.DoesNotExist:
            messages.error(request, 'Purchase with this bill number not found.')
            r_form = ReturnRequestForm(request.POST, request.FILES)
    else:
        r_form = ReturnRequestForm()
        
    return render(request, 'return_request.html', {'r_form': r_form, 'bill_number': bill_number})

@login_required
def refund_management(request):
    refunds = ReturnRequest.objects.exclude(status='Completed').order_by('-return_date')
    return render(request, 'refund_management.html', {'refunds': refunds})

@login_required
def update_refund_status(request, pk, status):
    refund = get_object_or_404(ReturnRequest, pk=pk)
    if status in dict(ReturnRequest.STATUS_CHOICES):
        refund.status = status
        refund.save()
        messages.success(request, f'Refund status updated to {status}.')
        if status == 'Completed':
            return redirect('dashboard')
    return redirect('refund_management')

@login_required
def refund_history(request):
    refunds = ReturnRequest.objects.filter(status='Completed').order_by('-return_date')
    return render(request, 'refund_history.html', {'refunds': refunds})

@login_required
def customer_records(request):
    customers = Customer.objects.annotate(
        total_purchases=Count('purchase', distinct=True),
        total_returns=Count('purchase__returnrequest', distinct=True)
    )
    return render(request, 'customer_records.html', {'customers': customers})

@login_required
def reports(request):
    # Monthly Report for current year
    current_year = datetime.datetime.now().year
    monthly_refunds = ReturnRequest.objects.filter(
        status='Completed', 
        return_date__year=current_year
    ).values('return_date__month').annotate(total=Sum('refund_amount')).order_by('return_date__month')
    
    total_refund = ReturnRequest.objects.filter(status='Completed').aggregate(Sum('refund_amount'))['refund_amount__sum'] or 0
    
    context = {
        'monthly_refunds': monthly_refunds,
        'total_refund': total_refund,
    }
    return render(request, 'reports.html', context)

@login_required
def profile_settings(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            u_form = ProfileUpdateForm(request.POST, instance=request.user)
            p_form = PasswordChangeForm(request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Profile details updated successfully!')
                return redirect('dashboard')
        elif 'change_password' in request.POST:
            u_form = ProfileUpdateForm(instance=request.user)
            p_form = PasswordChangeForm(request.user, request.POST)
            if p_form.is_valid():
                user = p_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('dashboard')
        else:
             u_form = ProfileUpdateForm(instance=request.user)
             p_form = PasswordChangeForm(request.user)
    else:
        u_form = ProfileUpdateForm(instance=request.user)
        p_form = PasswordChangeForm(request.user)
        
    return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})

def about(request):
    return render(request, 'about.html')

@login_required
def help_view(request):
    return render(request, 'help.html')

@login_required
def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'logout_confirm.html')
def forgot_password(request):
    """
    Simplified password reset: User provides username and new password.
    Note: In a production app, this should have more security (like email verification).
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not username or not new_password:
            messages.error(request, "Please fill in all fields.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully! Please log in with your new password.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "User with this username not found.")
                
    return render(request, 'forgot_password_simple.html')
