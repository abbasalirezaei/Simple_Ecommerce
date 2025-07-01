from django.urls import path, include


urlpatterns = [
    path('api/v1/', include('accounts.api.v1.urls')),
]
