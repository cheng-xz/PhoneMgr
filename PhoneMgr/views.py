#-*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response,RequestContext,HttpResponseRedirect
from formQue import *
from models import *
import time,traceback
from django.core.mail import send_mail
from django.db import connection

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User,Group




#导入其他的模块信息
from viewsUser import *
from viewsDevice import *
#from viewsPubDevice import *
#from viewsAssignDevice import *
#from viewsConfirmBorrow import *
#from viewsBorrowedDevice import *
#from viewsConfirmBack import *
from viewsSimInfo import *
from viewsChngPass import *
from viewsLog import *
from viewsMyDev import *
from viewsTestPage import *


from viewsPub import MainMenu


def mylogout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login?next=/')

@login_required
def homepage(request):
    context = '这是主页面'
    #user = request.user
    #if user.username == 'admin':
    #    print 'user:',user.username

    return render_to_response('home.html',{'context':context,'MainMenu':MainMenu},\
                              context_instance = RequestContext(request))

def AskBackMgr(request):
    context = '这里是催还借出设备管理界面'

    return render_to_response('home.html',{'context':context})

def msg_show(request):
    if request.method == 'GET':
        notice = request.GET['t']
        return HttpResponse(notice)

def msg_show_noauth(request):
    if request.method == 'GET':
        notice = request.GET['t']
        return render_to_response('msg.html',{'context':notice},\
                                  context_instance = RequestContext(request))
