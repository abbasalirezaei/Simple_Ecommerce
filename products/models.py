from django.db import models
from django.urls import reverse

# Category Model


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
# Product Model


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    main_image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={
            'id':self.pk,
            'slug': self.slug
        })
