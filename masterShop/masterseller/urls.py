from django.conf.urls import url
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    url(r'^forms/masterselleraddnewproductform/$', views.masterselleraddnewproduct),
    url(r'^forms/mastersellerdeleteproduct/$', views.mastersellerdeleteproduct),
    url(r'^forms/mastersellerrestockproduct/$', views.mastersellerrestockproduct),

    url(r'^tables/mastersellerviewproductdata/$', views.mastersellerviewproductdata),
    url(r'^tables/mastersellerviewproductsimple/$', views.mastersellerviewproductsimple),

    url(r'^charts/mastersellergenerallook/$', views.mastersellergenerallook),

    url(r'^mastersellerdashboard/$', views.mastersellerdashboard),

    url(r'^mailbox/mastersellermailbox/$', views.mastersellermailbox),
    url(r'^mailbox/mastersellercompose/$', views.mastersellercompose),
    url(r'^mailbox/mastersellerread-mail/$', views.mastersellerread_mail),
    url(r'^mailbox/mastersellersent/$', views.mastersellersent),
    url(r'^mailbox/mastersellerdraft/$', views.mastersellerdraft),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
