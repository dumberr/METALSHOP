from django.conf import settings

from .models import Colectie


def procesare(request):
    return {
        "firma": settings.DATE_FIRMA,
        "copyright": "© 2026 Metalshop. Toate drepturile rezervate.",
        "categorii_meniu": Colectie.objects.filter(albume__isnull=False).distinct()
    }