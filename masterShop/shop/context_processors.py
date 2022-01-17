from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date,datetime
from django.db.models import F
from django.template import RequestContext

def get_cart_products(request):
    try:
        cart = Cart.objects.get(profile=Profile.objects.get(user = request.user))
    except Cart.DoesNotExist:
        cart = Cart(profile=Profile.objects.get(user = request.user))
    ProductsList = []
    for dico in Dictio.objects.filter(cart=cart):
        ProductsList.append([Product.objects.filter(Id=dico.product),dico])
    return ProductsList

def page(request):
    args = {'categories' : Category.objects.all()}
    if request.user.is_authenticated:
        args['dictios'] = get_cart_products(request)
        args['profile'] = Profile.objects.get(user = request.user)
    return args
