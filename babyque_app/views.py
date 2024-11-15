from .models import Category, Product
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Order

def home(request):
    user_id = request.session.get('user_id')
    categories = Category.objects.all()  
    products = Product.objects.all()[:8] 

    # Check if the user has any orders
    order = None
    if user_id:
        order = Order.objects.filter(user_id=user_id).order_by('-id').first()  # Fetch latest order

    return render(request, 'index.html', {
        'categories': categories,
        'products': products,
        'order': order,  # Pass the latest order to the template
    })


# ===============================================================================================
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)  # Fetch related products
    return render(request, 'product-page.html', {'product': product, 'related_products': related_products})


# ==========================================================================================
# def check_out(request):
#     return render (request,"check-out.html")
def order_success(request):
    return render (request,"order_success.html")
def order_failed(request):
    return render (request,"order_failed.html")
def contact(request):
    return render (request,"contact.html")
def product_page(request):
    return render (request,"product-page.html")
def profile(request):
    return render (request,"profile.html")
def mycart(request):
    return render (request,"my_cart.html")
def login_view(request):
    return render (request,"login.html")
def about(request):
    return render (request,"about.html")



# ==============================================================================================

# Send OTP using Twilio
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User
from django.contrib.auth import authenticate, login
import json
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
import random

# Generate a random OTP

def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP using Twilio
def send_otp_via_twilio(phone_number, otp):
    # Debugging: Log the phone number
    print(f"Sending OTP to phone number: {phone_number}")
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
        # Send the message
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,  # Ensure your Twilio phone number is configured in settings
            to=phone_number  # Must be in E.164 format
        )
        print(f"Message SID: {message.sid}")
        return message.sid
    except Exception as e:
        # Log any exceptions
        print(f"Error sending OTP via Twilio: {str(e)}")
        raise e

# View for OTP request (AJAX) with checks for existing accounts
def get_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            email = data.get('email')

            # Check if the email or phone number is already registered
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'success': False, 'message': 'Phone number already registered.'})
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email address already registered.'})

            # Generate and send OTP if no account exists with the given phone or email
            otp = generate_otp()
            send_otp_via_twilio(phone_number, otp)

            # Store OTP in session for later verification
            request.session['otp'] = otp

            return JsonResponse({'success': True, 'message': 'OTP sent successfully!'})
        except Exception as e:
            print(f"Error sending OTP: {str(e)}")  # Log the exception for debugging
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Get the user data from the form
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            otp = form.cleaned_data.get('otp')

            # Simulate OTP verification using session
            user_otp = request.session.get('otp')
            if user_otp and user_otp == otp:
                # OTP is valid, create the user
                user = User.objects.create_user(
                    email=email,
                    full_name=full_name,
                    phone_number=phone_number
                )
                
                # Clear OTP session after success
                del request.session['otp']
                
                # Registration successful, redirect to login
                messages.success(request, "Registration successful!")
                return redirect('login')
            else:
                # OTP is incorrect
                messages.error(request, "Invalid OTP. Please try again.")
        else:
            messages.error(request, "There was an error in the form. Please try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def send_login_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')

            # Check if phone number exists in the database
            if not User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'success': False, 'message': 'Phone number not registered.'})

            # Generate OTP and send it via Twilio
            otp = generate_otp()
            send_otp_via_twilio(phone_number, otp)

            # Store the OTP in session for verification
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number

            return JsonResponse({'success': True, 'message': 'OTP sent successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# View to verify OTP and log the user in
def verify_login_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        entered_otp = request.POST.get('otp')

        session_otp = request.session.get('otp')
        session_phone = request.session.get('phone_number')

        if session_otp == entered_otp and session_phone == phone_number:
            try:
                user = User.objects.get(phone_number=phone_number)
                
                if user.is_blocked:
                    return JsonResponse({'success': False, 'message': 'Your account is blocked.'})

                login(request, user)
                request.session['user_id'] = user.id
                del request.session['otp']
                del request.session['phone_number']

                return JsonResponse({'success': True, 'message': 'Logged in successfully!', 'redirect_url': '/'})  
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid OTP or phone number'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


# =======================================================================================
# views.py
def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    # Get the age filter from the query parameters
    age_filter = request.GET.get('age_filter')

    # Apply the age filter if selected
    if age_filter:
        try:
            age = int(age_filter)
            products = products.filter(age_upto=age)  # Only show products for the exact selected age
        except ValueError:
            pass

    # Create a list of ages (1 to 10)
    ages = list(range(1, 11))

    # Pass the user's shortlisted products to the template
    user_id = request.session.get('user_id')
    shortlisted_products = []
    if user_id:
        user = User.objects.get(id=user_id)
        shortlisted_products = Shortlist.objects.filter(user=user).values_list('product', flat=True)

    return render(request, 'products_by_category.html', {
        'category': category,
        'products': products,
        'ages': ages,
        'shortlisted_products': shortlisted_products,  # Pass to template
    })




# ==========================================================================================
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Shortlist, Product, User
import json

@csrf_exempt
@require_POST
def add_to_shortlist(request):
    # Fetch the user from the session
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not logged in'})

    try:
        # Parse the JSON request body
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'Product ID is required'})

        # Fetch the user and product objects
        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is already in the shortlist
        shortlist, created = Shortlist.objects.get_or_create(user=user, product=product)

        if created:
            return JsonResponse({'status': 'success', 'message': 'Product added to shortlist'})
        else:
            # If already shortlisted, remove it
            shortlist.delete()
            return JsonResponse({'status': 'removed', 'message': 'Product removed from shortlist'})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def shortlist_view(request):
    # Ensure the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    # Fetch the products from the user's shortlist
    shortlisted_products = Product.objects.filter(shortlisted_by__user=user)

    # Render the shortlist view with the shortlisted products
    return render(request, 'shortlist.html', {
        'shortlisted_products': shortlisted_products,
    })


@require_POST
def add_to_cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=403)

    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if product_id and quantity:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user_id=user_id, product=product)
        cart_item.quantity += quantity if not created else quantity
        cart_item.save()

        return JsonResponse({'status': 'success', 'message': 'Product added to cart successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid product or quantity'})



from .models import Cart
from django.http import JsonResponse

def my_cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect if not logged in

    cart_items = Cart.objects.filter(user_id=user_id)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'my_cart.html', {
        'cart_items': cart_items,
        'total': total
    })


from django.views.decorators.http import require_POST

@require_POST
def remove_from_cart(request, cart_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=403)

    cart_item = Cart.objects.filter(id=cart_id, user_id=user_id).first()
    if cart_item:
        cart_item.delete()
        return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Item not found in cart'}, status=404)


from django.views.decorators.http import require_POST
import json

@require_POST
def update_cart_quantity(request, cart_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=403)

    try:
        data = json.loads(request.body)
        new_quantity = int(data.get('quantity', 1))  # Ensure we get the new quantity
    except (ValueError, KeyError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid quantity'}, status=400)

    cart_item = Cart.objects.filter(id=cart_id, user_id=user_id).first()

    if cart_item:
        cart_item.quantity = new_quantity
        cart_item.save()
        return JsonResponse({'status': 'success', 'message': 'Quantity updated'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Item not found in cart'}, status=404)
    
    
def payment_failed(request):
    return render (request,"payment_failed.html")


import logging
import razorpay
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, Order,OrderItem   

logger = logging.getLogger(__name__)

def checkout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Ensure user is logged in

    cart_items = Cart.objects.filter(user_id=user_id)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    print("Total amount calculated:", total_amount)

    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            return JsonResponse({'status': 'error', 'message': 'Address is required'}, status=400)
        
        try:
            # Initialize Razorpay client
            client = razorpay.Client(auth=("rzp_test_RygLyDPora5U2G", "EYw9ReCWe4hioEnnq7OaF8ZM"))
            print("Razorpay Client initialized:", client)
            
            # Payment data with amount converted to paise
            payment_data = {
                "amount": int(total_amount * 100),  # Convert to paise
                "currency": "INR",
                "receipt": f"order_rcptid_{user_id}"
            }
            payment = client.order.create(data=payment_data)  # Creates Razorpay order
            print("Payment object created:", payment)

            # Save the order with Razorpay order ID
            order = Order.objects.create(
                user_id=user_id,
                address=address,
                total_amount=total_amount,
                razorpay_order_id=payment['id']
            )
            return render(request, 'payment.html', {'order': order, 'payment': payment, 'total': total_amount})
        
        except razorpay.errors.BadRequestError as e:
            logger.error("Razorpay BadRequestError: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Invalid data sent to Razorpay.'}, status=500)

        except razorpay.errors.ServerError as e:
            logger.error("Razorpay ServerError: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Razorpay server error, please try again.'}, status=500)

        except Exception as e:
            logger.error("Unexpected Error: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Payment initiation failed due to an unexpected error.'}, status=500)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total_amount,
    })




from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get('razorpay_order_id')
            payment_id = data.get('razorpay_payment_id')

            # Retrieve order and verify
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_id = payment_id
            order.status = 'completed'
            order.save()

            # Move items from Cart to OrderItem and clear the cart
            cart_items = Cart.objects.filter(user_id=order.user_id)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart_items.delete()

            return JsonResponse({'status': 'success', 'message': 'Payment successful and order updated'})
        except Order.DoesNotExist:
            logger.error("Order not found for Razorpay order ID: %s", razorpay_order_id)
            return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
        except Exception as e:
            logger.error("Error processing payment success: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Error processing payment'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)




    


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user_id=request.session.get('user_id'))
    return render(request, 'order_detail.html', {'order': order})



from django.shortcuts import get_object_or_404

def order_confirmation(request):
    user_id = request.session.get('user_id')
    order = Order.objects.filter(user=user_id).latest('created_at')  # Get the latest order for the user
    order_items = order.items.all()  # Fetch all items related to this order

    return render(request, 'order_confirmation.html', {'order': order, 'order_items': order_items})


from django.shortcuts import render, get_object_or_404
from .models import Order


def order_tracking(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login page if user is not authenticated

    try:
        # Fetch orders for the authenticated user
        orders = Order.objects.filter(user=user_id)
        return render(request, 'track_order.html', {'orders': orders})
    except Order.DoesNotExist:
        # Handle case where there are no orders for the user
        return render(request, 'track_order.html', {'orders': None, 'message': 'No orders found.'})



# ==========================================================================================
def logout_view(request):
    del request.session['user_id']
    return redirect('home') 


