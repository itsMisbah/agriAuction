from django.urls import path
from . import views

urlpatterns = [
    path('get-role/', views.get_role, name='get_role'),
    path('select-role/', views.select_role, name='select_role'),
    # path('signup/', views.signup_view, name='signup'),
]
