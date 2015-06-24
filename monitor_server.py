#! /usr/bin/python
# -*- coding: utf8 -*-
# author: WickyDong
import MySQLdb
import datetime
import test
time = datetime.datetime.today().strftime("%Y-%m-%d")
def makesql():
    content = ""
    try:
        con = MySQLdb.connect(host="localhost",user="root",passwd="root",\
              db="sihaizi")
        cur = con.cursor()
        cur.execute("select cpu,mem,disk,come from monitor where day like '%%%s%%'" %time)
        msg =  cur.fetchall()
        for i in msg:
            cpu = i[0].encode("utf-8").lstrip(" ").split("%")[0].split(" ")[-1]
            print cpu
            mem = i[1]
            disk = i[2].strip("\n")
            come = i[3]
            msg_str = ''' 
%s 服务器情况：
cpu未使用：%s%%;
内存闲置：%s KB;
硬盘情况：
%s;\n 
''' %(come,cpu,mem,disk)
            content = content + msg_str + "\n"
        sub = "12xue linux服务器巡检(测试版)"
        test.send_mail(sub,content)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

makesql()
