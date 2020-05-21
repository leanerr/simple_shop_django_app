from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.




def catalog(request):
    #check that if there is cart already , if not create one
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']
    #dont expire untill the browser is closed
    request.session.set_expiry(0)
    #getting all products, to show in main page
    store_items = Product.objects.all()
    ctx = {
        'store_items' : store_items,
        'cart_size' : len(cart)
    }
    if request.method == "POST":
        #will add the object that they have posted to the card.
        #we called our form object input object ID . the input name = "obj_id"
        #after clicking to addToItem  => the item will add to cart by its porduct.id as value and obj_id as name in input
        cart.append(int(request.POST['obj_id']))
        #catalog is the name of the main page
        return  redirect('catalog')

    return render(request , "main.html" , ctx)

#************************************************
#cart page data
#getting and returning real product from DB
def cartItems(cart):
    items = []
    #the products that are added to cart , now will be gotten from DB
    #and they will be added in items
    for item in cart:
        #we added products by their id , so item here is the id
        #and we use this item to be = id in query
        items.append(Product.objects.get(id=item))
    return items


#return total_price for each product(item)
def priceCart(cart):
    cart_items = cartItems(cart)
    price = 0
    for item in cart_items:
        price += item.price
    return price
def genItemsList(cart):
    cart_items = cartItems(cart)
    items_list = ""
    for item in cart_items:
        items_list += ","
        items_list += item.name
    return items_list


#cart page
def cart(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {
        'cart':cart ,
        #the number of products in cart
        'cart_size' : len(cart) ,
        #the porduct in cart
        'cart_items': cartItems(cart),
        #the total price of each product in cart by knwoing its number
        'total_price':priceCart(cart),
    }
    return render(request , "cart.html" , ctx)

def removefromcart(request):
    request.session.set_expiry(0)
    #getting obj_id or the name  of the item that is going to be deleted
    obj_to_remove = int(request.POST['obj_id'])
    #finding the index of that item in cart.array
    obj_index = request.session['cart'].index(obj_to_remove)
    #pop it !
    request.session['cart'].pop(obj_index)
    return redirect('cart')



def checkout(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {
        'cart':cart ,
        'cart_size':len(cart) ,
        'total_price':priceCart(cart)
    }
    return render(request, "checkout.html", ctx)


def completeOrder(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart,
           'cart_size':len(cart),
           'cart_items':cartItems(cart),
           'total_price': priceCart(cart)}
    order = Order()
    order.items = genItemsList(cart)
    order.first_name = request.POST['first_name']
    order.last_name = request.POST['last_name']
    order.address = request.POST['address']
    order.city = request.POST['city']
    order.payment_data = request.POST['payment_data']
    order.fulfilled = False
    order.payment_method = request.POST['payment']
    order.save()
    request.session['cart'] = []
    return render(request, "complete_order.html", ctx)


def adminLogin(request):
    if request.method == "POST":
        usname = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(username=usname, password=pwd)
        if user is not None:
                login(request, user)
                return redirect("admin")
        else:
            return render(request, "admin_login.html", {'login': False})


    return render(request, "admin_login.html",None)

def adminDashboard(request):
    orders = Order.objects.all()
    ctx = {'orders': orders}
    return render(request, "admin_panel.html", ctx)

