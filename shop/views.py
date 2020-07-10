from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
# Create your views here.
def index(request):
    products = Product.objects.all()
    # n = len(products)
    # nslides = (n//4) + ceil((n/4) - (n//4))
    # params = {'no_slides':nslides, 'product':products, 'range':range(1, nslides)}
    # allProds = [[products, range(1, nslides), nslides], 
    #             [products, range(1, nslides), nslides]]
    allProds = []
    catprods =  Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = (n // 4) + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nslides), nslides])

    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)
def about(request):
    return render(request, 'shop/about.html')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        desc = request.POST.get('desc', '')
        subject = request.POST.get('subject', '')
        contacts = Contact(name=name, email=email, desc=desc, subject=subject)
        contacts.save()
        return render(request, 'shop/contact.html', {'suc':"success"})
    else:
        return render(request, 'shop/contact.html')
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_decs, 'time':item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')
def searchMatch(query, item):
    #Return true only if query matches the item
    if query in item.product_desc or query in item.product_name or query in item.category:
        return True
    elif query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods =  Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslides = (n // 4) + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nslides), nslides])
    params = {'allProds':allProds, 'msg':""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg':"Please make sure to enter relevant search query"} 
    return render(request, 'shop/search.html', params)

def productView(request, myid):
    # fetching the product view using id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/productview.html', {'productv':product[0]})

def checkout(request):
    if request.method == "POST":
        itemsJson = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '')+ " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json = itemsJson, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phoneNumber=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_decs="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html')
