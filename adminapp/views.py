from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def form_basic(request):
    return render (request,"form-basic.html")
def basic_table(request):
    return render (request,"basic-table.html")
def data_table(request):
    return render (request,"datatable.html")
def ad_register(request):
    return render (request,"ad_register.html")
def ad_login(request):
    return render (request,"ad_login.html")
def faq(request):
    return render (request,"faq.html")
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Admin

def admin_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'ad_register.html', {'error': 'Passwords do not match.'})

        try:
            admin = Admin(username=username, email=email, full_name=full_name, phone_number=phone_number)
            admin.set_password(password)
            admin.save()
            return render(request, 'index1.html')  # Redirect to login page after successful registration
        except Exception as e:
            return render(request, 'ad_register.html', {'error': str(e)})

    return render(request, 'ad_register.html')

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.shortcuts import render

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin = authenticate(request, username=username, password=password)

        if admin is not None:
            login(request, admin)
            return render(request, "index1.html")  # Render index.html after successful login
        else:
            # Pass a flag to indicate an error
            return render(request, 'ad_login.html', {'error': 'Invalid username or password.'})

    return render(request, 'ad_login.html')

def admin_logout(request):
    logout(request)  # This will log out the user
    return redirect('admin_login') 

from django.shortcuts import render, redirect
from .forms import CategoryForm

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'add_category.html')  # Redirect to a page that shows a list of categories
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})
# views.py
from django.shortcuts import render
from babyque_app.models import Category

def category_list(request):
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'category_table.html', {'categories': categories})

def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to the category list page after saving
    else:
        form = CategoryForm(instance=category)  # Prepopulate form with existing data
    
    return render(request, 'edit_category.html', {'form': form, 'category': category})


from django.shortcuts import get_object_or_404
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':  # Confirm the deletion via POST
        category.delete()
        return redirect('category_list')  # Redirect to category list after deletion
    
    return render(request, 'delete_category.html', {'category': category})


from django.shortcuts import render, redirect, get_object_or_404
from babyque_app.models import Product,User
from .forms import ProductForm

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'add_product.html')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_table.html', {'products': products})

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})




from django.shortcuts import redirect
from django.contrib import messages

def block_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_blocked = True
        user.save()
        messages.success(request, f"User {user.email} has been blocked.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('user_list')

def unblock_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_blocked = False
        user.save()
        messages.success(request, f"User {user.email} has been unblocked.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('user_list')


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# from django.shortcuts import render
# from babyque_app.models import Order, OrderItem

# def list_users_with_orders(request):
#     orders = Order.objects.select_related('user').prefetch_related('orderitem_set')

#     user_orders_data = {}
#     for order in orders:
#         user = order.user
#         if user not in user_orders_data:
#             user_orders_data[user] = []
        
#         user_orders_data[user].append({
#             'order': order,
#             'items': order.orderitem_set.all(),
#         })

#     context = {
#         'user_orders_data': user_orders_data,
#     }
#     return render(request, 'list_users_with_orders.html', context)
from babyque_app.models import Order,User


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

