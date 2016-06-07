from django.db import models
from django.contrib.auth.models import Permission

#手机厂商表
class ProductInfo(models.Model):
    ProductName = models.CharField(max_length=20)
    ProductAbout = models.CharField(blank=True,max_length=50,null=True)

    def __unicode__(self):
        return u'%d,%s,%s' % (self.id,self.ProductName,self.ProductAbout)

#操作系统表
class OsInfo(models.Model):
    OsName = models.CharField(max_length=10)
    OsAbout = models.CharField(blank=True,max_length=50,null=True)

    def __unicode__(self):
        return u'%d,%s,%s' % (self.id,self.OsName,self.OsAbout)

#操作系统版本号表
class OsVersionInfo(models.Model):
    OsVersionName = models.CharField(max_length=20)
    OsInfo = models.ForeignKey(OsInfo)

    def __unicode__(self):
        return u'%d,%s,%s' % (self.id,self.OsVersionName,self.OsInfo.OsName)

#分辨率表
class ResolutionInfo(models.Model):
    ResolutionName = models.CharField(max_length=20)
    ResolutionLevel = models.IntegerField(blank=True,null=True)
    ResolutionAbout = models.CharField(blank=True,max_length=50,null=True)

    def __unicode__(self):
        return u'%d,%s,%d,%s' % (self.id,self.ResolutionName,\
                                 self.ResolutionLevel,self.ResolutionAbout)

#主屏尺寸表
class ScreenSizeInfo(models.Model):
    ScreenSizeName = models.CharField(max_length=20)
    ScreenSizeUnit = models.IntegerField(blank=True,null=True)
    ScreenSizeAbout = models.CharField(blank=True,max_length=50,null=True)

    def __unicode__(self):
        return u'%d,%s,%d,%s' % (self.id,\
                                 self.ScreenSizeName,\
                                 self.ScreenSizeUnit,\
                                 self.ScreenSizeAbout
                                 )

class MemoryInfo(models.Model):
    MemorySize = models.CharField(max_length=20)
    MemoryAbout = models.CharField(blank=True,max_length=50,null=True)

    def __unicode__(self):
        return u'%d,%s,%s' % (self.id,self.MemorySize,self.MemoryAbout)    

#省份表
class Province(models.Model):
    ProvinceName = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%d,%s' % (self.id,self.ProvinceName)

#运营商表
class Carrier(models.Model):
    CarrierName = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%d,%s' % (self.id,self.CarrierName)

#Sim卡白名单
class SimWhiteList(models.Model):
    ListDesc = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%d,%s' % (self.id,self.ListDesc)


#主题界面表
class MainMenu(models.Model):
    MenuName = models.CharField(max_length=30)
    MenuLink = models.CharField(max_length=100)
    AuthMenuId = models.ForeignKey(Permission)
    IfNotEffective = models.CharField(max_length=1,blank=True,null=True)
    def __unicode__(self):
        return u'%d,%s,%s,%s' % (self.id,self.MenuName,\
                                 self.MenuLink,\
                              self.IfNotEffective)   
    
