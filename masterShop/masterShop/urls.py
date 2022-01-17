from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url,handler404,handler500
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('', include('masteradmin.urls')),
    path('', include('masterseller.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#handler404 = 'shop.views.page_not_found'
#handler500 = 'shop.views.page_not_found'
