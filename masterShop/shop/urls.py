from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.home_page, name='index'),
    url(r'^product_detail/?$', views.product_detail, name='voir_produits'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^products/?$', views.products, name='products'),
    url(r'^signin/?$', views.signin, name='signin'),
    url(r'^editprofile/?$', views.editprofile, name='editprofile'),
    url(r'^add_to_cart/?$', views.add_to_cart, name='add_to_cart'),
    url(r'^delete_product/?$', views.delete_product, name='delete_product'),
    url(r'^logout/?$', views.signout, name='logout'),
    url(r'^cart/?$', views.cart, name='cart'),
    url(r'^search/?$', views.search, name='search'),
    url(r'^update_cart/?$', views.update_cart, name='update_cart'),
    url(r'^checkout/?$', views.checkout, name='chekout'),
    url(r'^order_received/?$', views.order_received, name='order_received'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^myaccount/$', views.myAccount, name='myaccount'),
    url(r'^add_review/?$', views.add_review, name='add_review'),
    url(r'^add_to_wishlist/?$', views.add_to_wishlist, name='add_to_wishlist'),
    url(r'^r_f_wl/?$', views.remove_from_wishlist, name='remove_from_wishlist'),
    url(r'^about_us/?$', views.about_us, name='about_us'),
    url(r'^shipping/?$', views.shipping, name='shipping'),
    url(r'^faq/?$', views.faq, name='faq'),
    url(r'^become_a_seller/?$', views.become_a_seller, name='become_a_seller'),
    url(r'^page_not_found/?$', views.page_not_found, name='page_not_found'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
