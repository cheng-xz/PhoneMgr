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
from viewsPub import SaveLog,MainMenu,RepeatList

tag = None

#这里的设备主要是手机
@login_required
def MyDevMgr(request):
    global tag 
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.MyDevice_MyDeviceMenu'):    
        PhoneInfoResult = PhoneInfo.objects.filter(Owner=user)
        SimInfoResult = SimInfo.objects.filter(CurrOwner=user)

#        tag = PhoneInfoResult
                

        return render_to_response('MyDevice.html',{'PhoneInfoResult':PhoneInfoResult,'MainMenu':MainMenu,\
                                                 'SimInfoResult':SimInfoResult},\
                              context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无权访问我的设备！')

@login_required
def MyDevMgr_Borrow(request):
    user = request.user
    if True:  
        op_result = ''
        if request.method == 'POST':
            form = PhoneInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                #print SimInfo.objects.get(id = 2)
                #这里添加数据
                CurrState = 12  #分配设备借出
                #获取要修改的数据值
                p1 = PhoneInfo.objects.get(id = request.POST['p_id'])
                #进行状态检查
                if p1.CurrState == 12:
                    return HttpResponseRedirect('/msg?t=指定的设备已经借出！')
                
                p1.BorrowMan = User.objects.get(id = int(cd['BorrowMan']))
                p1.BorrowDate = int(time.time())
                p1.IfBorrowAuth = 1
                p1.BorrowAuthMan = user
                p1.CurrState = CurrState
                p1.UpdateDate = int(time.time())

                #进行操作合法性检查
                if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_BorrowDevice') or p1.Owner == user:
                    pass
                else:
                    return HttpResponseRedirect('/msg?t=无权进行借出操作！')
                
                try:
                    p1.save()   
                except:
                    op_result = '设备借出失败！'
                else:
                    op_result = '设备借出成功'

                    p2 = PhoneHisState(PhoneInfo=p1,\
                                       BorrowMan = p1.BorrowMan,\
                                       BorrowDate = p1.BorrowDate,\
                                       CurrState=CurrState,\
                                       BorrowAuthMan = p1.BorrowAuthMan,\
                                       CreateDate=int(time.time()))
                    p2.save()
                    #保存日志记录
                    SaveLog(user,1006,p1,1)

                return HttpResponseRedirect('/msg?t='+op_result)
        else:
            id_i = int(request.GET['id'])
            #获取要修改的数据值
            try:
                p1 = PhoneInfo.objects.get(id=id_i)
            except:
                return HttpResponseRedirect('/msg?t=错误的操作！')

            if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_BorrowDevice') or p1.Owner == user:
                pass
            else:
                return HttpResponseRedirect('/msg?t=无权进行借出操作！')
            

            if p1.CurrState == 12:
                return HttpResponseRedirect('/msg?t=已借出的设备不能重复借出')
            #对待修改的数据进行初始化
            form = PhoneInfoQue(
                initial = {'PhoneName':p1.PhoneName,\
                           'BorrowMan':p1.BorrowMan
                           }
                )
            
        return render_to_response('Dev_Borrow.html',{'form':form,
                                                           'op_result':op_result,\
                                                           'p_id':id_i},\
                                  context_instance = RequestContext(request))



@login_required
def MyDevMgr_Back(request):
    user = request.user
    if True:
        op_result = ''
        
        id_i = int(request.GET['id'])
        #获取要修改的数据值
        try:
            p1 = PhoneInfo.objects.get(id=id_i)
        except:
            return HttpResponseRedirect('/msg?t=对应的设备未找到！')

        if p1.CurrState == 11:
            return HttpResponseRedirect('/msg?t=已归还设备不能重复归还')        

        if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_ReturnDevice') or p1.Owner == user:          
            pass
        else:
            op_result = '无归还设备权限'
            return HttpResponseRedirect('/msg?t='+op_result)
        
        p1.CurrState = 11 # 变成可借
        p1.BorrowMan = None
        p1.UpdateDate = int(time.time())
        try:
            p1.save()
        except:
            op_result = '确定归还失败'
            return HttpResponseRedirect('/msg?t='+op_result)
        else:
            op_result = '归还成功'
            p2 = PhoneHisState(PhoneInfo=p1,\
                               CurrState=p1.CurrState,\
                               CreateDate=int(time.time()))

            p2.save()
            #保存日志记录
            SaveLog(user,1007,p1,1)

        return HttpResponseRedirect('/MyDevice')


@login_required
def MyDevMgr_AskBack(request):
    user = request.user
    if True:
        op_result = ''

        id_i = int(request.GET['id'])
        #获取要修改的数据值
        try:
            p1 = PhoneInfo.objects.get(id=id_i)
        except:
            return HttpResponseRedirect('/msg?t=对应的设备未找到！')
        
        if p1.CurrState != 12:
            return HttpResponseRedirect('/msg?t=只有已借出的设备可以催还！')

        if user.username == 'admin' or user.has_perm('PhoneMgr.BorrowedDevice_AskBackDeviceOne') or p1.Owner == user:
            if p1.BorrowMan.email is None:
                return HttpResponseRedirect('/msg?t=借设备用户邮箱为空，无法催还!')

            #MyMail('催还机器:' + p1.PhoneName.encode('utf8'),'有借有还，再接不难啦！',p1.BorrowMan.email)
            send_mail('【测试设备管理】催还机器' + p1.PhoneName.encode('utf8'),\
                '有借有还，再接不难啦！',\
                'cxztest@163.com',\
                [p1.BorrowMan.email,],\
                fail_silently = False
                    )
            return HttpResponseRedirect('/msg?t=发送催还邮件成功')
        else:
            return HttpResponseRedirect('/msg?t=你没有操作权限')

@login_required
def MySimMgr_Borrow(request):
    user = request.user
    if True:  
        op_result = ''
        if request.method == 'POST':
            form = SimInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                #print SimInfo.objects.get(id = 2)
                #这里添加数据
                CurrState = 12  #分配SIM借出
                #获取要修改的数据值
                p1 = SimInfo.objects.get(id = request.POST['p_id'])
                #进行状态检查
                if p1.CurrState == 12:
                    return HttpResponseRedirect('/msg?t=指定的SIM已经借出！')
                
                p1.BorrowMan = User.objects.get(id = int(cd['BorrowMan']))
                p1.BorrowDate = int(time.time())
                p1.IfBorrowAuth = 1
                p1.BorrowAuthMan = user
                p1.CurrState = CurrState
                p1.UpdateDate = int(time.time())

                #进行操作合法性检查
                if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_BorrowSim') or p1.CurrOwner == user:
                    pass
                else:
                    return HttpResponseRedirect('/msg?t=无权进行借出操作！')
                
                try:
                    p1.save()   
                except:
                    op_result = 'SIM借出失败！'
                else:
                    op_result = 'SIM借出成功'

                    p2 = SimHisState(SimInfo=p1,\
                                       BorrowMan = p1.BorrowMan,\
                                       BorrowDate = p1.BorrowDate,\
                                       CurrState=CurrState,\
                                       BorrowAuthMan = p1.BorrowAuthMan,\
                                       CreateDate=int(time.time()))
                    p2.save()
                    #保存日志记录
                    SaveLog(user,3006,p1,3)

                return HttpResponseRedirect('/msg?t='+op_result)
        else:
            id_i = int(request.GET['id'])
            #获取要修改的数据值
            try:
                p1 = SimInfo.objects.get(id=id_i)
            except:
                return HttpResponseRedirect('/msg?t=错误的操作！')

            if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_BorrowSim') or p1.CurrOwner == user:
                pass
            else:
                return HttpResponseRedirect('/msg?t=无权进行借出操作！')
            

            if p1.CurrState == 12:
                return HttpResponseRedirect('/msg?t=已借出的SIM不能重复借出')
            #对待修改的数据进行初始化
            form = SimInfoQue(
                initial = {'PhoneNum':p1.PhoneNum,\
                           'BorrowMan':p1.BorrowMan
                           }
                )
            
        return render_to_response('SimInfo_Borrow.html',{'form':form,
                                                           'op_result':op_result,\
                                                           'p_id':id_i},\
                                  context_instance = RequestContext(request))



@login_required
def MySimMgr_Back(request):
    user = request.user
    if True:
        op_result = ''
        
        id_i = int(request.GET['id'])
        #获取要修改的数据值
        try:
            p1 = SimInfo.objects.get(id=id_i)
        except:
            return HttpResponseRedirect('/msg?t=对应的SIM未找到！')

        if p1.CurrState == 11:
            return HttpResponseRedirect('/msg?t=已归还SIM不能重复归还')        

        if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_ReturnSim') or p1.CurrOwner == user:          
            pass
        else:
            op_result = '无归还SIM权限'
            return HttpResponseRedirect('/msg?t='+op_result)
        
        p1.CurrState = 11 # 变成可借
        p1.BorrowMan = None
        p1.UpdateDate = int(time.time())
        try:
            p1.save()
        except:
            op_result = '确定归还失败'
            return HttpResponseRedirect('/msg?t='+op_result)
        else:
            op_result = '归还成功'
            p2 = SimHisState(SimInfo=p1,\
                               CurrState=p1.CurrState,\
                               CreateDate=int(time.time()))

            p2.save()
            #保存日志记录
            SaveLog(user,3007,p1,3)

        return HttpResponseRedirect('/MyDevice')


@login_required
def MySimMgr_AskBack(request):
    user = request.user
    if True:
        op_result = ''

        id_i = int(request.GET['id'])
        #获取要修改的数据值
        try:
            p1 = SimInfo.objects.get(id=id_i)
        except:
            return HttpResponseRedirect('/msg?t=对应的SIM未找到！')
        
        if p1.CurrState != 12:
            return HttpResponseRedirect('/msg?t=只有已借出的SIM可以催还！')

        if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_AskBackSim') or p1.CurrOwner == user:
            if p1.BorrowMan.email is None:
                return HttpResponseRedirect('/msg?t=借SIM用户邮箱为空，无法催还!')

            #MyMail('催还机器:' + p1.PhoneNum.encode('utf8'),'有借有还，再接不难啦！',p1.BorrowMan.email)
            send_mail('【测试SIM管理】催还SIM' + p1.PhoneNum.encode('utf8'),\
                '有借有还，再接不难啦！',\
                'cxztest@163.com',\
                [p1.BorrowMan.email,],\
                fail_silently = False
                    )
            return HttpResponseRedirect('/msg?t=发送催还邮件成功')
        else:
            return HttpResponseRedirect('/msg?t=你没有操作权限')
