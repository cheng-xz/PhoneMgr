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
from viewsPub import MainMenu,RepeatList,SaveLog

tag = None


@login_required
def UserInfoMgr(request):
    global tag
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.UserMgr_QueUserInfo'):
        UserInfoResult = ''
        if request.method == 'POST':
            search = request.POST['search']
            if len(search) == 0 or search == '搜索…'.decode('utf8'): #如果没有填写查询项
                UserInfoResult = UserInfo.objects.all()
            else:
                #通过user表的username
                R1 = []
                p = User.objects.filter(username__icontains = search)
                if len(p) != 0:
                    for p0 in p:
                        try:
                            for p1 in p0.r_1000.all():
                                R1.append(p1)
                        except:
                            pass
                #通过username表engname
                R2 = UserInfo.objects.filter(EngName__icontains = search)
                #加入中文名搜索
                R3 = UserInfo.objects.filter(ChnName__icontains = search)
                #加入部门搜索
                R4 = UserInfo.objects.filter(Dept__icontains = search)

                #结果合并
                R = R1
                [R.append(r2) for r2 in R2]
                [R.append(r3) for r3 in R3]
                [R.append(r4) for r4 in R4]
                #for r2 in R2:
                #    R.append(r2)
                #for r3 in R3:
                #    R.append(r3)
                #for r4 in R4:
                #    R.append(r4)
                #结果剔重
                UserInfoResult = RepeatList(R)

            tag = UserInfoResult
                
        else:
            UserInfoResult = UserInfo.objects.all()
            try:
                page = int(request.GET['page'])
            except:
                tag = UserInfoResult
            else:
                if page > 0 and tag is not None:
                    UserInfoResult = tag
                    

        #print UserInfoResult
        #groupsname = []
        #for userinfo in UserInfoResult:
        #    print userinfo.Userid.id,userinfo.EngName,userinfo.Userid.groups.all()[0].name
        #    groupsname.append(userinfo.Userid.groups.all()[0].name)
        
        #print groupsname
        #print type(UserInfoResult)
        #MenuItem = MainMenu[0]
        #print MenuItem.AuthMenuId.codename
        #print user.get_all_permissions()
        #print 'PhoneMgr.'+MenuItem.AuthMenuId.codename in user.get_all_permissions()
        #这里增加一个查询消息
        #messages.success(request,"你在用户界面做了查询操作")
        
        return render_to_response('UserInfo.html',{'UserInfoResult':UserInfoResult,'MainMenu':MainMenu},\
                              context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无权操作！')
            

@login_required
def UserInfoMgr_Del(request):
    global tag    
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.UserMgr_DelUserInfo'):
        try:
           id_i = int(request.GET['id'])
        except:
            result = UserInfo.objects.all()
            try:
                page = int(request.GET['page'])
            except:
                tag = result
            else:
                if page > 0 and tag is not None:
                    result = tag
        else:
            try:
                p1 = UserInfo.objects.get(id=id_i)
                p2 = p1.Userid
            except:
                return HttpResponseRedirect('/msg?t=无效的用户')
            #判断是否本人
            if p2 == user:
                return HttpResponseRedirect('/msg?t=不能删除本人')

            try:
                #保存日志
                SaveLog(user,2003,p2,2)
                p1.delete()
                p2.delete()
            except:
                return HttpResponseRedirect('/msg?t=删除用户失败')
            else:
                return HttpResponseRedirect('/UserMgr')
            
        return render_to_response('UserInfo.html',{'UserInfoResult':result,'MainMenu':MainMenu},\
                              context_instance = RequestContext(request))
           
    else:
        return HttpResponseRedirect('/msg?t=无权操作！')
    

@login_required
def UserInfoMgr_Add(request):
    global tag
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.UserMgr_CanReg') or user in [p.Owner for p in PhoneInfo.objects.all()]:
        UserInfo_add_result = ''
        if request.method == 'POST':
            form = UserInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
                #print SimInfo.objects.get(id = 2)
                #生成一个用户
                try:
                    user1 = User.objects.create_user(username=cd['username'],\
                                                    email=cd['email'],\
                                                    password=cd['passwd'])
                    user1.save()
                except:
                    UserInfo_add_result = '添加用户失败！'
                    return HttpResponseRedirect('/msg?t='+UserInfo_add_result)
                #添加组
                group = Group.objects.get(id = int(cd['Group']))
                user1.groups.add(group)
                #添加到用户组中
                p1 = UserInfo(Userid=user1,\
                              EngName = cd ['EngName'],\
                              ChnName = cd['ChnName'],\
                              Dept = cd['Dept'],\
                              UserInfoAbout = cd['UserInfoAbout'],\
                              IsCheck = 1)
                try:
                    p1.save()
                except Exception,e:
                    UserInfo_add_result = '添加用户失败！'
                    #print e
                    #traceback.print_exc()
                else:
                    UserInfo_add_result = '添加用户成功'
                    #保存日志
                    SaveLog(user,2001,user1,2)

                return HttpResponseRedirect('/msg?t='+UserInfo_add_result)
        else:
            form = UserInfoQue(
                initial = {
                           'Group':2,\
                           },
                )
            
        return render_to_response('UserInfo_add.html',{'form':form,'PhoneInfo_add_result':UserInfo_add_result},\
                              context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无权操作！')

@login_required
def UserInfoMgr_Mod(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.UserMgr_UpdateUserInfo'):
        UserInfo_mod_result = ''
        if request.method == 'POST':
            #print request
            form = UserInfoQue(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #print cd
            
                p1 = UserInfo.objects.get(id = request.POST['p_id'])
                p2 = p1.Userid
                
                p1.EngName = cd['EngName']
                p1.ChnName = cd['ChnName']
                p1.Dept = cd['Dept']
                p1.UserInfoAbout = cd['UserInfoAbout']

                #修改系统表信息
                p2.username = cd['username']
                if len(cd['passwd']) == 0:
                    pass
                else:
                    p2.set_password(cd['passwd'])
                p2.email = cd['email']
                p2.username = cd['username']
                #添加组
                group = Group.objects.get(id = int(cd['Group']))
                p2.groups.clear()
                p2.groups.add(group)
            
                try:
                    p1.save()
                    p2.save()
                except:
                    UserInfo_mod_result = '修改数据失败'
                else:
                    UserInfo_mod_result = '修改数据成功'
                    #保存日志
                    SaveLog(user,2002,p2,2)

                return HttpResponseRedirect('/msg?t='+UserInfo_mod_result)
        else:
            id_i = int(request.GET['id'])
            #获取要修改的数据值
            try:
                p1 = UserInfo.objects.get(id=id_i)
            except:
                return HttpResponseRedirect('/msg?t=错误的操作！')
            p2 = p1.Userid
            #对待修改的数据进行初始化
            #print 'aaa:',len(p2.groups.all())
            if len(p2.groups.all()) == 0:
                groupid = 1
            else:
                groupid = p2.groups.all()[0].id
            form = UserInfoQue(
                initial = {'username':p2.username,\
                           'EngName':p1.EngName,\
                           'ChnName':p1.ChnName,\
                           'Dept':p1.Dept,\
                           'passwd':'',\
                           'email':p2.email,\
                           'Group':groupid,\
                           'UserInfoAbout':p1.UserInfoAbout
                           },
            
                )
        return render_to_response('UserInfo_mod.html',{'form':form,\
                                                        'User_mod_result':UserInfo_mod_result,\
                                                        'p_id':id_i},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无权操作！')   
