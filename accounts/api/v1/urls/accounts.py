from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .. import views

urlpatterns = [
    # register
    # registration
    path(
        "registration/",
        views.RegistrationApiView.as_view(),
        name="registration",
    ),
    # activation
    path(
        "activation/confirm/<str:token>/",
        views.ActivationAPIView.as_view(),
        name="activation-confirm",
    ),

    # reset password

    path(
        "activation/resend/",
        views.ActivationResendAPIView.as_view(),
        name="activation-resend",
    ),

    # login with jwt

    path("jwt/token/create/",
         views.CustomTokenObtainPairView.as_view(), name="jwt-token"),
    path("jwt/token/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/token/verify/", TokenVerifyView.as_view(), name="jwt-verify"),

    # change password
    path(
        "changepassword/", views.ChangePasswordAPIView.as_view(), name="change-password"
    ),



]
