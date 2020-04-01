from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# 导入 Category 模型
from book.models import Category, Book, Comment
from book.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import math
from operator import *
import json
from django.db.models import Q

# Create your views here.
def index(request):
    # 查询数据库，获取目前存储的所有分类
    # 按点赞次数倒序排列分类
    # 获取前 5 个分类（如果分类数少于 5 个，那就获取全部）
    # 把分类列表放入 context_dict 字典
    # 稍后传给模板引擎
    #category_list = Category.objects.order_by('-likes')[:5]
    book_list = Book.objects.order_by('-id')[:8]
    context_dict = {'books': book_list}
    # 渲染响应，发给客户端
    return render(request, 'book/index.html', context_dict)
    #return HttpResponse('abc')

def show_category(request, category_id):
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}
    try:
        # 能通过传入的分类别名找到对应的分类吗？
        # 如果找不到， .get() 方法抛出 DoesNotExist 异常
        # 因此 .get() 方法返回一个模型实例或抛出异常
        category = Category.objects.get(id=category_id)
        # 检索关联的所有网页
        # 注意， filter() 返回一个网页对象列表或空列表
        books = Book.objects.filter(category=category).order_by('-id')[:20]
        # 把得到的列表赋值给模板上下文中名为 pages 的键
        context_dict['books'] = books
        # 也把从数据库中获取的 category 对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category
    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 什么也不做
        # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['books'] = None
    # 渲染响应，返回给客户端
    return render(request, 'book/category.html', context_dict)

def show_book(request, book_id):
    context_dict = {}
    try:
        book = Book.objects.get(id=book_id)
        comments = Comment.objects.filter(book_id=book_id).order_by('-id')[:10]
        context_dict['book'] = book
        context_dict['category'] = book.category
        context_dict['comments'] = comments
    except Book.DoesNotExist:
        context_dict['book'] = None
        context_dict['category'] = None
        context_dict['comments'] = None
    print(context_dict['category'].name)
    return render(request, 'book/book.html', context_dict) 

def register(request):
    # 一个布尔值，告诉模板注册是否成功
    # 一开始设为False，注册成功后改为True
    registered = False

    # 如果是HTTP POST请求，处理表单数据
    if request.method == 'POST':
        # 尝试获取原始表单数据
        # 注意，UserForm和UserProfileForm中的数据都需要
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # 如果两个表单中的数据是有效的......
        if user_form.is_valid() and profile_form.is_valid():
            # 把UserForm中的数据存入数据库
            user = user_form.save()

            # 使用set_password方法计算密码哈希值
            # 然后更新user对象
            user.set_password(user.password)
            user.save()

            # 现在处理UserProfile实例
            # 因为要自行处理user属性，所以设定commit=False
            # 延迟保存模型，以防止出现完整性问题
            profile = profile_form.save(commit=False)
            profile.user = user

            # 用户提供头像了吗？
            # 如果提供了，从表单数据库中提取出来，赋给UserProfile模型
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            # 保存UserProfile模型实例
            profile.save()

            # 更新变量的值，告诉模板成功注册了
            registered = True
        else:
            # 表单数据无效，出错了？
            # 在终端打印问题
            print(user_form.errors, profile_form.errors)
    else:
        # 不是HTTP POST请求，渲染两个ModelForm实例
        # 表单为空，待用户填写
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    # 根据上下文渲染模板
    return render(request, 
                  'book/register.html',
                  {'user_form': user_form,
                  'profile_form': profile_form,
                  'registered': registered})

def user_login(request):
    # 如果是HTTP POST请求，尝试提取相关信息
    if request.method == 'POST':
        # 获取用户在登陆表单中输入的用户名和密码
        # 我们使用的事request.POST.get('<variable>')
        # 而不是request.POST['<variable>']
        # 这是因为对应的值不存在时，前者返回None,
        # 而后者抛出KeyError异常
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 使用Django提供的函数检查username/password是否有效
        # 如果有效，返回一个User对象
        user = authenticate(username=username, password=password)

        # 如果得到了User对象，说明用户输入的凭据是对的
        # 如果是None，说明没找到与凭据匹配的用户
        if user:
            # 账户激活了吗？可能被禁了
            if user.is_active:
                # 登入有效且已激活的账户
                # 然后重定向到首页
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # 账户未激活，禁止登录
                return HttpResponse("Your account is disabled.")
        else:
            # 提供的登录凭据有问题，不能登录
            print('Invalid login details: {0}, {1}'.format(username, password))
            return render(request, 'book/login.html', {'info':"Invalid login details supplied."})
    # 不是HTTP POST请求，显示登录表单
    # 极有可能是HTTP GET请求
    else:
        # 没什么上下文变量要传给模板系统
        # 因此传入一个空字典
        return render(request, 'book/login.html', {})

# 使用login_required()装饰器限制
# 只有已登录的用户才能访问这个视图
@login_required
def user_logout(request):
    # 可以确定用户已登录，因此直接退出
    logout(request)
    # 把用户带回首页
    return HttpResponseRedirect(reverse('index'))

@login_required
def add_comment(request):
    user_id = None
    book_id = None
    content = None
    score = None
    if request.method == 'GET':
        user_id = request.GET['user_id']
        book_id = request.GET['book_id']
        content = request.GET['content']
        score = request.GET['score']
    
    if user_id and book_id:
        try:
            user_obj = User.objects.get(id=int(user_id))
        except User.DoesNotExist:
            user_obj = None

        try:
            book_obj = Book.objects.get(id=int(book_id))
        except Book.DoesNotExist:
            book_obj = None

        print(book_obj)
        print(book_obj.id)
        comment = Comment.objects.create(book=book_obj, user=user_obj)
        comment.score = int(score)
        comment.content = content
        comment.save()

        print(user_obj)
        print(book_obj)
        #print(comment)
    return HttpResponse("ok")

@login_required
def favorite(request):
    userid = None
    if request.method == 'GET':
        userid = request.GET['user_id']
    
    if not userid:
        return HttpResponse('[]')
    
    rv_dict, shopping_dict = get_user_data(userid)

    print(rv_dict)
    print(shopping_dict)
    if 0 == len(rv_dict) or 0 == len(shopping_dict):
        return HttpResponse('[]')

    W3 = Usersim(shopping_dict)
    Last_Rank = Recommend(int(userid), shopping_dict, W3, rv_dict, 2)
    print(Last_Rank)


    book_list = []
    for i in Last_Rank:
        book = Book.objects.get(id=i)
        item = {}
        item['id'] = book.id
        item['name'] = book.name
        item['picture'] = str(book.picture)
        item['author'] = book.author
        item['publishers'] = book.publishers
        item['price'] = book.price
        item['category'] = book.category.name
        book_list.append(item)
    book_list = book_list[:20]
    with open("rb.json","w") as f_obj:
        json.dump(book_list,f_obj)

    return HttpResponse(json.dumps(book_list))

# 得到用户user相关dic,rv
def  get_user_data(userid):
    shopping_dict = {}
    rv_dict = {}

    try:
        #获取当前用户的评论列表
        comment_list = Comment.objects.filter(user_id=userid)
    except User.DoesNotExist:
        comment_list = []
        return rv_dict, shopping_dict
    
    books_set = set()
    for item in comment_list:
        #获取用户评论过的书籍
        books_set.add(item.book_id)

    user_set = set()
    #user_set.add(userid)
    #获取该用户评论过的书籍的其他评论用户
    for bookid in books_set:
        comment_list = Comment.objects.filter(book_id=bookid)
        for item in comment_list:
            user_set.add(item.user_id)
    
    for userid in user_set:
        books_set = set()
        rv_item_dict = {}
        comment_list = Comment.objects.filter(user_id=userid)
        for item in comment_list:
            books_set.add(item.book_id)
            rv_item_dict[item.book_id] = item.score
        rv_dict[userid] = rv_item_dict
        shopping_dict[userid] = tuple(books_set)
    return rv_dict, shopping_dict

#例子中的数据相当于是一个用户字典{A:(a,b,d),B:(a,c),C:(b,e),D:(c,d,e)}
#我们这样存储原始输入数据
 
#dic={'A':('a','b','d'),'B':('a','c'),'C':('b','e'),'D':('c','d','e')}#简单粗暴，记得加''
 
#计算用户兴趣相似度
def Usersim(dicc):
	#把用户-商品字典转成商品-用户字典（如图中箭头指示那样）
	item_user=dict()
	for u,items in dicc.items():
		for i in items:#文中的例子是不带评分的，所以用的是元组而不是嵌套字典。
			if i not in item_user.keys():
				item_user[i]=set()#i键所对应的值是一个集合（不重复）。
			item_user[i].add(u)#向集合中添加用户。
 
	C=dict()#感觉用数组更好一些，真实数据集是数字编号，但这里是字符，这边还用字典。
	N=dict()
	for item,users in item_user.items():
		for u in users:
			if u not in N.keys():
				N[u]=0   #书中没有这一步，但是字典没有初始值不可以直接相加吧
			N[u]+=1 #每个商品下用户出现一次就加一次，就是计算每个用户一共购买的商品个数。
			#但是这个值也可以从最开始的用户表中获得。
			#比如： for u in dic.keys():
			#             N[u]=len(dic[u])
			for v in users:
				if u==v:
					continue
				if (u,v) not in C.keys():#同上，没有初始值不能+=
					C[u,v]=0
				C[u,v]+=1  #这里我不清楚书中是不是用的嵌套字典，感觉有点迷糊。所以我这样用的字典。
#到这里倒排阵就建立好了，下面是计算相似度。
	W=dict()
	for co_user,cuv in C.items():
		W[co_user]=cuv / math.sqrt(N[co_user[0]]*N[co_user[1]])#因为我不是用的嵌套字典，所以这里有细微差别。
	return W
 
def Recommend(user,dicc,W2,rv,K):
    rank=dict()
    related_user=[]
    #相似用户评论过的书中当前用户已经购买过的书
    interacted_items=dicc[user]
    for co_user,item in W2.items():
        if co_user[0]==user:
            related_user.append((co_user[1],item))#先建立一个和待推荐用户兴趣相关的所有的用户列表。
    for v,wuv in sorted(related_user,key=itemgetter(1),reverse=True)[0:K]:
    #找到K个相关用户以及对应兴趣相似度，按兴趣相似度从大到小排列。itemgetter要导包。
        for i in dicc[v]:
            if i in interacted_items:
                continue
            if i not in rank.keys():#如果不写要报错，是不是有更好的方法？
                rank[i]=0
            if v in rv and i in rv[v]:
                rank[i] += wuv * rv[v][i]
    return rank

def category_search(request):
    category_id = None
    search_type = None
    condition_value = None
    if request.method == 'GET':
        category_id = request.GET['category_id']
        keyword = request.GET['keyword']

    if not category_id:
        return HttpResponse('[]')

    book_list = Book.objects.filter(Q(category_id=category_id),Q(name__icontains=keyword)|Q(author__icontains=keyword)|Q(publishers__icontains=keyword))
    result = []
    i = 0
    for book in book_list:
        item = {}
        item['id'] = book.id
        item['name'] = book.name
        item['picture'] = str(book.picture)
        item['author'] = book.author
        item['publishers'] = book.publishers
        item['price'] = book.price
        item['category'] = book.category.name
        result.append(item)
        i += 1
        if 20 <= i:
            break;

    return HttpResponse(json.dumps(result))

def global_search(request):
    keyword = None
    if request.method == 'GET':
        keyword = request.GET['keyword']

    if None == keyword:
        return HttpResponse('no data')

    # sciencenews = models.Sciencenews.objects.filter(Q(title__icontains=keyword)\
	#	|Q(content__icontains=keyword)|Q(author__icontains=keyword))
    book_list = []
    book_list = Book.objects.filter(Q(name__icontains=keyword)|Q(author__icontains=keyword)|Q(publishers__icontains=keyword))
    #return HttpResponse(json.dumps(book_list))
    print(book_list)
    result = []
    i = 0
    for book in book_list:
        item = {}
        item['id'] = book.id
        item['name'] = book.name
        item['picture'] = str(book.picture)
        item['author'] = book.author
        item['publishers'] = book.publishers
        item['price'] = book.price
        item['category'] = book.category.name
        result.append(item)
        i += 1
        if 20 <= i:
            break;

    return HttpResponse(json.dumps(result))

@login_required
def comment(request):
    order_id = None
    user_id = None
    book_id = None
    context_dict = {}
    if request.method == 'GET':
        order_id = request.GET['order_id']
        book_id = request.GET['book_id']
        user_id = request.user.id

    if not order_id or not book_id or not user_id:
        return render(request, 'book/comment.html', context_dict)

    context_dict['order_id'] = order_id
    context_dict['user_id'] = user_id
    context_dict['book_id'] = book_id
    return render(request, 'book/comment.html', context_dict)

'''
if __name__=='__main__':
	W3=Usersim(dic)
	Last_Rank=Recommend('A',dic,W3,2)
	print Last_Rank
'''
