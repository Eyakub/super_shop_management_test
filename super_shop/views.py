from django.shortcuts import render

from super_shop.forms import CreateOrder
from super_shop.models import Product


# Create your views here.
def index(request):
    
    form = CreateOrder(request.POST or None)
    if form.is_valid():
        print('valid')
    # products = Product.objects.all()
    ctx = {
        # 'products': products,
        'form': form
    }
    return render(request, template_name='index.html', context=ctx)


def dashboard_index(request):
    product_list = Product.objects.all()
    ctx = {
        'products': product_list
    }
    return render(request, template_name='dashboard/index.html', context=ctx)
