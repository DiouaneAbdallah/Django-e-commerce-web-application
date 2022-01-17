from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.models import *
from django.urls import reverse
from django.db.models import Max
from datetime import date, timedelta,datetime
#from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def mastersellersent(request):
    if request.GET.get('delete', 0) != 0:
        Message.objects.get(Id=request.GET.get('replyto')).delete()

    allmessages = Message.objects.filter(profile=Profile.objects.get(user=request.user)).order_by('-date_created')
    page = request.GET.get('page', 1)
    paginator = Paginator(allmessages, 10)
    msg = paginator.get_page(page)
    return render(request, 'masterseller/mailbox/sent.html' ,{'msg':msg})

def mastersellermailbox(request):
    if request.GET.get('delete', 0) != 0:
        Message.objects.get(Id=request.GET.get('replyto')).delete()
    allmessages = Message.objects.all().exclude(profile=Profile.objects.get(user=request.user)).order_by('-date_created')
    page = request.GET.get('page', 1)
    paginator = Paginator(allmessages, 10)
    msg = paginator.get_page(page)
    return render(request, 'masterseller/mailbox/mailbox.html' ,{'msg':msg})

def mastersellerdraft(request):
    allmessages = Message.objects.filter(draft=1,profile=Profile.objects.get(user=request.user)).order_by('-date_created')
    page = request.GET.get('page', 1)
    paginator = Paginator(allmessages, 10)
    msg = paginator.get_page(page)
    return render(request, 'masterseller/mailbox/mailbox.html' ,{'msg':msg})

def mastersellercompose(request):
    if request.method == 'POST':
        if request.POST.get("draftbtn"):
            sendto = request.POST.get('sendto')
            mailsubject = request.POST.get('mailsubject')
            content = request.POST.get('content')
            Message(profile=Profile.objects.get(user=request.user),content=content,subject=mailsubject,sendto=sendto,draft=1).save()
            redirect('mailbox/mastersellerdraft')
        subject = request.POST.get('mailsubject')
        content = request.POST.get('composetextarea')
        Message(profile=Profile.objects.get(user=User.objects.get(email = request.user.email)),content=content,subject=subject,sendto=request.POST.get('sendto')).save()

    if request.GET.get('forward', 0) != 0:
        forward = Message.objects.get(Id=request.GET.get('replyto'))
        return render(request, 'masterseller/mailbox/compose.html' ,{'forward':forward})

    if request.GET.get('replyto') is not None:
        replyto = Message.objects.get(Id=request.GET.get('replyto'))
        return render(request, 'masterseller/mailbox/compose.html' ,{'replyto':replyto})
    return render(request, 'masterseller/mailbox/compose.html' ,{})

def mastersellerread_mail(request):
    allmessages = Message.objects.all().exclude(profile=Profile.objects.get(user=request.user)).order_by('-date_created')
    toread      = Message.objects.get(Id=int(request.GET.get('lemessage')))
    toread.seen = 1
    toread.save()
    return render(request, 'masterseller/mailbox/read-mail.html' ,{'toread':toread})

def mastersellerdashboard(request):
	if request.user.is_authenticated:
		categories = Category.objects.all()
		products = Product.objects.filter(seller_id = Profile.objects.get(user=request.user))
		productnumbycategory = {}
		for category in categories:
			productnumbycategory[category]=len(Product.objects.filter(seller=Profile.objects.get(user=request.user),category=category))
		r=products.aggregate(Max('rating'))

		toprated = Product.objects.filter(seller=Profile.objects.get(user=request.user),rating=r['rating__max'])
		prodates = Product.objects.filter(seller=Profile.objects.get(user=request.user)).order_by('-date_created')

		return render(request, 'masterseller/dashboard.html' ,
            {
            'productnumbycategory':productnumbycategory,
            'toprated':toprated,
            'prodates':prodates[:4],
            'max_rating':Product.objects.filter(seller=Profile.objects.get(user=request.user)).aggregate(Max('rating'))['rating__max']})
	else:
		return render(request, 'masterseller/notallowed.html' ,{} )

def mastersellergenerallook(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    productnumbycategory = {}
    for category in categories:
        productnumbycategory[category]=len(Product.objects.filter(seller=Profile.objects.get(user=request.user),category=category))
    print(productnumbycategory)

    return render(request, 'masterseller/charts/generallook.html' ,{'productnumbycategory':productnumbycategory} )

def mastersellerviewproductsimple(request):
    products   = Product.objects.all()
    categories = Category.objects.all()
    productbycategory = []
    for category in categories:
        productbycategory.append(Product.objects.filter(seller=Profile.objects.get(user=request.user),category=category))

    print(productbycategory)
    return render(request, 'masterseller/tables/viewproductsimple.html' ,{'products':products,'categories':categories,'productbycategory':productbycategory})

def mastersellerviewproductdata(request):
    products = Product.objects.filter(seller=Profile.objects.get(user=request.user))
    return render(request, 'masterseller/tables/viewproductdata.html' ,{'products':products} )

def mastersellerrestockproduct(request):
    if request.method == 'POST':
        idname                    = request.POST.get('productidname')
        restock                   = request.POST.get('productrestock')
        productId                 = idname[0]
        product                   = Product.objects.get(Id=productId)

        archive                   = ProductArchives.objects.get(prodId=product.Id)
        archive.totalPiecesStock -= product.piecesStock

        product.piecesStock       = restock
        product.save()

        archive.totalPiecesStock  += restock
        #product.popularity         = (archive.purchases / archive.totalPiecesStock) * 100
        archive.save()
        return redirect('masterseller/forms/restockproduct')

    products = Product.objects.filter(seller=Profile.objects.get(user=request.user))
    return render(request, 'masterseller/forms/restockproduct.html' ,{'products':products} )

def mastersellerdeleteproduct(request):
    if request.method == 'POST':
        idname    = request.POST.get('productidname')
        productId = idname[0]
        product = Product.objects.get(Id=productId)
        product.delete()
        return redirect('masterseller/forms/deleteproduct')

    products = Product.objects.filter(seller=Profile.objects.get(user=request.user))
    return render(request, 'masterseller/forms/deleteproduct.html' ,{'products':products} )

def masterselleraddnewproduct(request):
    if request.method == 'POST':
        name           = request.POST.get('productname')
        description    = request.POST.get('productdescription')
        price          = float(request.POST.get('productprice'))
        images         = request.FILES.getlist('productimages')
        category       = request.POST.get('productcategory')
        features       = request.POST.get('productfeatures')
        manufacturer   = request.POST.get('productmanufacturer')
        piecesstock    = request.POST.get('productpiecesstock')
        keywords       = request.POST.get('productkeywords')

        product        = Product(name=name,description=description,price=price,category=Category.objects.get(name=category),features=features,manufacturer=manufacturer,piecesStock=piecesstock,keywords=keywords,seller=Profile.objects.get(user=request.user))

        if len(images) == 1:
            product.image  = images[0]
        elif len(images) == 2:
            product.image  = images[0]
            product.image2 = images[1]
        else:
            product.image  = images[0]
            product.image2 = images[1]
            product.image3 = images[2]

        product.save()

        archive = ProductArchives(prodId=product.Id,name=product.name,description=product.description,category=product.category.name,manufacturer=product.manufacturer,totalPiecesStock=product.piecesStock,purchases=product.purchases,raters=product.raters,seller=product.seller)
        print(archive)
        archive.save()
        return redirect('masterseller/forms/addnewproductform/')

    categories = Category.objects.all()
    return render(request, 'masterseller/forms/addnewproductform.html' ,{'categories':categories} )
