from django.db import models
from book.models import User, Book

# Create your models here.
# 购物车
class Cart(models.Model):
    user = models.OneToOneField(User)       # 关联用户
    goods = models.TextField(default='')    # 购物车中商品编号列表及数量
    count = models.IntegerField(default=0)  # 购物车中商品数量
    def __str__(self):
        return str(self.user.username)

# 订单
class Order(models.Model):
    user = models.ForeignKey(User)           # 关联用户
    book = models.ForeignKey(Book)           # 订单关联的商品
    num = models.IntegerField(default=0)     # 商品数量
    comments = models.TextField(default='')  # 评论的编号列表
    status = models.IntegerField(default=0)  # 订单状态：1：已结算；2：已评价
    def __str__(self):
        return str(self.id)