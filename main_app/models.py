from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)  # e.g., Mens, Womens, Kids
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Watch(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='watches')
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='watch_images/', blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.brand})"
    

