from django.db import models
from django.contrib.auth.models import User,Group
from modelsBasic import *

#用户信息表
class UserInfo(models.Model):
    Userid = models.ForeignKey(User,related_name='r_1000')
    EngName = models.CharField(max_length=20)
    ChnName = models.CharField(max_length=20)
    #Group = models.ForeignKey(Group,null=True,blank=True)
    Dept = models.CharField(max_length=20,null=True,blank=True)
    IsCheck = models.IntegerField()
    UserInfoAbout = models.CharField(max_length=50,null=True,blank=True)

    def __unicode__(self):
        return u'%d,%s,%s,%s' % (self.id,self.EngName,self.ChnName,self.Dept)


#自定义的manager
class iosPhoneInfo(models.Manager):
    def get_queryset(self):
        os = OsInfo.objects.get(id = 1)
        print 'os info:',os
        return super(iosPhoneInfo,self).get_queryset().filter(OsInfo = os)

class androidPhoneInfo(models.Manager):
    def get_queryset(self):
        os = OsInfo.objects.filter(OsName = 'Android')
        print 'os info:',os
        return super(androidPhoneInfo,self).get_queryset().filter(OsInfo = os)

#根据状态自定义
class CanBorrowedPhonInfo(models.Manager):
    def get_queryset(self):
        return super(CanBorrowedPhonInfo,self).get_queryset().filter(CurrState=11)

class CanNotBorrowedPhonInfo(models.Manager):
    def get_queryset(self):
        return super(CanBorrowedPhonInfo,self).get_queryset().filter(CurrState=12)    


#手机信息表
class PhoneInfo(models.Model):
    PhoneName = models.CharField(max_length=50)
    ProductInfo = models.ForeignKey(ProductInfo,related_name='r_1001')
    ScreenSizeInfo = models.ForeignKey(ScreenSizeInfo,related_name='r_1002')
    ResolutionInfo = models.ForeignKey(ResolutionInfo,related_name='r_1003')
    MemoryInfo = models.ForeignKey(MemoryInfo,null=True,blank=True,related_name='r_1004')
    OsInfo = models.ForeignKey(OsInfo,related_name='r_1005')
    OsVersionInfo = models.ForeignKey(OsVersionInfo,related_name='r_1006')
    CpuType = models.CharField(max_length=200,null=True,blank=True)
    CpuCoreNum = models.IntegerField(blank=True,null=True)
    IMEI = models.CharField(max_length=20)
    #IfSim = models.BooleanField()
    #SimInfo = models.ForeignKey(SimInfo,null=True,blank=True)
    FundId = models.CharField(max_length=100,blank=True,null=True)
    HealthState = models.IntegerField(blank=True,null=True)
    IfTel = models.IntegerField(blank=True,null=True)
    Owner = models.ForeignKey(User,blank=True,null=True,related_name='r_1007')
    #这里是状态信息
    CurrState = models.IntegerField()
    BorrowMan = models.ForeignKey(User,related_name='r_1008',null=True,blank=True)
    BorrowDate = models.IntegerField(null=True,blank=True)
    BorrowAuthMan = models.ForeignKey(User,related_name='r_1009',null=True,blank=True)
    IfBorrowAuth = models.IntegerField(null=True,blank=True)
    BackMan = models.ForeignKey(User,related_name='r_1010',null=True,blank=True)
    BackDate = models.IntegerField(null=True,blank=True)
    BackAuthMan = models.ForeignKey(User,related_name='r_1011',null=True,blank=True)
    IfBackAuth = models.IntegerField(null=True,blank=True)
    #其他信息
    CreateDate = models.IntegerField(blank=True,null=True)
    UpdateDate = models.IntegerField(blank=True,null=True)
    About = models.CharField(max_length=50,blank=True,null=True)
    InitInfo = models.CharField(max_length=50,blank=True,null=True)

    objects = models.Manager()
    androidObjects = androidPhoneInfo()
    iosObjects = iosPhoneInfo()
    CanBorrowedObjects = CanBorrowedPhonInfo()
    CanNotBorrowedObjects = CanNotBorrowedPhonInfo()
    
    

    

    

    
#手机历史状态表
class PhoneHisState(models.Model):
    PhoneInfo = models.ForeignKey(PhoneInfo,related_name='r_1012')
    CurrState = models.IntegerField()
    BorrowMan = models.ForeignKey(User,related_name='r_1013',null=True,blank=True)
    BorrowDate = models.IntegerField(null=True,blank=True)
    BorrowAuthMan = models.ForeignKey(User,related_name='r_1014',null=True,blank=True)
    BackMan = models.ForeignKey(User,related_name='r_1015',null=True,blank=True)
    BackDate = models.IntegerField(null=True,blank=True)
    BackAuthMan = models.ForeignKey(User,related_name='r_1016',null=True,blank=True)
    IfBorrowAuth = models.IntegerField(null=True,blank=True)
    IfBackAuth = models.IntegerField(null=True,blank=True)
    CreateDate = models.IntegerField(null=True,blank=True)


#SIM卡信息表
class SimInfo(models.Model):
    PhoneNum = models.CharField(max_length=11)
    Province = models.ForeignKey(Province,related_name='r_1017')
    Carrier = models.ForeignKey(Carrier,related_name='r_1018')
    IMSI = models.CharField(max_length=11,blank=True,null=True)
    CurrOwner = models.ForeignKey(User,null=True,blank=True,related_name='r_1019')
    ServerPass = models.CharField(max_length=10,null=True,blank=True)
    SimWhiteList = models.ForeignKey(SimWhiteList,related_name='r_2001',null=True,blank=True)
    #当前状态信息
    CurrState = models.IntegerField()
    BorrowMan = models.ForeignKey(User,related_name='r_1020',null=True,blank=True)
    BorrowDate = models.IntegerField(null=True,blank=True)
    BorrowAuthMan = models.ForeignKey(User,related_name='r_1021',null=True,blank=True)
    BackMan = models.ForeignKey(User,related_name='r_1022',null=True,blank=True)
    BackDate = models.IntegerField(null=True,blank=True)
    BackAuthMan = models.ForeignKey(User,related_name='r_1023',null=True,blank=True)
    #其他信息
    SimAbout = models.CharField(max_length=50,blank=True,null=True)
    

    def __unicode__(self):
        return u'%d,%s,%s,%s' % (self.id,self.PhoneNum,\
                              self.Carrier.CarrierName,
                              self.Province.ProvinceName)

#SIM卡历史状态表
class SimHisState(models.Model):
    SimInfo = models.ForeignKey(SimInfo,related_name='r_1024')
    CurrState = models.IntegerField()
    BorrowMan = models.ForeignKey(User,related_name='r_1025',null=True,blank=True)
    BorrowDate = models.IntegerField(null=True,blank=True)
    BorrowAuthMan = models.ForeignKey(User,related_name='r_1026',null=True,blank=True)
    BackMan = models.ForeignKey(User,related_name='r_1027',null=True,blank=True)
    BackDate = models.IntegerField(null=True,blank=True)
    BackAuthMan = models.ForeignKey(User,related_name='r_1028',null=True,blank=True)
    CreateDate = models.IntegerField(null=True,blank=True)

class LogInfoOrderManager(models.Manager):
    def get_queryset(self):
        return super(LogInfoOrderManager,self).get_queryset().order_by('-CreateDate')

#操作历史表
class LogInfo(models.Model):
    #UserInfo = models.ForeignKey(User,related_name='r_1029',blank=True,null=True)
    UserName = models.CharField(max_length=50,blank=True,null=True)
    code = models.IntegerField()
    #PhoneInfo = models.ForeignKey(PhoneInfo,related_name='r_1030',blank=True,null=True)
    PhoneName = models.CharField(max_length=50,blank=True,null=True)
    CreateDate = models.IntegerField(null=True,blank=True)
    objects = models.Manager()
    OrderObjects = LogInfoOrderManager()
