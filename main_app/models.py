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
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='watch_images/', blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.brand})"
    
    def get_absolute_url(self):
        # Redirect to this watch's detail page
        return reverse("watch_detail", args=[str(self.id)])

