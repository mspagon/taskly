"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Future proofing for language translation.
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for user."""
    ordering = ['id']
    list_display = ['email', 'name', 'last_login']
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        """Custom logic for modifications made in admin page."""
        super().save_model(request, obj, form, change)


admin.site.register(models.User, UserAdmin)


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    ordering = ['date_created']
    list_display = ['title', 'date_created', 'date_due', 'id', 'is_completed']
    readonly_fields = ['user', 'date_created']
    list_filter = ('is_completed', 'date_created', 'date_completed', 'date_due')
    fields = ('title', 'description', 'date_created', 'date_due', 'date_completed', 'is_completed', 'user')
