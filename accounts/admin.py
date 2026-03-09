from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'role', 'is_staff']
    search_fields = ['username', 'email']
    list_filter = ['role']
    fieldsets = [
        ("Role", {
            "fields": ["role"],
        }),
        ("Additional Information", {
            "fields": ["bio", "profile_picture"],
        }),
        ("Updated At", {
            "fields": ["updated_at"],
        }),
    ]
    readonly_fields = ['updated_at']

admin.site.register(User, CustomUserAdmin)