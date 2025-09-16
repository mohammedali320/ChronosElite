from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)  # e.g., Mens, Womens, Kids
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Watch(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='watches')
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='watch_images/', blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.brand})"
    
    def get_absolute_url(self):
        # Redirect to this watch's detail page
        return reverse("watch_detail", args=[str(self.id)])

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Each user has one cart

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    watch = models.ForeignKey('Watch', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.watch.name}"

    def total_price(self):
        return self.watch.price * self.quantity