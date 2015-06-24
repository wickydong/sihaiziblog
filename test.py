#!/usr/bin/python
# -*-coding:utf8-*-


import smtplib  
from email.mime.text import MIMEText  
  
def send_mail(sub,content):  
    mailto_list=["kundong@gridinfo.com.cn"] 
    mail_host="smtp.163.com"  #设置服务器
    mail_user="dongkun881226"    #用户名
    mail_pass="beibei2baobao"   #口令 
    mail_postfix="163.com"  #发件箱的后缀
    me="WickyDong"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(mailto_list)  
    print "准备就绪"
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        print "准备发送"
        server.sendmail(me,mailto_list, msg.as_string())  
        server.close()  
        print "发送成功"  
        return True
    except Exception, e:  
        print str(e)  
        return False  
#if __name__ == '__main__':  
#    if send_mail(mailto_list,"hello","hello world！"):  
#        print "发送成功"  
#    else:  
#        print "发送失败"  
