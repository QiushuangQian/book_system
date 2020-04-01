#-*-coding:utf-8-*-

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