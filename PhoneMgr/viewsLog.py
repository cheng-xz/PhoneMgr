from django.http import HttpResponse
from django.shortcuts import render_to_response,RequestContext,HttpResponseRedirect
from formQue import *
from models import *
import time,traceback,datetime
from django.core.mail import send_mail
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
import traceback
#from django.db.models import F  

#导入公共模块
from viewsPub import MainMenu


@login_required
def LogView(request):
    user = request.user
    if user.username == 'admin' or user.has_perm('PhoneMgr.LogView_LogViewMenu'):
        #这里处理分页
        ONE_PAGE_OF_DATA = 10
        try:
            curPage = int(request.GET.get('curPage','1'))
            allPage = int(request.GET.get('allPage','1'))
            pageType = str(request.GET.get('pageType',''))
        except ValueError:
            curPage = 1
            alllPage = 1
            pageType = ''
        if pageType == 'pageDown':
            curPage += 1
        elif pageType == 'pageUp':
            curPage -= 1
        startPos = (curPage - 1)*ONE_PAGE_OF_DATA
        endPos = startPos + ONE_PAGE_OF_DATA

        
        LogInfoResult = ''
        if request.method == 'POST':
            #print request.POST
            
            startdate = request.POST['logstart']
            enddate = request.POST['logend']
            phone = request.POST['phone']
            #print 'log:%s,%s' % (startdate,enddate)
            if len(startdate) != 0 and len(enddate) != 0:
                try:
                    startdate_i = time.mktime(time.strptime(startdate+' 00:00:00','%Y-%m-%d %H:%M:%S'))
                    enddate_i = time.mktime(time.strptime(enddate+' 23:59:59','%Y-%m-%d %H:%M:%S'))
                except:
                    #获取当前时间
                    dt = datetime.datetime.now()
                    tt = dt.timetuple()
                    #设置当天的开始时间和结束时间
                    curr_date_str = '%d-%d-%d' % (tt[0],tt[1],tt[2])
                    #生成当天整天的开始时间和结束时间
                    startdate_i = time.mktime(time.strptime(curr_date_str + '00:00:00','%Y-%m-%d %H:%M:%S'))
                    enddate_i = time.mktime(time.strptime(curr_date_str + '23:59:59','%Y-%m-%d %H:%M:%S'))

                #print '%d,%d' % (startdate_i,enddate_i)
                if user.has_perm('PhoneMgr.LogView_AccessOtherLog'):
                    LogInfoResult = LogInfo.OrderObjects.filter(CreateDate__gt=startdate_i,CreateDate__lt = enddate_i)[startPos:endPos]
                    LogInfoAll = LogInfo.OrderObjects.filter(CreateDate__gt=startdate_i,CreateDate__lt = enddate_i)
                else:
                    LogInfoResult = LogInfo.OrderObjects.filter(CreateDate__gt=startdate_i,CreateDate__lt = enddate_i,UserName=user.username)[startPos:endPos]
                    LogInfoAll = LogInfo.OrderObjects.filter(CreateDate__gt=startdate_i,CreateDate__lt = enddate_i,UserName=user.username)
            else:
                if len(phone) != 0:
                    #LogInfoResult = []
                    #p = PhoneInfo.objects.filter(PhoneName__icontains = phone)
                    #print p
                    #for p0 in p:
                    #    #print 'p0 is: ',dir(p0)
                    #    for p1 in p0.r_1030.all():
                    #        LogInfoResult.append(p1)
                    #print LogInfoResult
                    if user.has_perm('PhoneMgr.LogView_AccessOtherLog'):
                        LogInfoResult = LogInfo.OrderObjects.filter(PhoneName__icontains = phone)[startPos:endPos]
                        LogInfoAll = LogInfo.OrderObjects.filter(PhoneName__icontains = phone)
                    else:
                        LogInfoResult = LogInfo.OrderObjects.filter(PhoneName__icontains = phone,UserName=user.username)[startPos:endPos]
                        LogInfoAll = LogInfo.OrderObjects.filter(PhoneName__icontains = phone,UserName=user.username)
                else:
                    if user.has_perm('PhoneMgr.LogView_AccessOtherLog'):
                        LogInfoResult = LogInfo.OrderObjects.all()[startPos:endPos]
                        LogInfoAll = LogInfo.OrderObjects.all()
                    else:
                        LogInfoResult = LogInfo.OrderObjects.filter(UserName=user.username)[startPos:endPos]
                        LogInfoAll = LogInfo.OrderObjects.filter(UserName=user.username)
                
        else:
        
            #这里处理分页的相关数据
            if user.has_perm('PhoneMgr.LogView_AccessOtherLog'):
                LogInfoResult = LogInfo.OrderObjects.all()[startPos:endPos]
                LogInfoAll = LogInfo.OrderObjects.all()
            else:
                LogInfoResult = LogInfo.OrderObjects.filter(UserName=user.username)[startPos:endPos]
                LogInfoAll = LogInfo.OrderObjects.filter(UserName=user.username)

        #这里进行全部页处理
        if curPage == 1 and allPage == 1:
            allPostCounts = LogInfoAll.count()
            allPage = allPostCounts / ONE_PAGE_OF_DATA
            remainPost = allPostCounts % ONE_PAGE_OF_DATA
            if remainPost > 0:
                allPage += 1
        return render_to_response('LogInfo.html',{'LogInfoResult':LogInfoResult,'MainMenu':MainMenu,\
                                                  'allPage':allPage,\
                                                  'curPage':curPage},\
                                  context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/msg?t=无操作权限') 
