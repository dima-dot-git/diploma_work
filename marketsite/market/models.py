from django.db import models
from django.contrib.auth.models import User, AbstractUser



class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    country = models.CharField(max_length=50, verbose_name="Country")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Brand")
    model = models.CharField(max_length=100, verbose_name="Model")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    details = models.TextField(verbose_name="Details")
    specifications = models.TextField(verbose_name="Specifications")

    def __str__(self):
        return f"{self.brand.name} - {self.model} {self.category}"

    def get_model_name(self):
        return f"{self.__class__.__name__}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class PhotoProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod_img")
    photo = models.ImageField(upload_to="image_prod")


class ProductInStock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Product")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product}"

    class Meta:
        verbose_name = "Product In Stock"
        verbose_name_plural = "Products In Stock"


class Stock(models.Model):
    products = models.ManyToManyField(ProductInStock)

    def __str__(self):
        return f" Stock in {self.products} products"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class ProductInCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name="product")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product}"


class Cart(models.Model):
    products = models.ManyToManyField(ProductInCart, verbose_name="Products in cart", blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Customer")

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def total_price(self):
        total = sum(item.product.price * item.amount for item in self.products.all())
        return total

    def __str__(self):
        return f" Cart: #{self.id} - User: {self.customer}"


class Orders(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.cart.customer.username} - {self.date}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name="market_user")
    avatar = models.ImageField(upload_to="user_ava",blank=True,default="user_ava/user-avatar_0WPOaNi.png")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number", blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
