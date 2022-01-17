from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date,datetime
from django.db.models import F
from django.template import RequestContext
"""
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
"""
def home_page(request):
    Products_cat = {}
    for cat in Category.objects.all():
        Products_cat[cat.Id] = Product.objects.filter(category = cat)

    args = {'Products_cat' : Products_cat,
            'products':Product.objects.all().order_by('-date_created'),
            'rand_products':Product.objects.all().order_by('?')}
    return render(request, 'shop/index.html', args)

def register(request):

    if request.method == 'POST':
        first_name      = request.POST.get('firstName')
        last_name       = request.POST.get('lastName')
        email           = request.POST.get('email')
        country         = request.POST.get('country')
        address         = request.POST.get('address')
        password        = request.POST.get('password')
        username        = request.POST.get('username')
        birth_date      = request.POST.get('birth_date')
        profilePic      = request.FILES.get('profilePic')
        user            = User.objects.create_user(username,email,password)
        user.first_name = first_name
        user.last_name  = last_name
        user.save()
        pf              = Profile(profilePic= profilePic,
                                  address   = address,
                                  country   = country,
                                  birth_date= birth_date)
        pf.user         = user
        pf.save()
        return redirect('/')
    return render(request, 'shop/register.html')

def signin(request):
    error = False
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
        if user:  # Si l'objet renvoyé n'est pas None
            login(request, user)  # nous connectons l'utilisateur
            return redirect('/')
        else: # sinon une erreur sera affichée
            return render(request, 'shop/index.html', {'error0':'upi'})
    else:
        return render(request, 'shop/register.html')

    #return render(request, 'shop/register.html', {'error0':'upi'})

def signout(request):
    logout(request)
    #redirect(reverse(signin))
    return redirect('/')

@login_required
def editprofile(request):
    if request.method == 'POST':
        username    = request.POST.get('username')
        password    = request.POST.get('password')
        firstname   = request.POST.get('firstName')
        lastname    = request.POST.get('lastName')
        email       = request.POST.get('email')
        address     = request.POST.get('address')
        country     = request.POST.get('country')
        profilePic  = request.FILES.get('profilePic')
        #sprofilePic = 'images/'+str(profilePic)
        birth_date  = request.POST.get('birth_date')

        user = request.user

        user.first_name = firstname
        user.last_name  = lastname
        user.save()

        profile = Profile.objects.get(user=request.user)
        profile.address = address
        profile.country = country
        profile.birth_date = birth_date
        profile.profilePic = profilePic
        profile.save()

        return redirect('/myaccount')
    return redirect('/myaccount')

def ProductsDates(list):
    Diff={}
    for prod in list:
        date_format = "%Y-%m-%d"
        new_dt = str(prod.date_created)[:19]
        a = datetime.strptime(str(datetime.now().date()), date_format)
        b = datetime.strptime(new_dt, "%Y-%m-%d %H:%M:%S")
        delta = b - a
        Diff[prod.Id] = abs(delta.days)
    return Diff

def product_detail(request):
    prodId = int(request.GET.get('prod'))
    Product.objects.filter(Id=prodId).update(views = F('views')+1)
    prod = Product.objects.get(Id=prodId)
    L = prod.features.split('|')
    if L[0] == '':
        L = None

    date_format = "%Y-%m-%d"
    new_dt = str(prod.date_created)[:19]
    a = datetime.strptime(str(datetime.now().date()), date_format)
    b = datetime.strptime(new_dt, "%Y-%m-%d %H:%M:%S")
    delta = b - a

    ids = prod.category.all()


    args = {'prod' : prod ,
            'feat' : L ,
            'today': abs(delta.days) ,
            'produits' : Product.objects.filter( category__in = ids ).exclude(Id = prodId)}

    if request.user.is_authenticated:
        reviews = []
        for rev in Review.objects.filter(product = prodId):
            reviews.append(rev)
        args['reviews'] = reviews

    return render(request, 'shop/product-detail.html' ,args )

def products(request):

    if request.method == 'GET':
        if 'cat' in request.GET:
            catId = request.GET.get('cat')
            if 'manu' in request.GET:
                manu = request.GET.get('manu')
                if 'sort' in request.GET:
                    sort = str(request.GET.get('sort'))
                    if 'min' in request.GET:
                        min = str(request.GET.get('min'))
                        max = str(request.GET.get('max'))
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,price__range=(min,max),category = catId, manufacturer = manu).order_by(sort)
                        else:
                            Products_list = Product.objects.filter(price__range=(min,max),category = catId, manufacturer = manu).order_by(sort)
                    else:
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,category = catId, manufacturer = manu).order_by(sort)
                        else:
                            Products_list = Product.objects.filter(category = catId, manufacturer = manu).order_by(sort)
                else:
                    if 'min' in request.GET:
                        min = str(request.GET.get('min'))
                        max = str(request.GET.get('max'))
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,price__range=(min,max),category = catId, manufacturer = manu)
                        else:
                            Products_list = Product.objects.filter(price__range=(min,max),category = catId, manufacturer = manu)
                    else:
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,category = catId, manufacturer = manu)
                        else:
                            Products_list = Product.objects.filter(category = catId, manufacturer = manu)
            else:
                if 'sort' in request.GET:
                    sort = str(request.GET.get('sort'))
                    if 'min' in request.GET:
                        min = str(request.GET.get('min'))
                        max = str(request.GET.get('max'))
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,price__range=(min,max),category = catId).order_by(sort)
                        else:
                            Products_list = Product.objects.filter(price__range=(min,max),category = catId).order_by(sort)
                    else:
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,category = catId).order_by(sort)
                        else:
                            Products_list = Product.objects.filter(category = catId).order_by(sort)
                else:
                    if 'min' in request.GET:
                        min = str(request.GET.get('min'))
                        max = str(request.GET.get('max'))
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,price__range=(min,max),category = catId)
                        else:
                            Products_list = Product.objects.filter(price__range=(min,max),category = catId)
                    else:
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,category = catId)
                        else:
                            Products_list = Product.objects.filter(category = catId)
        else:
            if 'manu' not in request.GET:
                if 'sort' in request.GET:
                    sort = str(request.GET.get('sort'))
                    if 'min' in request.GET:
                        min = str(request.GET.get('min'))
                        max = str(request.GET.get('max'))
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,price__range=(min,max)).order_by(sort)
                        else:
                            Products_list = Product.objects.filter(price__range=(min,max)).order_by(sort)
                    else:
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key).order_by(sort)
                        else:
                            Products_list = Product.objects.all().order_by(sort)
                else:
                    if 'min' in request.GET:
                        min = str(request.GET.get('min'))
                        max = str(request.GET.get('max'))
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,price__range=(min,max))
                        else:
                            Products_list = Product.objects.filter(price__range=(min,max))
                    else:
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key)
                        else:
                            Products_list = Product.objects.all()
            else:
                manu = request.GET.get('manu')
                if 'sort' in request.GET:
                    sort = str(request.GET.get('sort'))
                    if 'min' in request.GET:
                        min = str(request.GET.get('min'))
                        max = str(request.GET.get('max'))
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,price__range=(min,max),manufacturer = manu).order_by(sort)
                        else:
                            Products_list = Product.objects.filter(price__range=(min,max),manufacturer = manu).order_by(sort)
                    else:
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,manufacturer = manu).order_by(sort)
                        else:
                            Products_list = Product.objects.filter(manufacturer = manu).order_by(sort)
                else:
                    if 'min' in request.GET:
                        min = str(request.GET.get('min'))
                        max = str(request.GET.get('max'))
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,price__range=(min,max),manufacturer = manu)
                        else:
                            Products_list = Product.objects.filter(price__range=(min,max),manufacturer = manu)
                    else:
                        if 'key' in request.GET:
                            key = str(request.GET.get('key'))
                            Products_list = Product.objects.filter(keywords__icontains = key,manufacturer = manu)
                        else:
                            Products_list = Product.objects.filter(manufacturer = manu)
        page = request.GET.get('page', 1)
        paginator = Paginator(Products_list, 12)
        try:
            Products = paginator.page(page)
        except PageNotAnInteger:
            Products = paginator.page(1)
        except EmptyPage:
            Products = paginator.page(paginator.num_pages)

        brands = set()
        for proda in Product.objects.all():
            brands.add(proda.manufacturer)

        args = {'produits'   : Products,
                'brands'     : list(brands),
                'topProducts': Product.objects.all().order_by('-rating')[:4]}


        return render(request, 'shop/products.html' ,args )
    else:
        return render(request, 'shop/products.html' ,args )

def search(request):
    categ = str(request.GET.get('categ'))
    key   = request.GET.get('key')
    if key == '':
        if categ == '0':
            url = '/products'
        else:
            url = '/products?cat={}'.format(categ)
    else:
        if categ == '0':
            url = '/products?key={}'.format(key)
        else:
            url = '/products?cat={}&key={}'.format(categ, key)
    return redirect(url)

@login_required
def cart(request):
    return render(request, 'shop/cart.html')

@login_required
def add_to_cart(request):
    product = request.GET.get('prod')
    nbr = int(request.GET.get('num', '1'))
    feature = request.GET.get('feature', 'nothing')

    try:
        cart = Cart.objects.get(profile=Profile.objects.get(user = request.user))
    except Cart.DoesNotExist:
        cart = Cart(profile=Profile.objects.get(user = request.user))
        cart.save()
    piecesStock = getattr(Product.objects.get(Id = product), 'piecesStock')
    if nbr <= piecesStock:
        try:
            dico = Dictio.objects.get(product = product,cart=cart)
            dico.quantity += nbr
            dico.save()
        except Dictio.DoesNotExist:
            Dictio(product  = product,
                   cart     = cart,
                   quantity = nbr,
                   feature  = feature).save()
        Product.objects.filter(Id = product).update(piecesStock = piecesStock-nbr)
    elif piecesStock > 0:
        try:
            dico = Dictio.objects.get(product=Product.objects.get(Id = product) ,cart=cart)
            dico.quantity += piecesStock
            dico.save()
        except Dictio.DoesNotExist:
            Dictio(product=Product.objects.get(Id = product),
                  cart=cart,
                  quantity=piecesStock,
                  feature  = feature).save()
        Product.objects.filter(Id = product).update(piecesStock = 0)

    return redirect('/cart')

@login_required
def update_cart(request):
    p = request.GET.getlist('prods[]')
    q = request.GET.getlist('quans[]')

    cart = Cart.objects.get(profile=Profile.objects.get(user = request.user))

    for i,j in zip(p,q):
        j=int(j)
        i=int(i)
        piecesStock = getattr(Product.objects.get(Id = i), 'piecesStock')
        quantity    = getattr(Dictio.objects.get(product= i ,cart=cart), 'quantity')

        if j > quantity:
            if j <= piecesStock:
                Dictio.objects.filter(product= i ,cart=cart).update(quantity = j)
                Product.objects.filter(Id = i).update(piecesStock = piecesStock - (j-quantity))
            elif piecesStock != 0:
                Dictio.objects.filter(product= i ,cart=cart).update(quantity = piecesStock)
                Product.objects.filter(Id = i).update(piecesStock = 0)
        elif j < quantity:
             Dictio.objects.filter(product= i ,cart=cart).update(quantity = j)
             Product.objects.filter(Id = i).update(piecesStock = piecesStock + (quantity-j))
    return redirect('/cart')

@login_required
def delete_product(request):
    product = int(request.GET.get('prod'))

    cart = Cart.objects.get(profile=Profile.objects.get(user = request.user))

    piecesStock = getattr( Product.objects.get(Id = product), 'piecesStock')
    quantity    = getattr( Dictio.objects.get(product = product ,cart=cart), 'quantity')
    Product.objects.filter(Id = product).update(piecesStock = piecesStock+quantity)

    dico = Dictio.objects.filter(product= product ,cart=cart).delete()

    return redirect('/cart')

@login_required
def checkout(request):
    args = {'ship_meth' : ShippingMethod.objects.all()}
    return render(request, 'shop/checkout.html',args)

@login_required
def order_received(request):
    shipping = request.GET.get('shipping')
    payments = request.GET.get('payments')
    total    = request.GET.get('total')

    cart = Cart.objects.get(profile = Profile.objects.get(user = request.user))

    order = Order(profile     = Profile.objects.get(user = request.user),
                  payment     = payments,
                  total_price = float(total),
                  shipping    = shipping)
    order.save()

    for dico in Dictio.objects.filter(cart = cart):
        OrderDict(product  = dico.product, quantity = dico.quantity,
                  feature  = dico.feature, order    = order).save()

    Dictio.objects.filter(cart=cart).delete()
    ordersProducts = []
    for dico in OrderDict.objects.filter(order = order):
        ordersProducts.append([Product.objects.filter(Id = dico.product),dico])

    args = {'OrderDictio': ordersProducts,
            'order'      : order}
    return render(request, 'shop/order-received.html',args)

def contact(request):
    if request.method == 'POST':
        tosend  = request.POST.get('message')
        subject = request.POST.get('subject')
        if request.user.is_authenticated:
            full_name = request.user.first_name + ' ' +request.user.last_name
            message = Message(fullname=full_name, email=request.user.email, subject=subject, content=tosend, profile=Profile.objects.get(user=request.user))
        else:
            fullname          = request.POST.get('fullName')
            email             = request.POST.get('email')
            message           = Message(fullname=fullname,email=email,content=tosend)

        message.save()
        return redirect('/')
    return render(request, 'shop/contact.html')

def get_orders_products(request):
    Orders = {}
    for order in Order.objects.filter(profile = Profile.objects.get(user = request.user)):
        ProductsList = []
        for dico in OrderDict.objects.filter(order=order):
            ProductsList.append([Product.objects.filter(Id = dico.product),dico])
        Orders[order.id] = ProductsList
    return Orders

@login_required
def myAccount(request):
    wishlistProducts = []
    for wish in Wishlist.objects.filter(profile = Profile.objects.get(user = request.user)):
        wishlistProducts.append(wish.product)
    args = {'wishlistProducts': wishlistProducts,
            'orders'          : Order.objects.filter(profile = Profile.objects.get(user = request.user)),
            'ordersProducts'  : get_orders_products(request)}
    return render(request, 'shop/myaccount.html',args)

def page_not_found(request):
    return render(request, 'shop/404.html')

def send_message(request):
    full_name   = request.GET.get('full_name')
    email       = request.GET.get('email')
    message     = request.GET.get('message')
    Message(full_name   = full_name,
            email       = email,
            message     = message).save()
    return redirect('/')

def add_review(request):
    review  = request.GET.get('review')
    rating  = int(request.GET.get('rating'))
    product = request.GET.get('product')
    Product.objects.filter(Id = product).update(raters = F('raters')+1)
    Product.objects.filter(Id = product).update(rate   = F('rate')+rating)
    Product.objects.filter(Id = product).update(rating = F('rate')/F('raters'))
    Review( review  = review,
            rating  = rating,
            product = Product.objects.get(Id   = product),
            profile = Profile.objects.get(user = request.user)).save()
    return redirect('/product_detail?prod={}'.format(product))

@login_required
def add_to_wishlist(request):
    product = request.GET.get('prod')
    for wish in Wishlist.objects.filter(profile = Profile.objects.get(user = request.user)):
        if wish.id != product :
            Wishlist( product = Product.objects.get(Id   = product),
                    profile = Profile.objects.get(user = request.user)).save()
    return redirect('/')

@login_required
def remove_from_wishlist(request):
    product = request.GET.get('prod')
    Wishlist.objects.filter(product= product, profile = Profile.objects.get(user = request.user)).delete()
    return redirect('/myaccount')

def about_us(request):
    return render(request, 'shop/about.html')

def shipping(request):
    return render(request, 'shop/shipping.html')

def faq(request):
    return render(request, 'shop/faq.html')

def become_a_seller(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        sn = SellerNotification(profile=Profile.objects.get(user=request.user))
        sn.save()
        return redirect('/')
    return render(request, 'shop/become-a-seller.html')
