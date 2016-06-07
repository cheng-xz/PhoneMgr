from models import *
from django.shortcuts import render_to_response,RequestContext,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
import time
from django.db.models import Q

#对应的字段为1表示该菜单无效
MainMenu = MainMenu.objects.filter(~Q(IfNotEffective='1'))

def RepeatList(R):
    result = []
    for i in range(len(R)):
        if R[i] not in R[(i+1):]:
            result.append(R[i])

    return result

#传入参数
#user: 操作人
#code: 操作编码
#x: 待提取的数据对象
#sign:标记 1:表示手机  2：用户 3：SIM

def SaveLog(user,code,x,sign=1):
    if sign == 1:
        s = x.PhoneName
    elif sign == 2:
        s = x.username
    elif sign == 3:
        s = x.PhoneNum
    else:
        s = 'error'
    
    p1 = LogInfo(UserName=user.username,\
                 code=code,\
                 PhoneName = s,\
                 CreateDate = int(time.time()))
    p1.save()
    

def MyAllAuth(user,authname):
    if user.username != 'admin' and not user.has_perm(authname):
        return HttpResponseRedirect('/')

def MyMail(sub,content,tomail):
    sub = '【测试机管理系统】' + sub
    send_mail(\
        sub,\
        content,\
        'cxztest@163.com',\
        [content,],\
        fail_silently = False
        )
