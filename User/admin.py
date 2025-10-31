# User/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for our email-based User model
    """
    
    # List view (what you see in the main grid)
    list_display = ('email', 'name', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'name')
    ordering = ('-date_joined',)
    
    # Form fields (what you see when adding/editing)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields shown when adding NEW user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    
    # Autocomplete for large user lists
    autocomplete_fields = ('groups',)
    
    # Don't show these fields in list view (they take space)
    exclude = ('username',)  # Our username=None field
    
    # Better UX
    list_per_page = 50
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).only(
            'email', 'name', 'is_staff', 'is_active', 
            'is_superuser', 'date_joined', 'last_login'
        )


# BONUS: Register UserManager (for debugging)
class UserManagerAdmin(admin.ModelAdmin):
    """Optional: View manager stats"""
    list_display = ('__str__',)
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

# Don't register manager - just for reference