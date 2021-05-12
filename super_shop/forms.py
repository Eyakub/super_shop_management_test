from django import forms

from .models import Product


class CreateOrder(forms.Form):
    customer_name = forms.CharField(max_length=256, 
        label='Customer Name *',
        required=True,
        error_messages={'required': 'Customer name is required.'},
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    customer_phone = forms.CharField(max_length=256, 
        label='Customer Phone *',
        required=True,
        error_messages={'required': 'Customer phone is required.'},
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    customer_email = forms.CharField(max_length=256, 
        label='Customer Email *',
        required=True,
        error_messages={'required': 'Customer email is required.'},
        widget=forms.TextInput(attrs={'class': "form-control"})
    )

    products = forms.ModelChoiceField(queryset=Product.objects.all(), 
        label="Products", required=True,
        error_messages={'required': 'Please select a product.'},
        widget=forms.Select(attrs={'class': 'form-control'}))

    total_unit = forms.CharField(required=True,
        label="Product quantity",
        error_messages={'required': 'Please provide at least 1 product.'},
        widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Enter numbers Only '}))

    def clean_total_unit(self):
        total_unit = self.cleaned_data.get('total_unit', None)
        selected_product = self.cleaned_data.get('products')
        if int(total_unit) > selected_product.current_stock:
            raise forms.ValidationError(
                f"You can't select more than {selected_product.current_stock} product.")
        return total_unit


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'category', 'unit_price', 'current_stock']