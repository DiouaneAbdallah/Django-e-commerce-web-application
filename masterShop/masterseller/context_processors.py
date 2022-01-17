from shop.models import *
from datetime import date, timedelta,datetime

def pages(request):
	if not request.user.is_superuser:
		args = {}
		if request.user.is_authenticated:
			messages = Message.objects.all().exclude(profile=Profile.objects.get(user=request.user)).order_by('-date_created')
			newmessages = Message.objects.filter(seen = 0).exclude(profile=Profile.objects.get(user=request.user)).order_by('-date_created')

			args['messages']=messages
			args['newmessages']=newmessages
			args['profile']		= Profile.objects.get(user=request.user)

			productstoday = Product.objects.filter(seller=Profile.objects.get(user=request.user),date_created=datetime.today()).count()
			profilestoday = Product.objects.filter(seller=Profile.objects.get(user=request.user),date_created=datetime.today()).count()
			orderstoday   = Order.objects.filter(Order_date=datetime.today()).count()
			totaltoday    = productstoday + profilestoday + orderstoday

			args['productstoday']	= productstoday
			args['profilestoday']	= profilestoday
			args['orderstoday']  	= orderstoday
			args['productstoday']	= productstoday
			args['totaltoday']   	= totaltoday
			return args
		else:
			return {}
	else:
		return {}
