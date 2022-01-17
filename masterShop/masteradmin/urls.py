from django.conf.urls import url
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('product', views.product),
    url(r'^forms/addnewcategoryform/$', views.addnewcategory),
    url(r'^forms/deletecategory/$', views.deletecategory),
    url(r'^forms/addnewproductform/$', views.addnewproduct),
    url(r'^forms/deleteproduct/$', views.deleteproduct),
    url(r'^forms/restockproduct/$', views.restockproduct),

    url(r'^tables/viewproductdata/$', views.viewproductdata),
    url(r'^tables/viewproductsimple/$', views.viewproductsimple),

    url(r'^tables/viewcategorydata/$', views.viewcategorydata),
    url(r'^tables/viewcategorysimple/$', views.viewcategorysimple),

    #url(r'^$', views.dashboardv1),
    url(r'^dashboard/$', views.dashboard),

    url(r'^tables/viewusersclients/$', views.viewusersclients),
    url(r'^tables/viewuserssellers/$', views.viewuserssellers),

    url(r'^forms/makeseller/$', views.makeseller),
    url(r'^forms/orderS/$', views.orderS),

    url(r'^mailbox/mailbox/$', views.mailbox),
    url(r'^mailbox/sent/$', views.sent),
    url(r'^mailbox/draft/$', views.draft),
    url(r'^mailbox/compose/$', views.compose),
    url(r'^mailbox/read-mail/$', views.read_mail),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
