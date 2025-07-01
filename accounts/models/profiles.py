from django.db import models
from django.utils.text import slugify


class Profile(models.Model):

    slug = models.SlugField(unique=True)
    user = models.OneToOneField(
        'accounts.User', on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=1000)
    bio = models.TextField()
    image = models.ImageField(
        upload_to='profile_images/', null=True, blank=True)
    
    is_premium = models.BooleanField(default=False)
    premium_expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Profile of {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Automatically generate slug from full_name
            base_slug = slugify(self.full_name)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            while Profile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    @property
    def user_comments(self):
        """Access comments via user model."""
        return self.user.user_comments
    
    @property
    def user_posts(self):
        return self.user.posts
    