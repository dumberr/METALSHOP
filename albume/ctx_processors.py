from django.conf import settings


def procesare(request):
    return {
        "firma": settings.DATE_FIRMA,
        "copyright": "© 2026 Metalshop. Toate drepturile rezervate."
    }