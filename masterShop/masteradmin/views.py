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
from django.db.models import F
from django.db.models import Count


def sent(request):
    if request.GET.get('delete', 0) != 0:
        Message.objects.get(Id=request.GET.get('replyto')).delete()

    if request.user.is_superuser:
        allmessages = Message.objects.filter(profile=Profile.objects.get(user=request.user)).order_by('-date_created')
        page = request.GET.get('page', 1)
        paginator = Paginator(allmessages, 10)
        msg = paginator.get_page(page)
    return render(request, 'masteradmin/mailbox/sent.html' ,{'msg':msg})

def mailbox(request):
    if request.GET.get('delete', 0) != 0:
        Message.objects.get(Id=request.GET.get('replyto')).delete()
    if request.user.is_superuser:
        allmessages = Message.objects.all().exclude(profile=Profile.objects.get(user=request.user)).order_by('-date_created')
        page = request.GET.get('page', 1)
        paginator = Paginator(allmessages, 10)
        msg = paginator.get_page(page)
    return render(request, 'masteradmin/mailbox/mailbox.html' ,{'msg':msg})

def draft(request):
    allmessages = Message.objects.filter(draft=1).exclude(sendto=request.user.email).order_by('-date_created')
    page = request.GET.get('page', 1)
    paginator = Paginator(allmessages, 10)
    msg = paginator.get_page(page)
    return render(request, 'masteradmin/mailbox/mailbox.html' ,{'msg':msg})

def compose(request):
    if request.method == 'POST':
        if request.POST.get("draftbtn"):
            sendto = request.POST.get('sendto')
            mailsubject = request.POST.get('mailsubject')
            content = request.POST.get('content')
            Message(profile=Profile.objects.get(user=request.user),content=content,subject=mailsubject,sendto=sendto,draft=1).save()
            redirect('mailbox/draft')
        subject = request.POST.get('mailsubject')
        content = request.POST.get('composetextarea')
        Message(profile=Profile.objects.get(user=User.objects.get(email = request.user.email)),content=content,subject=subject,sendto=request.POST.get('sendto')).save()

    if request.GET.get('forward', 0) != 0:
        forward = Message.objects.get(Id=request.GET.get('replyto'))
        return render(request, 'masteradmin/mailbox/compose.html' ,{'forward':forward})

    if request.GET.get('replyto') is not None:
        replyto = Message.objects.get(Id=request.GET.get('replyto'))
        return render(request, 'masteradmin/mailbox/compose.html' ,{'replyto':replyto})
    return render(request, 'masteradmin/mailbox/compose.html' ,{})

def read_mail(request):
    allmessages = Message.objects.all().exclude(profile=Profile.objects.get(user=request.user)).order_by('-date_created')
    toread      = Message.objects.get(Id=int(request.GET.get('lemessage')))
    toread.seen = 1
    toread.save()
    return render(request, 'masteradmin/mailbox/read-mail.html' ,{'toread':toread})

def viewuserssellers(request):
    if request.user.is_superuser:
        sellers  = Profile.objects.filter(is_seller=1)
        return render(request, 'masteradmin/tables/viewuserssellers.html' ,{'sellers':sellers})
    return render(request, 'masteradmin/notallowed.html' ,{})

def viewusersclients(request):
    if request.user.is_superuser:
        profiles = Profile.objects.all()
        return render(request, 'masteradmin/tables/viewusersclients.html' ,{'profiles':profiles} )
    return render(request, 'masteradmin/notallowed.html' ,{})

def orderS(request):
    order   = request.GET.get('order')
    status  = request.GET.get('status')
    ord = Order.objects.get(id=order)
    ord.status = status
    ord.save()
    return redirect('/dashboard')
def get_orders_products(request):
    Orders = {}
    for order in Order.objects.all():
        ProductsList = []
        for dico in OrderDict.objects.filter(order=order):
            ProductsList.append([Product.objects.filter(Id = dico.product),dico])
        Orders[order.id] = ProductsList
    return Orders

def dashboard(request):
    if request.user.is_superuser:
        categories = Category.objects.all()
        products = Product.objects.all()
        productnumbycategory = {}
        for category in categories:
            if category.name != 'Gaming':
                productnumbycategory[category]=len(Product.objects.filter(category=category))

        sales = 0
        for order in Order.objects.all():
            sales += order.total_price

        max_rating = Product.objects.all().aggregate(Max('rating'))['rating__max']
        max_views  = Product.objects.all().aggregate(Max('views'))['views__max']

        toprated = Product.objects.get(rating = max_rating)
        topviewed = Product.objects.get(views = max_views)

        profiles = Profile.objects.all().order_by('-user')
        prodates = Product.objects.all().order_by('-date_created')

        orders   = Order.objects.all()
        notifications = SellerNotification.objects.all()

        orderss = Order.objects.values('Order_date').annotate(idd=Count('id'))

        args = {'productnumbycategory' : productnumbycategory,
                'toprated'      : toprated,
                'profiles'      : profiles,
                'prodates'      : prodates[:4],
                'notifications' : notifications[:4],
                'topviewed'     : topviewed,
                'toprated'      : toprated,
                'max_views'     : max_views,
                'max_rating'    : max_rating,
                'sales'         : sales,
                'orders'        : orders,
                'orderss'       : orderss,
                'ordersProducts'  : get_orders_products(request)}
        return render(request, 'masteradmin/dashboard.html' ,args )
    return render(request, 'masteradmin/notallowed.html' ,{})

def viewproductsimple(request):
    products   = Product.objects.all()
    categories = Category.objects.all()
    productbycategory = []
    for category in categories:
        productbycategory.append(Product.objects.filter(category=category))

    Products_cat = {}
    for cat in Category.objects.all():
        if cat.name != 'Gaming':
            Products_cat[cat.name] = Product.objects.filter(category = cat)

    args = {'products'          :products,
            'categories'        :categories,
            'productbycategory' :Products_cat}

    return render(request, 'masteradmin/tables/viewproductsimple.html' ,args)

def viewproductdata(request):
    products = Product.objects.all()
    return render(request, 'masteradmin/tables/viewproductdata.html' ,{'products':products} )

def restockproduct(request):
    if request.method == 'POST':
        id                  = request.POST.get('product')
        restock             = request.POST.get('productrestock')
        product             = Product.objects.get(Id=id)
        product.piecesStock = restock
        product.save()

        return redirect('/forms/restockproduct')

    products = Product.objects.all()
    return render(request, 'masteradmin/forms/restockproduct.html' ,{'products':products} )

def deleteproduct(request):
    if request.method == 'POST':
        productId = request.POST.get('product')
        product = Product.objects.get(Id=productId)
        product.delete()
        return redirect('/forms/deleteproduct')

    products = Product.objects.all()
    return render(request, 'masteradmin/forms/deleteproduct.html' ,{'products':products} )


def makeseller(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            idname    = request.POST.get('useridname')
            userId = idname[0]
            profile = Profile.objects.get(Id=userId)
            profile.is_seller = 1
            profile.date_seller = datetime.now()
            profile.save()
            notification = SellerNotification.objects.get(profile=profile)
            notification.delete()
            return redirect('/forms/makeseller')

        notifications = SellerNotification.objects.all()
        return render(request, 'masteradmin/forms/makeseller.html' ,{'notifications':notifications} )
    return render(request, 'masteradmin/notallowed.html' ,{})

def viewcategorysimple(request):
    if request.user.is_superuser:
        categories = Category.objects.all()
        total = 0
        catlen = {}
        for category in categories:
            catlen[category] = len(Product.objects.filter(category=category))
            total += len(Product.objects.filter(category=category))
        args = {'categories':categories,
                'catlen':catlen,
                'total':total}
        return render(request, 'masteradmin/tables/viewcategorysimple.html' ,args )
    return render(request, 'masteradmin/notallowed.html' ,{})

def viewcategorydata(request):
    if request.user.is_superuser:
        categories = Category.objects.all()
        lencat     = []
        catlen = {}
        for category in categories:
            catlen[category] = len(Product.objects.filter(category=category))
            lencat.append(len(Product.objects.filter(category=category)))
        return render(request, 'masteradmin/tables/viewcategorydata.html' ,{'categories':categories,'catlen':catlen} )
    return render(request, 'masteradmin/notallowed.html' ,{})

def deletecategory(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            id    = request.POST.get('category')
            category = Category.objects.get(Id=id)
            category.delete()
            return redirect('/forms/deletecategory')

        categories = Category.objects.all()
        return render(request, 'masteradmin/forms/deletecategory.html' ,{'categories':categories} )
    return render(request, 'masteradmin/notallowed.html' ,{})

def addnewcategory(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            name     = request.POST.get('categoryname')
            ID       = int(Category.objects.all().aggregate(Max('Id'))['Id__max'])
            category = Category(Id=ID+1,name=name)
            category.save()
            if request.POST.get('ab') == 1:
                return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.href = "/forms/addnewproductform/";</script>')
            else:
                return render(request, 'masteradmin/forms/addnewcategoryform.html' ,{} )
        return render(request, 'masteradmin/forms/addnewcategoryform.html' ,{} )
    return render(request, 'masteradmin/notallowed.html' ,{})

def addnewproduct(request):
    if request.method == 'POST':
        name           = request.POST.get('productname')
        description    = request.POST.get('productdescription')
        details        = request.POST.get('productdetail')
        price          = float(request.POST.get('productprice'))
        oldprice       = float(request.POST.get('productoldprice'))
        images         = request.FILES.getlist('productimages')
        catego         = request.POST.getlist('productcategory')
        features       = request.POST.get('productfeatures')
        manufacturer   = request.POST.get('productmanufacturer')
        piecesstock    = request.POST.get('productpiecesstock')
        keywords       = request.POST.get('productkeywords')

        ID  = int(Product.objects.all().aggregate(Max('Id'))['Id__max'])

        product        = Product(Id=ID+1,name=name,description=description,details=details,price=price,old_price=oldprice,features=features,manufacturer=manufacturer,piecesStock=piecesstock,keywords=keywords,seller=Profile.objects.get(user=request.user))

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

        for cat in catego:
            product.category.add(Category.objects.get(name=cat))

        product.save()

        return redirect('/forms/addnewproductform/')

    categories = Category.objects.all()
    return render(request, 'masteradmin/forms/addnewproductform.html' ,{'categories':categories} )
