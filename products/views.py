from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


from django.shortcuts import get_object_or_404, redirect
from .models import Product
from cart.models import Cart, CartItem

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get('cart_id')
    if cart_id:  # Verifica se há um carrinho na sessão
        cart = Cart.objects.get(id=cart_id)
    else:  # Se não houver, cria um novo carrinho
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1  # Se o item já existe, incrementa a quantidade
        cart_item.save()

    return redirect('product_list')  # Redireciona de volta para a lista de produtos após adicionar ao carrinho

from django.shortcuts import render

def view_cart(request):
    cart_id = request.session.get('cart_id')
    cart_items = []  # Inicialize com uma lista vazia
    context = {}  # Inicialize o contexto vazio

    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)

    context = {
        'cart_items': cart_items  # Adicione o carrinho e outros dados necessários
        # Adicione mais dados ao contexto, se necessário
    }
    return render(request, 'view_cart.html', context)