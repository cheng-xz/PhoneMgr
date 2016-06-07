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

@login_required
def SimInfoMgr(request):
    global tag
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_QueSimInfo'):     
        SimInfoResultPre = []
        form = ''
        if request.method == 'POST':
            form = SimInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print 'Query province suc'
                PhoneNum_q = cd['PhoneNum']
                whitelist = int(cd['SimWhiteList'])
                #OsInfo_q = cd['OsInfo']
                if len(PhoneNum_q) == 0: #如果没有填写查询项
                    SimInfoResultPre = SimInfo.objects.filter(Carrier=cd['CarrierInfo'])
                    #print SimInfoResult
                else:
                    SimInfoResultPre = SimInfo.objects.filter(PhoneNum__icontains=PhoneNum_q,Carrier=cd['CarrierInfo'])

                #这里对白名单数据过滤
                SimInfoResult = []
                for pp in SimInfoResultPre:
                    if pp.SimWhiteList.id == whitelist:
                        SimInfoResult.append(pp)
                    
                tag = SimInfoResult               
        else:
            SimInfoResult = SimInfo.objects.all()
            if 'page' in request.GET:
                if tag is not None:
                    SimInfoResult = tag
            else:
                tag = SimInfoResult
                
            form = SimInfoQue()
        
        return render_to_response('SimInfo.html',{'form':form,'SimInfoResult':SimInfoResult,'MainMenu':MainMenu},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无操作权限') 

@login_required
def SimInfoMgr_Del(request):
    user = request.user
    try:
        id_i = int(request.GET['id'])
    except:
        return HttpResponseRedirect('/msg?t=请求参数有误')
    else:
        if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_AddNewSim'):
            try:
                p1 = SimInfo.objects.get(id=id_i)
            except:
                return HttpResponseRedirect('/msg?t=指定的sim卡不存在')
        else:
            return HttpResponseRedirect('/msg?t=无操作权限')
        try:
	    #保存日志记录
            SaveLog(user,3003,p1,3)

            p1.delete()
        except:
            return HttpResponseRedirect('/msg?t=删除失败')
        else:
            return HttpResponseRedirect('/SimInfo')

    return render_to_response('SimInfo.html',{'form':form,'SimInfoResult':SimInfoResult,'MainMenu':MainMenu},\
                                  context_instance = RequestContext(request))        


@login_required
def SimInfoMgr_Add(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_AddNewSim'):         
        SimInfo_add_result = ''
        if request.method == 'POST':
            form = SimInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                #print SimInfo.objects.get(id = 2)
                #这里添加数据
                #print cd['ProvinceInfo'],cd['CarrierInfo']
                CurrState = 11
                if int(cd['CurrOwner']) == 0:
                        CurrOwner = None
                else:
                        CurrOwner = User.objects.get(id = int(cd['CurrOwner']))
                    
                p1 = SimInfo(PhoneNum=cd['PhoneNum'],\
                             Province=Province.objects.get(id = int(cd['ProvinceInfo'])),\
                             Carrier=Carrier.objects.get(id = int(cd['CarrierInfo'])),\
                             IMSI=cd['IMSI'],\
                             CurrOwner = CurrOwner,\
                             CurrState = CurrState,\
                             ServerPass = cd['ServerPass'],\
                             SimWhiteList = SimWhiteList.objects.get(id = int(cd['SimWhiteList'])),\
                             SimAbout = cd['SimAbout']
                               )    
                try:
                    p1.save()   
                except:
                    SimInfo_add_result = '添加数据失败！'
                    traceback.print_exc()
                else:
                    SimInfo_add_result = '添加成功'
                    #添加成功后在手机状态表中添加一条记录
                    #if p1.CurrOwner is None: #没有归属人
                    #    p2 = SimCurrState(SimInfo=p1,CurrState=0)
                    #else:
                    #    p2 = SimCurrState(SimInfo=p1,CurrState=1)
                    p2 = SimHisState(SimInfo=p1,CurrState=CurrState)
                    p2.save()
		    #保存日志记录
		    SaveLog(user,3001,p1,3)

                #print SimInfo_add_result.decode('utf8').encode('gbk')
                return HttpResponseRedirect('/msg?t='+SimInfo_add_result)
        else:
            form = SimInfoQue()
            
        return render_to_response('SimInfo_add.html',{'form':form,'SimInfo_add_result':SimInfo_add_result},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无操作权限')


@login_required
def SimInfoMgr_Mod(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_UpdateSimInfo'):
        
        SimInfo_mod_result = ''
        if request.method == 'POST':
            #print request
            form = SimInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                CurrState = 0
                if int(cd['CurrOwner']) == 0:
                    CurrOwner = None
                else:
                    CurrOwner = User.objects.get(id = int(cd['CurrOwner']))
                    CurrState = 1
                
                p1 = SimInfo.objects.get(id = request.POST['p_id'])
                p1.PhoneNum = cd['PhoneNum']
                p1.Province = Province.objects.get(id = int(cd['ProvinceInfo']))
                p1.Carrier = Carrier.objects.get(id = int(cd['CarrierInfo']))
                p1.IMSI = cd['IMSI']
                p1.CurrOwner = CurrOwner
                p1.ServerPass = cd['ServerPass']
                p1.SimWhiteList = SimWhiteList.objects.get(id = int(cd['SimWhiteList']))
                p1.SimAbout = cd['SimAbout']
            
                try:
                    p1.save()
                except:
                    SimInfo_mod_result = '修改数据失败'
                else:
                    SimInfo_mod_result = '修改数据成功'
                    #修改sim状态表的内容
                    #p2 = p1.simcurrstate_set.all()[0]
                    #if CurrOwner is None:
                    #    #print p2
                    #    p2.CurrState = 0
                    #else:
                    #    p2.CurrState = 1
                    p2 = SimHisState(SimInfo=p1,CurrState = CurrState)
                    p2.save()
		    #保存日志记录
		    SaveLog(user,3002,p1,3)

                return HttpResponseRedirect('/msg?t='+SimInfo_mod_result)
        else:
            id_i = int(request.GET['id'])
            #获取要修改的数据值
            try:
                p1 = SimInfo.objects.get(id=id_i)
            except:
                return HttpResponseRedirect('/msg?t=错误的操作！')
            #对待修改的数据进行初始化
            form = SimInfoQue(
                initial = {'PhoneNum':p1.PhoneNum,\
                           'ProvinceInfo':p1.Province.id,\
                           'CarrierInfo':p1.Carrier.id,\
                           'IMSI':p1.IMSI,\
                           'CurrOwner':p1.CurrOwner,\
                           'ServerPass':p1.ServerPass,\
                           'SimWhiteList':p1.SimWhiteList.id,\
                           'SimAbout':p1.SimAbout
                           },
            
                )
        return render_to_response('SimInfo_mod.html',{'form':form,\
                                                        'SimInfo_mod_result':SimInfo_mod_result,\
                                                        'p_id':id_i},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无操作权限')


    
@login_required
def SimInfoMgr_Assign(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_AssignSim'):          
        result = ''
        if request.method == 'POST':
            form = SimInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                #print SimInfo.objects.get(id = 2)
                #这里添加数据
                #CurrState = 1
                #获取要修改的数据值
                p1 = SimInfo.objects.get(id = request.POST['p_id'])
                p1.CurrOwner = User.objects.get(id = int(cd['CurrOwner']))
                #p1.CurrState = CurrState
                p1.BorrowMan = None
                p1.BorrowDate = None
                p1.UpdateDate = int(time.time())
                try:
                    p1.save()   
                except:
                    result = '分配SIM失败！'
                else:
                    result = '分配成功'

                    #p2 = SimHisState(SimInfo=p1,\
                    #                   CurrState=CurrState,\
                    #                   CreateDate=int(time.time()))
                    #p2.save()
                    #保存日志记录
		    SaveLog(user,3004,p1,3)

                return HttpResponseRedirect('/msg?t='+result)
        else:
            id_i = int(request.GET['id'])
            #获取要修改的数据值
            try:
                p1 = SimInfo.objects.get(id=id_i)
            except:
                return HttpResponseRedirect('/msg?t=指定的SIM未找到！')
            if p1.CurrState != 11:
                return HttpResponseRedirect('/msg?t=不是可借状态的SIM不能分配！')
            #IfSimI = 0
            #if p1.IfSim:
            #    IfSimI = 1
            #对待修改的数据进行初始化
            form = SimInfoQue(
                initial = {'PhoneNum':p1.PhoneNum,\
                           'CurrOwner':p1.CurrOwner
                           }
                )
            
        return render_to_response('SimInfo_Assign.html',{'form':form,
                                                           'result':result,\
                                                           'p_id':id_i},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无权进行分配SIM操作！')


@login_required
def SimInfoMgr_UnAssign(request):
    user = request.user 
    if user.username == 'admin' or user.has_perm('PhoneMgr.SimMaintain_CancelAssignSim'):          
        op_result = ''
        
        id_i = int(request.GET['id'])
        #获取要修改的数据值
        try:
            p1 = SimInfo.objects.get(id=id_i)
        except:
            return HttpResponseRedirect('/msg?t=指定的SIM不存在！')

        if p1.CurrState == 12:
            return HttpResponseRedirect('/msg?t=先将SIM归还再取消分配')

        #if user.username == 'admin' or (p1.CurrOwner is not None and p1.CurrOwner == user):
        #    pass
        #else:
        #    op_result = '不是SIM归属者不能上交'
        #    return HttpResponseRedirect('/msg?t='+op_result)        

        p1.CurrOwner = None
        p1.CurrState = 11 # 变成可借状态
        p1.BorrowMan = None
        p1.BorrowDate = None
        p1.BorrowAuthMan = None
        p1.BackMan = None
        p1.BackDate = None
        p1.BackAuthMan = None
        p1.UpdateDate = int(time.time())
        try:
            p1.save()
        except:
            op_result = '取消分配失败'
            return HttpResponseRedirect('/msg?t='+op_result)
        else:
            op_result = '取消分配成功'
            p2 = SimHisState(SimInfo=p1,\
                               CurrState=p1.CurrState,\
                               CreateDate=int(time.time()))

            p2.save()
            #保存日志记录
	    SaveLog(user,3005,p1,3)

        return HttpResponseRedirect('/SimInfo')
    else:
        return HttpResponseRedirect('/msg?t=无权进行取消分配操作！')

@login_required
def SimInfoMgr_Borrow(request):
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
def SimInfoMgr_Back(request):
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

        return HttpResponseRedirect('/SimInfo')


@login_required
def SimInfoMgr_AskBack(request):
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

