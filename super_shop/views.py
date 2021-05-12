from django.shortcuts import render, redirect

from super_shop.forms import *
from super_shop.models import Product, Order, OrderLine, OrderStatus
import datetime
import qrcode.image.svg
from io import BytesIO

import qrcode
from django.http import HttpResponse


def make_pdf_file(template_src, context):
    template=get_template(template_src)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None

# Create your views here.
def index(request):
    
    form = CreateOrder(request.POST or None)
    if form.is_valid():
        order = Order()
        orderline = OrderLine()
        
        # data
        customer_name = form.cleaned_data['customer_name']
        customer_phone = form.cleaned_data['customer_phone']
        customer_email = form.cleaned_data['customer_email']
        product = form.cleaned_data['products']
        product_quantity = form.cleaned_data['total_unit']
        order_date = datetime.datetime.now()
        
        # order data
        order.customer_name = customer_name
        order.customer_phone = customer_phone
        order.customer_email = customer_email
        order.status = OrderStatus.PENDING
        order.total = int(product_quantity)  * (product.unit_price)
        order.save()

        # order line data
        orderline.name = product.name
        orderline.order = order
        orderline.product = product
        orderline.total_unit = product_quantity
        orderline.total_price = int(product_quantity)  * (product.unit_price)
        orderline.save()

        # this section for qr generator data
        msg = f"Date:\t{order_date}\nInvoice No:\t{order.id}\nName:\t{customer_name}\nPhone:\t{customer_phone}\nEmail:\t{customer_email}"
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(msg, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)

        ctx = {
            'qr_code': stream.getvalue().decode(),
            'product': product,
            'unit_price': product.unit_price,
            'product_quantity': product_quantity,
            'total': order.total
        }
        return render(request, template_name='output.html', context=ctx)
    else:
        ctx = {
            'form': form
        }
    return render(request, template_name='index.html', context=ctx)


def dashboard_index(request):
    product_list = Product.objects.all()
    ctx = {
        'products': product_list
    }
    return render(request, template_name='dashboard/index.html', context=ctx)


def product_add(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard_index')
    ctx = {
        'form': form
    }
    return render(request, template_name='dashboard/product_add.html', context=ctx)


def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('dashboard_index')
    ctx = {'form': form, 'product': product}
    return render(request, template_name='dashboard/product_add.html', context=ctx)


def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('dashboard_index')