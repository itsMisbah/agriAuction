from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import register, login, logout, current_user, CropViewSet

app_name = 'api'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'crops', CropViewSet, basename='crop')

urlpatterns = [
    # Authentication
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/me/', current_user, name='current-user'),
    
    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='docs'),
    
    # Router URLs
    path('', include(router.urls)),
]