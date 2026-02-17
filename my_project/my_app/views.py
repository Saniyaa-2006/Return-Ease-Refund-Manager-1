import json
import urllib.request
from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Purchase

# Simple view for the home page
def home(request):
    return render(request, 'my_app/home.html')

# Signup view - redirects to login on success
def signup(request):
    if request.method == 'POST':
        return redirect('login')
    return render(request, 'my_app/signup.html')

# Login view - redirects to dashboard on success
def login(request):
    if request.method == 'POST':
        return redirect('dashboard')
    return render(request, 'my_app/login.html')

# Forgot password view
def forgot_password(request):
    return render(request, 'my_app/forgot_password.html')

# Dashboard view
def dashboard(request):
    orders = Purchase.objects.all().order_by('-purchase_date')
    return render(request, 'my_app/dashboard.html', {'orders': orders})

# View Orders view
def view_orders(request):
    orders = Purchase.objects.all().order_by('-purchase_date')
    return render(request, 'my_app/view_orders.html', {'orders': orders})

# Products view - handles API fetching on the client side for better stability
def product_view(request):
    return render(request, 'my_app/products.html')

# Buy Now view - fetches product info using urllib for zero dependencies
def buy_now(request, product_id):
    product = None
    try:
        url = f'https://dummyjson.com/products/{product_id}'
        # Use a custom User-Agent to avoid blocks from some APIs
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        print(f"DEBUG: Attempting to fetch product {product_id} from {url}")
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                product = json.loads(response.read().decode())
                print(f"DEBUG: Successfully fetched: {product.get('title')}")
            else:
                print(f"DEBUG: API returned status code {response.status}")
    except Exception as e:
        print(f"ERROR: Exception during product fetch: {str(e)}")
        # If it fails, we still want to try to render the page if possible, 
        # but the redirect is a safe fallback. However, let's make sure we log it.
        return redirect('products')

    if not product:
        print(f"ERROR: No product data found for ID {product_id}")
        return redirect('products')

    purchase_date = timezone.now()
    return_deadline = purchase_date + timedelta(days=15)

    if request.method == 'POST':
        try:
            # Store in database
            Purchase.objects.create(
                product_id=product_id,
                product_name=product.get('title', 'Unknown Product'),
                product_price=product.get('price', 0),
                purchase_date=purchase_date,
                return_deadline=return_deadline
            )
            return render(request, 'my_app/purchase_success.html', {'product': product})
        except Exception as e:
            print(f"Error saving purchase: {e}")

    context = {
        'product': product,
        'purchase_date': purchase_date,
        'return_deadline': return_deadline
    }
    return render(request, 'my_app/buy_now.html', context)

# Static information pages
def help_view(request):
    return render(request, 'my_app/help.html')

def about_view(request):
    return render(request, 'my_app/about.html')

def profile_view(request):
    return render(request, 'my_app/profile.html')

# Logout confirmation
def logout_confirm(request):
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'my_app/logout_confirm.html')












# Update Orders view - shows all orders for update selection
def update_orders(request):
    try:
        orders = Purchase.objects.all().order_by('-purchase_date')
        return render(request, 'my_app/update_orders.html', {'orders': orders})
    except Exception as e:
        print(f"Error in update_orders view: {e}")
        return render(request, 'my_app/dashboard.html', {'error': 'Unable to load update page.'})

# Update Order view - handles status updates with product details form API
def update_order(request, order_id):
    try:
        order = Purchase.objects.get(id=order_id)
    except Purchase.DoesNotExist:
        print(f"Order {order_id} not found.")
        return redirect('view_orders')

    # Fetch product details from API
    product = None
    try:
        # Use Product ID to fetch details
        url = f'https://dummyjson.com/products/{order.product_id}'
        
        # Standard headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        # Increased timeout and context handling
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = response.read().decode('utf-8')
                product = json.loads(data)
                print(f"Successfully fetched product: {product.get('title', 'Unknown')}")
            else:
                print(f"API returned status {response.status} for product {order.product_id}")
                
    except Exception as e:
        print(f"Error fetching product details for order {order_id}: {e}")
        # We generally suppress this error so the page still loads even if the API fails
    
    if request.method == 'POST':
        try:
            new_status = request.POST.get('status')
            if new_status:
                order.status = new_status
                order.save()
                print(f"Updated order {order_id} status to {new_status}")
                return redirect('view_orders')
        except Exception as e:
            print(f"Error saving order {order_id}: {e}")

    context = {
        'order': order,
        'product': product
    }
    return render(request, 'my_app/update_order.html', context)


# Refund Orders view - shows all orders for refund processing
def refund_orders(request):
    orders = Purchase.objects.all().order_by('-purchase_date')
    return render(request, 'my_app/refund_orders.html', {'orders': orders})

# Delete Order view - handles cancellation
def delete_order(request, order_id):
    try:
        order = Purchase.objects.get(id=order_id)
    except Purchase.DoesNotExist:
        return redirect('refund_orders')

    if request.method == 'POST':
        order.delete()
        return redirect('refund_orders')

    return render(request, 'my_app/delete_order.html', {'order': order})
