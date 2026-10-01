from .models import SiteSettings


def site_settings(request):
    """Makes `site_settings` available in every template (footer contact info, etc.)."""
    return {"site_settings": SiteSettings.get_solo()}
