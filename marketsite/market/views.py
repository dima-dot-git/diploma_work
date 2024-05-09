from django.contrib.auth import logout, login
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from .forms import RegUserForm, SubscribeForm, ProfileForm, SetAvaForm, UserForm
from .models import Category, Product, PhotoProduct, User, Profile
from django.contrib.auth.decorators import login_required
from .models import Cart, ProductInCart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class MyLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'))


def get_info(request):
    profile = Profile(request.user)
    context = {"profile": profile}
    return render(request, "market/base.html", context)


def index(request):
    products = Product.objects.all().order_by("id")
    all_categories = Category.objects.all()
    photo = PhotoProduct.objects.all()
    cart = get_customer_cart(request)

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {"cart": cart, "products": products, "all_categories": all_categories, "photo": photo}
    return render(request, "market/index.html", context)


def categories(request, cat_id):
    cat = get_object_or_404(Category, id=cat_id)
    all_categories = Category.objects.all()
    photo = PhotoProduct.objects.all()
    products = Product.objects.filter(category__exact=cat).order_by("id")
    cart = get_customer_cart(request)

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {"products": products, "photo": photo, "cart": cart, "all_categories": all_categories}
    return render(request, 'market/index.html', context)


def about_us(request):
    cart = get_customer_cart(request)
    context = {"cart": cart}
    return render(request, "market/about-us.html", context)


def typography(request):
    cart = get_customer_cart(request)
    context = {"cart": cart}
    return render(request, 'market/typography.html', context)


def contact_us(request):
    cart = get_customer_cart(request)
    context = {"cart": cart}
    return render(request, 'market/contact-us.html', context)


def in_cart(request):
    cart = get_customer_cart(request)

    if request.method == "POST":
        select_product = get_object_or_404(ProductInCart, pk=request.POST.get("product_pk"))
        quantity = request.POST.get("quantity")
        select_product.amount = quantity
        select_product.save()
        return redirect("go_to_cart")
    context = {"cart": cart}
    return render(request, 'market/cart.html', context)


def add_to_cart(request, prod_pk):
    product = get_object_or_404(Product, pk=prod_pk)
    cart = get_customer_cart(request)
    if request.method == "POST":
        product_in_cart, created = ProductInCart.objects.get_or_create(cart=cart, product=product)
        if created:
            product_in_cart = ProductInCart(product=product, amount=1)
            product_in_cart.save()
            cart.products.add(product_in_cart)

    return redirect("index")


def del_of_cart(request, prod_pk):
    if request.method == 'POST':
        product_in_cart = get_object_or_404(ProductInCart, pk=prod_pk)
        product_in_cart.delete()
        return redirect('index')
    else:
        return redirect('index')


@login_required
def get_customer_cart(request):
    customer_cart = Cart.objects.filter(customer=request.user).first()
    if not customer_cart:
        customer_cart = Cart.objects.create(customer=request.user)
    return customer_cart


def registry_customer(request):
    if request.method == "POST":
        new_customer_form = RegUserForm(request.POST)
        if new_customer_form.is_valid():
            new_customer = new_customer_form.save()
            new_customer.save()
            profile = Profile.objects.create(user=new_customer)
            profile.save()
            login(request, new_customer)
            return redirect('index')
    else:
        new_customer_form = RegUserForm()
    context = {"new_customer_form": new_customer_form}
    return render(request, "market/registry_customer.html", context)


def product(request, prod_pk=None):
    cart = get_customer_cart(request)
    select_prod = get_object_or_404(Product, pk=prod_pk)
    select_prod_in_cart = cart.products.filter(product=select_prod)
    product_in_cart = []
    for item in cart.products.all():
        product_in_cart.append(item.product)
    context = {"cart": cart, "select_prod": select_prod, 'product_in_cart': product_in_cart,
               "select_prod_in_cart": select_prod_in_cart}
    return render(request, "market/product.html", context)


def go_to_cart(request):
    cart = get_customer_cart(request)
    context = {"cart": cart}
    return render(request, "market/go_to_cart.html", context)


def search(request):
    query = request.GET.get("search")
    cart = get_customer_cart(request)
    products = Product.objects.filter(
        Q(model__icontains=query) | Q(brand__name__icontains=query) | Q(category__name__icontains=query))
    context = {"products": products, "cart": cart}
    return render(request, 'market/index.html', context)


def subscribe(request):
    if request.method == "POST":
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
    return redirect("index")


def edit_profile(request, profile_pk):
    profile = get_object_or_404(Profile, pk=profile_pk)
    user = get_object_or_404(User, pk=profile_pk)
    if request.method == 'POST':
        change_profile_form = ProfileForm(request.POST, instance=profile)
        user_form = UserForm(request.POST, instance=user)
        set_ava_form = SetAvaForm(request.POST, request.FILES, instance=profile)
        if change_profile_form.is_valid() and user_form.is_valid() and set_ava_form.is_valid():
            change_profile_form.save()
            user_form.save()
            set_ava_form.save()
            return redirect("index")
    else:
        change_profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=user)
        set_ava_form = SetAvaForm(instance=profile)
    context = {"change_profile_form": change_profile_form, "user_form": user_form, "set_ava_form": set_ava_form}
    return render(request, "market/edit_profile.html", context)
