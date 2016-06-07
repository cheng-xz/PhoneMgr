from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from views import *
import settings   

#add admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login,logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PhoneMgr.views.home', name='home'),
    # url(r'^PhoneMgr/', include('PhoneMgr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #config javascript path                    
    #url(r'^myjs/(?P<path>.*)$','django.views.static.serve',
    #    {'document_root':settings.STATIC_ROOT}
    #    ),
    #url(r'^img/(?P<path>.*)$','django.views.static.serve',
    #    {'document_root':settings.STATIC_ROOT}
    #    ),
    #url(r'^css/(?P<path>.*)$','django.views.static.serve',
    #    {'document_root':settings.STATIC_ROOT}
    #    ),                          
    #process download request
    url(r'view/(?P<path>.*)$','django.views.static.serve',
        {'document_root':'/home/mypy/PhoneMgr/v4','show_indexes':True}
        ),                    
    #config main interface
    #url(r'^int/(\d{1,2})/$',int_process),                       
    #                       
    url(r'admin/', include(admin.site.urls)),
    #处理登陆和登出
    url('^accounts/login/$',login),
    url('^mylogout/$',mylogout),
    #首页                       
    url(r'^$',homepage),
    #处理用户
    url(r'^UserMgr[\/]?$',UserInfoMgr),
    url(r'^UserMgr/Add$',UserInfoMgr_Add),
    url(r'^UserMgr/Mod$',UserInfoMgr_Mod),
    url(r'^UserMgr/Del$',UserInfoMgr_Del),                       
    #处理设备
    url(r'^DeviceMaintain[\/]?$',DeviceMaintainMgr),
    url(r'^DeviceMaintain/Del$',DeviceMaintainMgr_Del),                       
    url(r'^DeviceMaintain/Add$',DeviceMaintainMgr_Add),
    url(r'^DeviceMaintain/Mod$',DeviceMaintainMgr_Mod),
    url(r'^DeviceMaintain/Assign$',DeviceMaintainMgr_Assign),
    url(r'^DeviceMaintain/UnAssign$',DeviceMaintainMgr_UnAssign),                       
    url(r'^DeviceMaintain/Borrow$',DeviceMaintainMgr_Borrow),
    url(r'^DeviceMaintain/Back$',DeviceMaintainMgr_Back),                       
    url(r'^DeviceMaintain/AskBack$',DeviceMaintainMgr_AskBack),                           
    #处理sim卡         
    #url(r'^hello/$',hello),                                             
    url(r'^SimInfo[\/]?$',SimInfoMgr),
    url(r'^SimInfo/Del$',SimInfoMgr_Del),                       
    url(r'^SimInfo/Add$',SimInfoMgr_Add),
    url(r'^SimInfo/Mod$',SimInfoMgr_Mod),
    url(r'^SimInfo/Assign$',SimInfoMgr_Assign),
    url(r'^SimInfo/UnAssign$',SimInfoMgr_UnAssign),
    url(r'^SimInfo/Borrow$',SimInfoMgr_Borrow),
    url(r'^SimInfo/Back$',SimInfoMgr_Back),
    url(r'^SimInfo/AskBack$',SimInfoMgr_AskBack),                           
    #修改密码                       
    url(r'^PasswordMan[\/]?$',ChngPassMgr),                                 
    url(r'^msg$',msg_show),
    url(r'^msg_noauth$',msg_show_noauth),
    #日志查看
    url(r'^LogView[\/]?$',LogView),
    #我的设备
    url(r'^MyDevice[\/]?$',MyDevMgr),
    url(r'^MyDevice/Borrow$',MyDevMgr_Borrow),
    url(r'^MyDevice/Back$',MyDevMgr_Back),                       
    url(r'^MyDevice/AskBack$',MyDevMgr_AskBack),
    url(r'^MySim/Borrow$', MySimMgr_Borrow),
    url(r'^MySim/Back$', MySimMgr_Back),
    url(r'^MySim/AskBack$', MySimMgr_AskBack),                         
    #测试页面
    url(r'^testpage[\/]?$',TestPage),                       
                       
) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
