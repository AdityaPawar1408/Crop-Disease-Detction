# crop_detection/urls.py

from django.contrib import admin
from django.urls import path, include, re_path # CRITICAL: Import re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CRITICAL FIX: Include the Django i18n URL patterns
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    
    # Include your app's URLs (keep this path definition)
    path('', include('detector.urls')), 
]

# ONLY FOR DEVELOPMENT: Serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)