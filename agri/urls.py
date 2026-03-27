from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('crops/', include('crops.urls')),
    path('api/', include('api.urls')),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]

# Only add this when DEBUG is True (during development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)