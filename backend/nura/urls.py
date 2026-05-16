from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
import os

frontend_dir = os.path.join(settings.BASE_DIR.parent, 'frontend')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    
    # Sirve el index.html en la raiz
    path('', serve, kwargs={'path': 'index.html', 'document_root': frontend_dir}),
    # Sirve el resto de los archivos estaticos del frontend (css, js, views)
    re_path(r'^(?P<path>.*)$', serve, kwargs={'document_root': frontend_dir}),
]
