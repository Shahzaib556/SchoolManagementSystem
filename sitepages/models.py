from django.db import models


class SiteSettings(models.Model):
    """Singleton-style settings for the public site — contact info, socials, and bank details
    for donations. Edit from the Django Admin panel (Sitepages > Site settings)."""
    phone = models.CharField(max_length=50, default="+92 300 1234567")
    email = models.EmailField(default="info@roshanhunarmarkaz.edu.pk")
    address = models.CharField(max_length=255, default="Main Campus Road, Islamabad, Pakistan")
    facebook_url = models.URLField(blank=True, help_text="Full URL to the school's Facebook page")
    whatsapp_number = models.CharField(max_length=50, blank=True)

    bank_name = models.CharField(max_length=150, blank=True)
    account_title = models.CharField(max_length=150, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    iban = models.CharField(max_length=50, blank=True)
    branch_code = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj
