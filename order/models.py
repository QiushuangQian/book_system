from django.db import models
from book.models import User, Book

# Create your models here.
# ���ﳵ
class Cart(models.Model):
    user = models.OneToOneField(User)       # �����û�
    goods = models.TextField(default='')    # ���ﳵ����Ʒ����б�����
    count = models.IntegerField(default=0)  # ���ﳵ����Ʒ����
    def __str__(self):
        return str(self.user.username)

# ����
class Order(models.Model):
    user = models.ForeignKey(User)           # �����û�
    book = models.ForeignKey(Book)           # ������������Ʒ
    num = models.IntegerField(default=0)     # ��Ʒ����
    comments = models.TextField(default='')  # ���۵ı���б�
    status = models.IntegerField(default=0)  # ����״̬��1���ѽ��㣻2��������
    def __str__(self):
        return str(self.id)