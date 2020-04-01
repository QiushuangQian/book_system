#-*-coding:utf-8-*-

import json
import random
import pymysql
import re

# 图片url列表
list_pic = []

# 图书
class Book:
    def __init__(self, item, categoryid):
        self.name = item['name']
        self.pic = item['pic']
        self.pic = self.pic.split('/')[-1]
        self.author = item['author']
        self.publishers = item['publishers']
        temp = re.findall(r'-?\d+\.?\d*e?-?\d*?', item['price'])[0]
        self.price = float(temp)
        self.description = item['description']
        self.category_id = categoryid

    def show(self):
        print('--------------------book-----------------------')
        print('name:        ' + self.name)
        print('pic:         ' + self.pic)
        print('author:      ' + self.author)
        print('publishers:  ' + self.publishers)
        print('pric:        ' + str(self.price))
        print('description: ' + self.description)
        print('category_id: ' + self.category_id)

# 评论
#        item['comments']
#        item['scores']
class Comment:
    def __init__(self, content, score, book_id, user_ids):
        self.content = content
        self.book_id = book_id
        self.user_id = random.choice(user_ids)[0]
        if '力荐' == score:
            self.score = 10
        elif '推荐' == score:
            self.score = 8
        elif '还行' == score:
            self.score = 6
        elif '较差' == score:
            self.score = 4
        elif '很差' == score:
            self.score = 2
        else:
            print('Comment score error')
            self.score = 0

    def show(self):
        print('------------------------comment-----------------')
        print('book_id: ' + str(self.book_id))
        print('user_id: ' + str(self.user_id))
        print('score:   ' + str(self.score))
        print('content: ' + self.content)

# 打开数据库连接
conn = pymysql.connect('127.0.0.1', 'root', '123456', 'book_system')

def search_userids(conn):
    userids = []
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()

    # 异常处理
    try:
        cursor.execute("select user_id from book_userprofile")

        #查询多条数据

        result=cursor.fetchall()

        for data in result:
            userids.append(data)
    except:
        # 如果发生错误则执行回滚操作
        print('error')
        return userids
    return userids

def search_bookid(conn, book_name):
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    sql = "select id from book_book where name='" + book_name + "'"
    print(sql)
    # 异常处理
    try:
        cursor.execute(sql)

        #查询多条数据
        result=cursor.fetchall()
        for data in result:
            return data[0]
    except:
        # 如果发生错误则执行回滚操作
        print('error')
        return -1

def insert_book(conn, book):
    # SQL语句：向数据表中插入数据
    sql = "INSERT INTO book_book(name,publishers,author,price,description,scores,number,category_id, picture)" \
          " values('%s','%s','%s',%f,'%s',0,0,%d,'%s')"%(book.name, book.publishers, book.author, book.price,book.description, book.category_id, book.pic)

    print(sql)
    cursor = conn.cursor()
    # 异常处理
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交事务到数据库执行
        conn.commit()       # 事务是访问和更新数据库的一个程序执行单元
        print('ok')
        return True
    except:
        # 如果发生错误则执行回滚操作
        conn.rollback()
        return False

def insert_comment(conn, comment):
    # SQL语句：向数据表中插入数据
    print(type(comment.score))
    print(type(comment.content))
    print(type(comment.book_id))
    print(type(comment.user_id))
    print(comment.user_id)
    sql = "INSERT INTO book_comment(score, content, book_id, user_id) values(%d, '%s', %d, %d)" % (comment.score, comment.content, comment.book_id, comment.user_id)

    print(sql)
    cursor = conn.cursor()
    # 异常处理
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交事务到数据库执行
        conn.commit()       # 事务是访问和更新数据库的一个程序执行单元
        print('ok')
        return True
    except:
        # 如果发生错误则执行回滚操作
        conn.rollback()
        #return False
    return True


#  book_images/28478428-1_b_8.jpg
with open("books-5社会.json", encoding='utf-8') as f:
    json_data = json.load(f)
categoryid = 5

user_ids = search_userids(conn)
for item in json_data:
    list_pic.append(item['pic'])
    book = Book(item, categoryid)
    if False == insert_book(conn, book):
        continue
    bookid = search_bookid(conn, book.name)
    print(bookid)
    print(len(item['comments']))
    print(len(item['scores']))
    len1 = len(item['comments'])
    len2 = len(item['scores'])
    length = len1
    if len1 > len2:
        length = len2
    for idx in range(length):
        comment = Comment(item['comments'][idx], item['scores'][idx], bookid, user_ids)
        comment.show()
        if False == insert_comment(conn, comment):
            exit()

with open(str(categoryid) + 'pic',"w") as f:
    f.writelines(str(list_pic))

'''
item = json_data[0]

list_pic.append(item['pic'])
book = Book(item)

print(list_pic)
book.show()

user_ids=[1,2,3,4,5]
book_id = 58
comment = Comment(item['comments'][0], item['scores'][0], book_id, user_ids)
comment.show()


import pymysql

# 打开数据库连接
conn = pymysql.connect('127.0.0.1', 'root', '123456', 'book_system')

# 使用cursor()方法获取操作游标
cursor = conn.cursor()

categories = ['诗词','言情','哲学','社会','教育','金融','投资','编程','通信']
for i in categories:
    name = "test" + str(i)
    email = name + "@163.com"
    # SQL语句：向数据表中插入数据
    sql = "INSERT INTO book_category(name) \
             VALUES ('%s')" % (i)

    print(sql)
    # 异常处理
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交事务到数据库执行
        conn.commit()       # 事务是访问和更新数据库的一个程序执行单元
        print('ok')
    except:
        # 如果发生错误则执行回滚操作
        conn.rollback()

# 关闭数据库连接
conn.close()
'''