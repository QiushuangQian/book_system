from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from order.models import Cart,Order
from book.models import Book
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import math
from operator import *
import json
from django.db.models import Q

# Create your views here.
@login_required
def show_cart(request):
    print(request.user.id)
    context_dict = {}
    obj_cart = None
    try:
        obj_cart = Cart.objects.get(user_id=request.user.id)
    except Cart.DoesNotExist:
        return render(request, 'order/cart.html', context_dict)
    
    json_goods = json.loads(obj_cart.goods)
    print(json_goods)
    goods_list = []
    summary = 0.0
    for item in json_goods:
        try:
            book = Book.objects.get(id=item['id'])
        except Book.DoesNotExist:
            continue
        goods = {}
        goods['id'] = book.id
        goods['name'] = book.name
        goods['price'] = book.price
        goods['count'] = item['count']
        goods['total'] = goods['price'] * goods['count']
        goods_list.append(goods)
        summary = summary + goods['total']

    context_dict['goods'] = goods_list
    context_dict['summary'] = summary
    return render(request, 'order/cart.html', context_dict)
    #return HttpResponse('ok')

@login_required
def count_cart(request):
    try:
        obj_cart = Cart.objects.get(user_id=request.user.id)
    except Cart.DoesNotExist:
        return HttpResponse('0')
    return HttpResponse(obj_cart.count)

@login_required
def add_cart(request):
    book_id = None
    count = None
    if request.method == 'GET':
        book_id = int(request.GET['book_id'])
        count = int(request.GET['count'])
    print(book_id)
    print(count)

    if not book_id or not count:
        return HttpResponse('0')

    obj_cart = Cart.objects.get_or_create(user_id=request.user.id)[0]
    try:
        obj_book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        obj_book = None

    print(obj_book)
    print(obj_cart)
    if not obj_book:
        return HttpResponse('0')

    
    json_goods = []
    if len(obj_cart.goods):
        json_goods = json.loads(obj_cart.goods)
    for item in json_goods:
        if item['id'] == book_id:
            item['count'] = item['count'] + count
            obj_cart.count = obj_cart.count + count
            count = 0
            break
    if 0 < count:
        good = {'id':obj_book.id, 'count': count}
        json_goods.append(good)
        obj_cart.count = obj_cart.count + count
    obj_cart.goods = json.dumps(json_goods)
    obj_cart.save()

    print(obj_cart.goods)
    print(obj_cart.count)
    return HttpResponse(str(obj_cart.count))

@login_required
def delete_cart(request):
    book_id = None
    if request.method == 'GET':
        book_id = int(request.GET['book_id'])
    print(book_id)
    if not book_id:
        return HttpResponse('-1')
    
    try:
        obj_cart = Cart.objects.get(user_id=request.user.id)
    except Cart.DoesNotExist:
        return HttpResponse('-1')
    
    count = 0
    json_goods = []
    if len(obj_cart.goods):
        json_goods = json.loads(obj_cart.goods)
    for item in json_goods:
        if item['id'] == book_id:
            count = item['count']
            json_goods.remove(item)
            break
    obj_cart.goods = json.dumps(json_goods)
    obj_cart.count = obj_cart.count - count
    obj_cart.save()

    return HttpResponse(str(book_id))

@login_required
def settle_cart(request):
    context_dict = {}
    obj_user = User.objects.get(id=request.user.id)
    obj_cart = None
    try:
        obj_cart = Cart.objects.get(user_id=request.user.id)
    except Cart.DoesNotExist:
        obj_cart = None
    if not obj_cart:
        return render(request, 'order/settle.html', context_dict)

    obj_goods = json.loads(obj_cart.goods)
    for item in obj_goods:
        obj_book = Book.objects.get(id=item['id'])
        obj_order = Order.objects.create(user=obj_user, book=obj_book)
        obj_order.num = item['count']
        obj_order.status = 1
        obj_order.save()
    context_dict['count'] = obj_cart.count
    obj_cart.delete()

    return render(request, 'order/settle.html', context_dict)

@login_required
def show_order(request):
    context_dict = {}
    obj_orders = None
    try:
        obj_orders = Order.objects.filter(user_id=request.user.id).order_by('-id')[:20]
    except Order.DoesNotExist:
        return render(request, 'order/order.html', context_dict)
    
    order_list = []
    for item in obj_orders:
        order_dict = {}
        order_dict['id'] = item.id
        order_dict['goods_id'] = item.book.id
        order_dict['goods_name'] = item.book.name
        order_dict['goods_count'] = item.num
        order_dict['total_price'] = item.book.price * item.num
        if 1 == item.status:
            order_dict['not_comment'] = item.status
        if 2 == item.status:
            order_dict['has_comment'] = item.status
        order_list.append(order_dict)
    
    context_dict['orders'] = order_list
    return render(request, 'order/order.html', context_dict)

@login_required
def modify_order(request):
    order_id = None
    if request.method == 'GET':
        order_id = int(request.GET['order_id'])
    print(order_id)
    if not order_id:
        return HttpResponse('-1')

    try:
        obj_order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse('-1')
    obj_order.status = 2
    obj_order.save()
    return HttpResponse(str(order_id))
