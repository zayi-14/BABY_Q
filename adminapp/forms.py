# forms.py
from django import forms
from babyque_app.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
        
        
# forms.py
from django import forms
from babyque_app.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'product_name', 'product_image', 'age_upto', 'price', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'age_upto': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

