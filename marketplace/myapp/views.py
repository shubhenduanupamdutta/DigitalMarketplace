from calendar import c
import json
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProductForm, UserRegistrationForm
from .models import OrderDetail, Product
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request, 'myapp/index.html', {'products': products})


def detail(request, id):
    product = Product.objects.get(id=id)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    context = {'product': product, 'stripe_public_key': stripe_public_key}
    return render(request, 'myapp/detail.html', context)


@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=request_data['email'],
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': product.name,
                        },
                        'unit_amount': int(product.price * 100),
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')) +
            "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed'))
        )
        print(checkout_session)

        order = OrderDetail()
        order.customer_email = request_data['email']
        order.product = product
        order.amount = int(product.price)
        order.strip_session_id = checkout_session.id
        order.save()

        return JsonResponse({'sessionId': checkout_session.id})
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)})


def payment_success_view(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    order = get_object_or_404(OrderDetail, strip_session_id=session.id)
    order.has_paid = True
    order.save()
    order.refresh_from_db()

    return render(request, 'myapp/payment_success.html', {"order": order})


def payment_failed_view(request):
    return render(request, 'myapp/payment_failed.html')


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.seller = request.user
            new_product.save()
            return redirect('index')
    form = ProductForm()
    return render(request, 'myapp/create_product.html', {'form': form})


def edit_product(request, id):
    product = Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')

    product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and product_form.is_valid():
        product_form.save()
        return redirect('index')
    return render(request, 'myapp/edit_product.html', {'form': product_form, 'id': id})


def delete_product(request, id):
    product = Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')
    if request.method == "POST":
        product.delete()
        return redirect('index')
    return render(request, 'myapp/delete_product.html', {'product': product})


def dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'myapp/dashboard.html', {'products': products})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            return redirect('index')

    form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})


def invalid(request):
    return render(request, 'myapp/invalid.html')


def my_purchases(request):
    orders = OrderDetail.objects.filter(customer_email=request.user.email)
    return render(request, 'myapp/purchases.html', {"orders": orders})
