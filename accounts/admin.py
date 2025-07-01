from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models.users import User
from .models.profiles import Profile



# --- Inline Profile ---
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ('slug', 'created_at', 'updated_at')


# --- Custom User Forms ---
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "role")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "role", "is_active", "is_staff", "verified", "is_online")


# --- Custom User Admin ---
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    inlines = (ProfileInline,) 

    list_display = ("id", "email", "role", "is_active", "is_staff", "verified", "is_online")
    list_filter = ("role", "is_staff", "verified", "is_active", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Status", {"fields": ("verified", "is_online")}),
        ("Role", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "role", "password1", "password2", "is_active", "is_staff", "is_superuser")}
         ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# --- Profile Admin ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "slug", "created_at")
    search_fields = ("user__email", "full_name", "slug")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

