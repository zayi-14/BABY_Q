from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Category,Product,Shortlist,Order,OrderItem

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'is_admin')
    search_fields = ('email', 'full_name', 'phone_number')
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'phone_number', 'otp', 'is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'otp')}
        ),
    )
    ordering = ('email',)

# Register the custom user model with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Shortlist)
admin.site.register(Order)
admin.site.register(OrderItem)

# admin.site.register(Order)

