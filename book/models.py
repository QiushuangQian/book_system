from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self): # Python 2 还要定义 __unicode__
        return self.name

class Book(models.Model):
    # 名字 出版商 作者 价格 图书的描述 总评分 评论数量
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=128, unique=True)
    picture = models.ImageField(upload_to='book_images', blank=True)
    publishers = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    price = models.FloatField(default=0.0)
    description = models.TextField()
    scores = models.IntegerField(default=0)
    number = models.IntegerField(default=0)

    def __str__(self): # Python 2 还要定义 __unicode__
        return self.name

class UserProfile(models.Model):
    # 这一行是必须的
    # 建立与 User 模型之间的关系
    user = models.OneToOneField(User)
    # 想增加的属性
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    # 覆盖 __str__() 方法，返回有意义的字符串
    # 如果使用 Python 2.7.x，还要定义 __unicode__ 方法
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)

    score = models.IntegerField(default=0)
    content = models.TextField()

    def __str__(self):
        return str(self.score)
