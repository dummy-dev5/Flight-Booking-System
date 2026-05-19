"""
URL configuration for fbs_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('fbs_instructor.urls')),
    path('api/', include('app.urls')),
    path('flightapp/', include('flightapp.urls')),
    
    #djoser
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/token-auth/', obtain_auth_token),
]

# Serve media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# POST /api/auth/users/ (register)
# POST /api/auth/token/login/ (Login)
# POST /api/auth/token/logout/ (logout)
# GET /api/auth/users/me/ (currnt user) builtin


# ==========================================
# AUTOMATIC SUPERUSER CREATION ON STARTUP
# ==========================================
try:
    from django.contrib.auth import get_user_model
    from decouple import config
    User = get_user_model()
    
    # Strictly load from environment variables with no hardcoded fallback secrets
    SU_USERNAME = config('SUPERUSER_USERNAME', default=None)
    SU_EMAIL = config('SUPERUSER_EMAIL', default=None)
    SU_PASSWORD = config('SUPERUSER_PASSWORD', default=None)
    
    if SU_USERNAME and SU_PASSWORD:
        if not User.objects.filter(username=SU_USERNAME).exists():
            User.objects.create_superuser(
                username=SU_USERNAME,
                email=SU_EMAIL or 'admin@example.com',
                password=SU_PASSWORD
            )
            print(f"--- AUTOMATIC SUPERUSER CREATION SUCCESSFUL: {SU_USERNAME} ---")
        else:
            print(f"--- Superuser '{SU_USERNAME}' already exists ---")
    else:
        print("--- Automatic superuser creation skipped: SUPERUSER_USERNAME or SUPERUSER_PASSWORD not set in environment variables ---")
except Exception as e:
    print(f"--- Automatic superuser creation skipped: {e} ---")



