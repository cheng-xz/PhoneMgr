from django import template
import time

register = template.Library()


def addModule(value):
    return 'PhoneMgr.'+value

def timeCv(value):
    try:
        value_i = int(value)
    except:
        return '时间转换出错'
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(value_i))

LogState = {1001:'添加新手机',\
            1002:'修改手机信息',\
            1003:'删除手机',\
            1004:'分配手机',\
            1005:'手机取消分配',\
            1006:'拥有者借手机',\
            1007:'拥有者还手机',\
            
            2001:'增加用户',\
            2002:'修改用户',\
            2003:'删除用户',\

            3001:'添加SIM卡',\
            3002:'修改SIM卡',\
            3003:'删除SIM卡',\
            3004:'分配SIM',\
            3005:'取消分配SIM',\
            3006:'拥有者借SIM',\
            3007:'拥有者还SIM'}

def getLogState(value):
    try:
        value_i = int(value)
    except:
        return '状态码错误'
    else:
        return LogState.get(value_i)

def mytotal(mylist):
    return len(mylist)



register.filter('addModule',addModule)
register.filter('timeCv',timeCv)
register.filter('getLogState',getLogState)
register.filter('mytotal',mytotal)
