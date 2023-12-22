import json
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
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
    request_data = json.load(request.body)
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

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

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session.payment_intent  # type: ignore
    order.amount = int(product.price)
    order.save()

    return JsonResponse({'sessionId': checkout_session.id})


def payment_success_view(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
    order.has_paid = True
    order.save()
    order.refresh_from_db()

    return render(request, 'myapp/payment_success.html', {"order": order})


def payment_failed_view(request):
    return render(request, 'myapp/payment_failed.html')
