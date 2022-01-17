from django.db import models
from django.contrib.auth.models import User

def get_superuser_email():
    return Profile.objects.get(Id=1).user.email

class Product(models.Model):
    Id          = models.AutoField(primary_key=True)
    date_created= models.DateTimeField(auto_now_add=True)
    name        = models.CharField(max_length=200)
    description = models.TextField()
    details     = models.TextField(default='details')
    price       = models.FloatField(max_length=200)
    old_price   = models.FloatField(max_length=200)
    category    = models.ManyToManyField('Category')
    features     = models.CharField(max_length=200 ,blank=True)
    manufacturer= models.CharField(max_length=200)
    image       = models.ImageField(upload_to='images/')
    image2      = models.ImageField(upload_to='images/', default='sample.jpg')
    image3      = models.ImageField(upload_to='images/', default='sample.jpg')
    piecesStock = models.IntegerField()
    purchases   = models.CharField(max_length=7, default='0', editable=False)
    raters      = models.IntegerField(default=0, editable=False)
    rate        = models.IntegerField(default=0, editable=False)
    rating      = models.FloatField(default=0, editable=False)
    views       = models.IntegerField(default=0, editable=False)
    keywords    = models.CharField(max_length=400, default='nothing')
    seller      = models.ForeignKey('Profile',on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Category(models.Model):
    Id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=100)
    date_created= models.DateTimeField(null=True, auto_now_add=True, blank=True)
    def __str__(self):
        return str(self.name)

class ShippingMethod(models.Model):
    shipping_company        = models.CharField(max_length=100)
    cost                    = models.FloatField()
    estimated_delivery_time = models.IntegerField()
    icon                    = models.ImageField(upload_to='images/')
    def __str__(self):
        return str(self.shipping_company)

class Profile(models.Model):
    Id         = models.AutoField(primary_key=True)
    user       = models.OneToOneField(User,on_delete=models.CASCADE)
    address    = models.CharField(max_length=300)
    profilePic = models.ImageField(upload_to='images/', blank=True, default = 'images/propic.jpeg')
    country    = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_seller  = models.IntegerField(null=True, blank=True, default=0)
    date_seller= models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.user.username)

class Dictio(models.Model):
    cart        = models.ForeignKey('Cart',on_delete=models.CASCADE)
    product     = models.IntegerField()
    feature     = models.CharField(max_length=30, default='nothing')
    quantity    = models.IntegerField()
    def __str__(self):
        return str(self.product)

class Cart(models.Model):
    profile      = models.OneToOneField('Profile',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.profile.user.username)

class OrderDict(models.Model):
    order     = models.ForeignKey('Order',on_delete=models.CASCADE)
    product   = models.IntegerField()
    feature   = models.CharField(max_length=30, default='nothing')
    quantity  = models.IntegerField()
    def __str__(self):
        return str(self.order)

class Order(models.Model):
    profile     = models.ForeignKey('Profile',on_delete = models.CASCADE)
    Order_date  = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(max_length=30, default='ON HOLD')
    payment     = models.CharField(max_length=30, default='Paypal')
    shipping	= models.CharField(max_length=40)
    total_price	= models.FloatField()
    def __str__(self):
        return str(self.id)

class Message(models.Model):
    Id           = models.AutoField(primary_key=True)
    profile      = models.ForeignKey('Profile',on_delete = models.CASCADE,null=True, blank=True)
    fullname     = models.CharField(max_length=30, default='nothing')
    email        = models.CharField(max_length=30, default='nothing')
    subject      = models.CharField(default='Contact Us',max_length=100,null=True, blank=True)
    content      = models.TextField(default='message',null=True, blank=True)
    sendto       = models.CharField(max_length=30, default=get_superuser_email,null=True, blank=True)
    seen         = models.IntegerField(default=0)
    draft        = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    profile     = models.ForeignKey('Profile',on_delete = models.CASCADE)
    product     = models.ForeignKey('Product',on_delete = models.CASCADE)
    review_date = models.DateTimeField(auto_now_add=True)
    review      = models.TextField()
    rating      = models.IntegerField()
    def __str__(self):
        return str(self.id)

class Wishlist(models.Model):
    profile     = models.ForeignKey('Profile',on_delete = models.CASCADE)
    product     = models.ForeignKey('Product',on_delete = models.CASCADE)

class SellerNotification(models.Model):
    Id           = models.AutoField(primary_key=True)
    profile      = models.ForeignKey('Profile',on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
