from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order, LineItem
from .forms import CartForm, CheckoutForm
from . import cart
from django.contrib import messages


@login_required
def purchase_tickets(request):
    all_products = Product.objects.all()


    return render(request,'ecommerce_app/purchaseticket.html', {
        'all_products': all_products,
    })





def founder(request):
    return render(request, 'ecommerce_app/founder.html')




def speakers(request):
    return render(request, 'ecommerce_app/speakers.html')





def donation(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        postaladdress = request.POST.get('postaladdress')
        Amount = request.POST.get('amount')
        agree = True

        o = Order(
            name=Name,
            email=Email,
            postal_code=postaladdress,
            agree=agree

        )

        o.save()

        li = LineItem(
            product_id= '4',
            price=Amount,
            quantity=1,
            order_id=o.id
        )

        li.save()
        request.session['order_id'] = o.id
        return redirect('process_payment')
    else:
        return render(request, 'ecommerce_app/Donation.html')


def schedule(request):
    return render(request, 'ecommerce_app/Schedule.html')





def product(request):



    return render(request, 'ecommerce_app/Product.html')




def about(request):
    return render(request, 'ecommerce_app/About.html')


def index(request):

    all_products = Product.objects.all()
    return render(request, "ecommerce_app/index.html", {
        'all_products': all_products,
    })

@login_required
def show_product(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CartForm(request, request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect('show_cart')

    form = CartForm(request, initial={'product_id': product.id})
    return render(request, 'ecommerce_app/product_detail.html', {
        'product': product,
        'form': form,
    })

@login_required
def show_cart(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'Update':
            cart.update_item(request)
        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)


    cart_items = cart.get_all_cart_items(request)
    cart_subtotal = cart.subtotal(request)
    return render(request, 'ecommerce_app/cart.html', {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
    })

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            agree2 = cleaned_data.get('agree')

            o = Order(
                name=cleaned_data.get('name'),
                email=cleaned_data.get('email'),
                postal_code=cleaned_data.get('postal_code'),
                agree=cleaned_data.get('agree')

            )

            o.save()

            all_items = cart.get_all_cart_items(request)
            for cart_item in all_items:
                li = LineItem(
                    product_id=cart_item.product_id,
                    price=cart_item.price,
                    quantity=cart_item.quantity,
                    order_id=o.id
                )

                li.save()

            cart.clear(request)

            request.session['order_id'] = o.id
            if agree2 == False:

                messages.warning(request,
                                 'You must agree to the terms and conditions before proceeding to the checkout.')
                return redirect('checkout')
            else:
                return redirect('process_payment')




    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', {'form': form})

@login_required
def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'ecommerce_app/process_payment.html', {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'ecommerce_app/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'ecommerce_app/payment_cancelled.html')
