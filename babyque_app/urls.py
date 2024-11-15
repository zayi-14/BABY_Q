from . import views
# from babyque_app.views import logout_view
from django.urls import path
urlpatterns = [
    path('',views.home,name="home"),
    # path('categories',views.categories,name="categories"),
    # path('check_out',views.check_out,name="check_out"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('product_page',views.product_page,name="product_page"),
    path('profile',views.profile,name="profile"),
    # path('mycart',views.mycart,name="mycart"),
    path('register/', views.register, name='register'),

    # URL to handle OTP request
    path('get-otp/', views.get_otp, name='get_otp'),
    path('login/', views.login_view, name='login'),
    path('send-login-otp/', views.send_login_otp, name='send_login_otp'),
    path('verify-login-otp/', views.verify_login_otp, name='verify_login_otp'),
    path('category/<int:category_id>/', views.products_by_category, name='product_by_category'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-shortlist/', views.add_to_shortlist, name='add_to_shortlist'),
    path('shortlist/', views.shortlist_view, name='shortlist_view'),
    path('add_to_cart',views.add_to_cart,name="add_to_cart"),
    path('my_cart/', views.my_cart, name='my_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),

    path('checkout/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order-tracking/', views.order_tracking, name='order_tracking'),


    # path('order-success/',views.order_success, name='order_success'),

    # Order tracking
    # path('track_order/', views.track_order, name='track_order'),

    # URL for login (assuming you have a login view)
    path('logout/', views.logout_view, name='logout'),
    
]