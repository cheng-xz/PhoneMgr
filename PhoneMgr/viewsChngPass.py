from django.http import HttpResponse
from django.shortcuts import render_to_response,RequestContext,HttpResponseRedirect
from formQue import *
from models import *
import time,traceback
from django.core.mail import send_mail
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
import traceback

#导入公共模块
from viewsPub import MainMenu


@login_required
def ChngPassMgr(request):
    user = request.user
    if True: #user.username == 'admin' or user.has_perm('PhoneMgr.PasswordMan_ModPasswd'):     
        OpResult = ''
        form = ''
        if request.method == 'POST':
            oldPass = request.POST['oldPass']
            newPass = request.POST['newPass']

            if len(oldPass) == 0 or len(newPass) == 0:
                OpResult = '填写数据有误'
            elif user.check_password(oldPass) == False:
                OpResult = '原密码错误'
            else:
                user.set_password(newPass)
                user.save()
                OpResult = '密码修改成功'
            

        return render_to_response('ChngPass.html',{'OpResult':OpResult,'MainMenu':MainMenu},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无权操作！')
