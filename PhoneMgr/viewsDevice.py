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
from django.contrib import messages

#导入公共模块
from viewsPub import SaveLog,MainMenu,RepeatList

tag = None

#这里的设备主要是手机
@login_required
def DeviceMaintainMgr(request):
    global tag 
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_QueAllDevice'):    
        PhoneInfoResult = ''
        if request.method == 'POST':
            search = request.POST['search']
            q_status = request.POST['device_status']
            q_status = int(q_status)
            #print q_status
            
            if len(search) == 0 or  search == '搜索…'.decode('utf8'): #如果没有填写查询项
                PhoneInfoResultPre = PhoneInfo.objects.all()
            else:
                #通过手机名称搜索
                R10 = PhoneInfo.objects.filter(PhoneName__icontains = search)
                #通过系统搜索
                R20 = []
                p = OsInfo.objects.filter(OsName__icontains = search)
                if len(p) != 0:
                    for p0 in p:
                        for p1 in p0.r_1005.all():
                            R20.append(p1)
                #通过厂商搜索
                R21 = []
                p = ProductInfo.objects.filter(ProductName__icontains = search)
                if len(p) != 0:
                    for p0 in p:
                        for p1 in p0.r_1001.all():
                            R21.append(p1)
                #通过OS版本号搜索
                R22 = []
                p = OsVersionInfo.objects.filter(OsVersionName__icontains = search)
                if len(p) != 0:
                    for p0 in p:
                        for p1 in p0.r_1006.all():
                            R22.append(p1)
                #通过主屏尺寸
                R23 = []
                p = ScreenSizeInfo.objects.filter(ScreenSizeName__icontains = search)
                if len(p) != 0:
                    for p0 in p:
                        for p1 in p0.r_1002.all():
                            R23.append(p1)
                #通过分辨率
                R24 = []
                p = ResolutionInfo.objects.filter(ResolutionName__icontains = search)
                if len(p) != 0:
                    for p0 in p:
                        for p1 in p0.r_1003.all():
                            R24.append(p1)
                #通过内存
                R25 = []
                p = MemoryInfo.objects.filter(MemorySize__icontains = search)
                if len(p) != 0:
                    for p0 in p:
                        for p1 in p0.r_1004.all():
                            R25.append(p1)

                #通过CPU型号
                R11 = PhoneInfo.objects.filter(CpuType__icontains = search)
                #通过归属人
                R26 = []
                p = User.objects.filter(username__icontains = search)
                if len(p) != 0:
                    for p0 in p:
                        for p1 in p0.r_1007.all():
                            R26.append(p1)                
                
                #合并结果
                R = R20 + R21 + R22 + R23 + R24 + R25 + R26
                [R.append(r10) for r10 in R10]
                [R.append(r11) for r11 in R11]
                
                PhoneInfoResultPre = RepeatList(R)
            
            #这里对最终的结果根据设备状态进行过滤
            PhoneInfoResult = []
            for pp in PhoneInfoResultPre:
                if pp.CurrState == q_status or q_status == 13:
                    PhoneInfoResult.append(pp)
                    

            tag = PhoneInfoResult

            #这里查询完后推送一条消息，将当前的选择框的值保存下来
            messages.add_message(request,messages.INFO,str(q_status))
        else:
            PhoneInfoResult = PhoneInfo.objects.all()
            #PhoneInfoResult = PhoneInfo.iosObjects.all()

            try:
                page = int(request.GET['page'])
            except:
                tag = PhoneInfoResult
            else:
                if page > 0 and tag is not None:
                    PhoneInfoResult = tag

            #messages.add_message(request, messages.INFO, '设备管理查询操作')
                

        return render_to_response('Device.html',{'PhoneInfoResult':PhoneInfoResult,'MainMenu':MainMenu},\
                              context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无权操作！')

@login_required
def DeviceMaintainMgr_Del(request):
    global tag 
    user = request.user
    try:
        id_i = int(request.GET['id'])
    except: #未进行操作字段提交
        return HttpResponseRedirect('/msg?t=指定参数出错')
    else:
        try:
            p1 = PhoneInfo.objects.get(id=id_i)
        except:
            return HttpResponseRedirect('/msg?t=指定的手机不存在！')
        if p1.CurrState == 12:
            return HttpResponseRedirect('/msg?t=已借出的设备不能删除')

        if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_AddNewDevice'):
            try:
                #保存日志记录
                SaveLog(user,1003,p1,1)
                p1.delete()
            except:
                return HttpResponseRedirect('/msg?t=删除失败')
            else:
                return HttpResponseRedirect('/DeviceMaintain')
        else:
            return HttpResponseRedirect('/msg?t=无权操作!')

        
    return render_to_response('Device.html',{'PhoneInfoResult':PhoneInfoResult,'MainMenu':MainMenu},\
                              context_instance = RequestContext(request))
    

@login_required
def DeviceMaintainMgr_Add(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_AddNewDevice'):      
        PhoneInfo_add_result = ''
        if request.method == 'POST':
            form = PhoneInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                #print SimInfo.objects.get(id = 2)
                #这里添加数据
                CurrState = 0
                if int(cd['Owner']) == 0:
                    owner = None
                    CurrState = 11
                else:
                    owner = User.objects.get(id = int(cd['Owner']))
                    CurrState = 11
                    
                p1 = PhoneInfo(PhoneName=cd['PhoneName'],\
                               ProductInfo=ProductInfo.objects.get(id= int(cd['ProductInfo'])),\
                               #ModelInfo=ModelInfo.objects.get(id = int(cd['ModelInfo'])),\
                               OsInfo=OsInfo.objects.get(id = int(cd['OsInfo'])),\
                               OsVersionInfo=OsVersionInfo.objects.get(id = int(cd['OsVersionInfo'])),\
                               CpuType = cd['CpuType'],\
                               CpuCoreNum = int(cd['CpuCoreNum']),\
                               ScreenSizeInfo = ScreenSizeInfo.objects.get(id = int(cd['ScreenSizeInfo'])),
                               ResolutionInfo=ResolutionInfo.objects.get(id = int(cd['ResolutionInfo'])),\
                               MemoryInfo=MemoryInfo.objects.get(id = int(cd['MemoryInfo'])),\
                               IMEI=cd['IMEI'],\
                               #IfSim=int(cd['IfSim']),\
                               #SimInfo=SimInfo.objects.get(id = int(cd['SimInfo'])),\
                               #健康状态默认正常
                               HealthState = 0,\
                               IfTel = int(cd['IfTel']),\
                               Owner=owner,\
                               CurrState = CurrState,\
                               FundId=cd['FundId'],\
                               About = cd['About'],\
                               CreateDate=int(time.time()),\
                               UpdateDate=int(time.time())
                               )
                #print p1
                try:
                    p1.save()   
                except Exception,e:
                    PhoneInfo_add_result = '[设备维护]添加数据失败！'
                    #traceback.print_exc()
                    #print e
                else:
                    PhoneInfo_add_result = '添加成功'
                
                    #添加成功后在手机状态表中添加一条记录
                    #if p1.Owner is None: #没有归属人
                    #    p2 = PhoneCurrState(PhoneInfo=p1,\
                    #                    CurrState=0)
                    #else:
                    #    p2 = PhoneCurrState(PhoneInfo=p1,\
                    #                CurrState=1)
                    #p2.save()
                    p2 = PhoneHisState(PhoneInfo=p1,CurrState = CurrState,CreateDate=int(time.time()))
                    p2.save()
                    #保存日志记录
                    SaveLog(user,1001,p1,1)
                    

                return HttpResponseRedirect('/msg?t='+PhoneInfo_add_result)
        else:
            form = PhoneInfoQue()
            
        return render_to_response('Device_add.html',{'form':form,'PhoneInfo_add_result':PhoneInfo_add_result},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=缺少相关操作权限')


@login_required
def DeviceMaintainMgr_Mod(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_UpdateDeviceState'):          
        PhoneInfo_mod_result = ''
        if request.method == 'POST':
            #print request
            form = PhoneInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                #if int(cd['Owner']) == 0:
                #    owner = None
                #else:
                #    owner = User.objects.get(id = int(cd['Owner']))
            
                p1 = PhoneInfo.objects.get(id = request.POST['p_id'])
                p1.PhoneName = cd['PhoneName']
                p1.ProductInfo = ProductInfo.objects.get(id = int(cd['ProductInfo']))
                #p1.ModelInfo = ModelInfo.objects.get(id = int(cd['ModelInfo']))
                p1.OsInfo = OsInfo.objects.get(id = int(cd['OsInfo']))
                p1.OsVersionInfo = OsVersionInfo.objects.get(id = int(cd['OsVersionInfo']))
                p1.CpuType = cd['CpuType']
                p1.CpuCoreNum = int(cd['CpuCoreNum'])
                p1.ResolutionInfo = ResolutionInfo.objects.get(id = int(cd['ResolutionInfo']))
                p1.ScreenSizeInfo = ScreenSizeInfo.objects.get(id = int(cd['ScreenSizeInfo']))
                p1.MemoryInfo = MemoryInfo.objects.get(id = int(cd['MemoryInfo']))
                p1.IMEI = cd['IMEI']
                p1.IfTel = int(cd['IfTel'])
                #p1.IfSim = int(cd['IfSim'])
                #p1.SimInfo = SimInfo.objects.get(id = int(cd['SimInfo']))
                #p1.Owner = owner
                p1.FundId = cd['FundId']
                p1.HealthState = int(cd['HealthState'])
                p1.About = cd['About']
                p1.UpdateDate = int(time.time())
            
                try:
                    p1.save()
                except:
                    PhoneInfo_mod_result = '修改数据失败'
                else:
                    PhoneInfo_mod_result = '修改数据成功'
                    #保存日志记录
                    SaveLog(user,1002,p1,1)

                return HttpResponseRedirect('/msg?t='+PhoneInfo_mod_result)
        else:
            id_i = int(request.GET['id'])
            #获取要修改的数据值
            try:
                p1 = PhoneInfo.objects.get(id=id_i)
            except:
                return HttpResponseRedirect('/msg?t=错误的操作！')
            #IfSimI = 0
            #if p1.IfSim:
            #    IfSimI = 1
            #对待修改的数据进行初始化
            form = PhoneInfoQue(
                initial = {'PhoneName':p1.PhoneName,\
                           'ProductInfo':p1.ProductInfo.id,\
                           #'ModelInfo':p1.ModelInfo.id,\
                           'OsInfo':p1.OsInfo.id,\
                           'OsVersionInfo':p1.OsVersionInfo.id,\
                           'ResolutionInfo':p1.ResolutionInfo.id,\
                           'ScreenSizeInfo':p1.ScreenSizeInfo.id,\
                           'CpuType':p1.CpuType,\
                           'CpuCoreNum':p1.CpuCoreNum,\
                           'IMEI':p1.IMEI,\
                           'FundId':p1.FundId,\
                           'IfTel':p1.IfTel,\
                           #'IfSim':IfSimI,\
                           #'SimInfo':p1.SimInfo.id,\
                           #'Owner':p1.Owner,\
                           'HealthState':p1.HealthState,\
                           'About':p1.About,\
                           'MemoryInfo':p1.MemoryInfo.id
                           },
            
                )
        return render_to_response('Device_mod.html',{'form':form,\
                                                        'PhoneInfo_mod_result':PhoneInfo_mod_result,\
                                                        'p_id':id_i},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=缺少相关操作权限')

@login_required
def DeviceMaintainMgr_Assign(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_AssignDevice'):          
        PhoneInfo_assign_result = ''
        if request.method == 'POST':
            form = PhoneInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                #print SimInfo.objects.get(id = 2)
                #这里添加数据
                #CurrState = 1
                #获取要修改的数据值
                p1 = PhoneInfo.objects.get(id = request.POST['p_id'])
                p1.Owner = User.objects.get(id = int(cd['Owner']))
                #p1.CurrState = CurrState
                p1.BorrowMan = None
                p1.BorrowDate = None
                p1.UpdateDate = int(time.time())
                try:
                    p1.save()   
                except:
                    PhoneInfo_assign_result = '分配设备失败！'
                else:
                    PhoneInfo_assign_result = '分配成功'

                    #p2 = PhoneHisState(PhoneInfo=p1,\
                    #                   CurrState=CurrState,\
                    #                   CreateDate=int(time.time()))
                    #p2.save()
                    #保存日志记录
                    SaveLog(user,1004,p1,1)

                return HttpResponseRedirect('/msg?t='+PhoneInfo_assign_result)
        else:
            id_i = int(request.GET['id'])
            #获取要修改的数据值
            try:
                p1 = PhoneInfo.objects.get(id=id_i)
            except:
                return HttpResponseRedirect('/msg?t=指定的设备未找到！')
            if p1.CurrState != 11:
                return HttpResponseRedirect('/msg?t=不是可借状态的设备不能分配！')
            #IfSimI = 0
            #if p1.IfSim:
            #    IfSimI = 1
            #对待修改的数据进行初始化
            form = PhoneInfoQue(
                initial = {'PhoneName':p1.PhoneName,\
                           'Owner':p1.Owner
                           }
                )
            print 'hello'
            
        return render_to_response('Device_Assign.html',{'form':form,
                                                           'PhoneInfo_assign_result':PhoneInfo_assign_result,\
                                                           'p_id':id_i},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无权进行分配设备操作！')


@login_required
def DeviceMaintainMgr_UnAssign(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_CancelAssignDevice'):          
        op_result = ''
        
        id_i = int(request.GET['id'])
        #获取要修改的数据值
        try:
            p1 = PhoneInfo.objects.get(id=id_i)
        except:
            return HttpResponseRedirect('/msg?t=指定的设备不存在！')

        if p1.CurrState == 12:
            return HttpResponseRedirect('/msg?t=先将设备归还再取消分配')

        #if user.username == 'admin' or (p1.Owner is not None and p1.Owner == user):
        #    pass
        #else:
        #    op_result = '不是设备归属者不能上交'
        #    return HttpResponseRedirect('/msg?t='+op_result)        

        p1.Owner = None
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
            p2 = PhoneHisState(PhoneInfo=p1,\
                               CurrState=p1.CurrState,\
                               CreateDate=int(time.time()))

            p2.save()
            #保存日志记录
            SaveLog(user,1005,p1,1)

        return HttpResponseRedirect('/DeviceMaintain')
    else:
        return HttpResponseRedirect('/msg?t=无权进行取消分配操作！')

@login_required
def DeviceMaintainMgr_Borrow(request):
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
def DeviceMaintainMgr_Back(request):
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

        return HttpResponseRedirect('/DeviceMaintain')


@login_required
def DeviceMaintainMgr_AskBack(request):
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

        if user.username == 'admin' or user.has_perm('PhoneMgr.DeviceMaintain_AskBackDevice') or p1.Owner == user:
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

