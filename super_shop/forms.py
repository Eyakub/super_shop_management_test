from django import forms


class CreateOrder(forms.Form):
    customer_name = forms.CharField(max_length=256, 
        label='Customer Name *',
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    customer_phone = forms.CharField(max_length=256, 
        label='Customer Phone *',
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    customer_email = forms.CharField(max_length=256, 
        label='Customer Email *',
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
