import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'book_system.settings')

import django
django.setup()
from book.models import Category, Book
'''
    # 名字 出版商 作者 价格 图书的描述 总评分 评论数量
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=128, unique=True)
    publishers = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    price = models.FloatField()
    description = models.TextField()
    score = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
'''
def populate():
    computer_books = [
        {"name": "Python基础知识",
         "publishers": "机械工业出版社",
         "author": "张三",
         "price": 59.6,
         "description": "基础知识，123"},
        {"name": "C++编程",
         "publishers": "人民邮电出版社",
         "author": "李四",
         "price": 20,
         "description": "c++语言简介，语法学习"},
        {"name": "django基础教程",
         "publishers": "abc",
         "author": "Leif Azzopardi & David Maxwell",
         "price": 36.5,
         "description": "django基础知识，web网站搭建"}
    ]

    social_books = [
        {"name": "无处安放的同情",
         "publishers": "广东人民出版社",
         "author": "[德]汉宁·里德",
         "price": 58.00,
         "description": "莱比锡图书奖得主经典哲学著作；20余位欧洲哲学家跨越时空的思想交锋；"
             "四个著名思想实验，一场关于世界大同的道德辩论！为什么我们总是对远处的灾难报以极大的同情，"
             "却对身边的不幸兴趣寥寥？世界被科技手段无限缩小，也把远处的不幸拉近到每个人身边。"
             "狄德罗相信五感的界限就是道德的界限，传媒技术将我们的感知力拓展到全球，"
             "让我们对千里之外的陌生人似乎也产生了道德责任；而卢梭认为人类的情感被距离拉伸时，"
             "必然会挥发、黯淡，我们之所以如此关注远处的灾难，正是因为我们不愿意承担身边的义务。"
             "德国知名作家、莱比锡图书奖得主汉宁·里德引用了十八世纪以来的几个著名思想实验，"
             "巴尔扎克、卢梭、伏尔泰、亚当·斯密等启蒙精英到陀思妥耶夫斯基、弗洛伊德、"
             "荣格等文学与思想巨擘跨越时空的思想交锋，掀起了一场关于世界大同的道德辩论。"},
        {"name": "雾行者",
         "publishers": "上海三联书店",
         "author": "路内",
         "price":  88.00,
         "description": "2004年冬，美仙建材公司仓库管理员周劭重返故地，调查一起部门同事的车祸死亡事件。"
             "与此同时，他的多年好友、南京仓管理员端木云不告而别。一个时代过去了，另一个时代正在到来。"
             "这是一本关于世纪交替的小说，从1998年的夏季，到奥运前夕的2008年，关于仓库管理员奇异的生活，"
             "关 于仿佛火车消失于隧道的二十岁时的恋人，直至中年的迷惘与自戮、告别与重逢，"
             "一群想要消灭过去之我的人，以及何之为我。"}
    ]

    cats = {"计算机":{"books":computer_books,"views":128,"likes":64},
            "社会":{"books":social_books, "views":64,"likes":32}}

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for book in cat_data["books"]:
            add_book(c, book)

    for c in Category.objects.all():
        for book in Book.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(book)))

def add_book(cat, book):
    b = Book.objects.get_or_create(category=cat, name=book['name'])[0]
    b.publishers = book['publishers']
    b.author = book['author']
    b.price = book['price']
    b.description = book['description']
    b.save()
    return b

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()