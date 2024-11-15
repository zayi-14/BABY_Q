from . import views
from django.urls import path
urlpatterns = [
    # path('index1/', views.index1, name='index1'),
    path('faq', views.faq, name='faq'),
    path('form_basic',views.form_basic,name="form_basic"), 
    path('basic_table',views.basic_table,name="basic_table"), 
    path('data_table',views.data_table,name="data_table"), 
    path('add-category/', views.add_category, name='add_category'),
     path('categories/', views.category_list, name='category_list'),  # The list of categories
    path('edit-category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:id>/', views.delete_category, name='delete_category'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='product_list'),
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('admin_register', views.admin_register, name='admin_register'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('user_list/', views.user_list, name='user_list'),
    path('users/block/<int:user_id>/', views.block_user, name='block_user'),
    path('users/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    # path('list_users_with_orders/', views.list_users_with_orders, name='list_users_with_orders'),
    path('order-list/', views.order_list, name='order-list'),
      
]