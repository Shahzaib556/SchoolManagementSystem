from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contact Info", {"fields": ("phone", "email", "address", "facebook_url", "whatsapp_number")}),
        ("Bank Details (for donations)", {"fields": ("bank_name", "account_title", "account_number", "iban", "branch_code")}),
    )

    def has_add_permission(self, request):
        # Keep this a singleton — only allow adding if none exists yet
        return not SiteSettings.objects.exists()
