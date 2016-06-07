from django import forms
from django.contrib.auth.models import User,Group
from models import *
import copy

class provinceQue(forms.Form):
    ProvinceName = forms.CharField(max_length=20,required=False)

class productInfoQue(forms.Form):
    ProductName = forms.CharField(max_length=20,required=True)
    ProductAbout = forms.CharField(max_length=50,required=False)

def get_ProductInfo():
    l = []
    #这里动态从数据库中获取数据
    ProductInfo_list = ProductInfo.objects.all()
    for ProcutInfo_i in ProductInfo_list:
        l.append([ProcutInfo_i.id,ProcutInfo_i.ProductName])

    return l
    
#def get_ModelInfo():
#    l = []
#    ModelInfo_list = ModelInfo.objects.all()
#    for ModelInfo_i in ModelInfo_list:
#        l.append([ModelInfo_i.id,ModelInfo_i.ModelName])

#    return l

def get_OsInfo():
    l = []
    l1 = []
    OsInfo_list = OsInfo.objects.all()
    for OsInfo_i in OsInfo_list:
        index = OsInfo_i.id
        if index == 2:
            l1.append([index,OsInfo_i.OsName])
        else:
            l.append([OsInfo_i.id,OsInfo_i.OsName])
    l = l1 + l

    return l

def get_OsVersionInfo():
    l = []
    OsVersionInfo_list = OsVersionInfo.objects.all()
    for OsVersionInfo_i in OsVersionInfo_list:
        l.append([OsVersionInfo_i.id,"["+OsVersionInfo_i.OsInfo.OsName+"]"+OsVersionInfo_i.OsVersionName])

    return l

def get_SimInfo():
    l = []
    SimInfo_list = SimInfo.objects.all()
    for SimInfo_i in SimInfo_list:
        l.append([SimInfo_i.id,SimInfo_i.PhoneNum])

    return l

def get_ResolutionInfo():
    l = []
    ResolutionInfo_list = ResolutionInfo.objects.all()
    for ResolutionInfo_i in ResolutionInfo_list:
        l.append([ResolutionInfo_i.id,ResolutionInfo_i.ResolutionName])

    return l

def get_ScreenSizeInfo():
    l = []
    ScreenSizeInfo_list = ScreenSizeInfo.objects.all()
    for ScreenSizeInfo_i in ScreenSizeInfo_list:
        l.append([ScreenSizeInfo_i.id,ScreenSizeInfo_i.ScreenSizeName])

    return l

def get_MemoryInfo():
    l = []
    MemoryInfo_list = MemoryInfo.objects.all()
    for MemoryInfo_i in MemoryInfo_list:
        l.append([MemoryInfo_i.id,MemoryInfo_i.MemorySize])

    return l

def get_SimWhiteList():
    l = []
    SimWhiteList_list = SimWhiteList.objects.all()
    for SimWhiteList_i in SimWhiteList_list:
        l.append([SimWhiteList_i.id,SimWhiteList_i.ListDesc])

    return l    

def get_GroupInfo():
    l = []
    la = []
    GroupInfo_list = Group.objects.all()
    for GroupInfo_i in GroupInfo_list:
        l.append([GroupInfo_i.id,GroupInfo_i.name])

    return l

def get_QAInfo():
    l = []
    l.append([0,'Default'])
    #这里只能是qas成员可以选择
    try:
        g = Group.objects.get(name='qas')
        u = g.user_set.all()
    except:
        u = []
    if len(u) == 0:
        pass
    else:
        #print u
        for u_i in u:
            l.append([u_i.id,u_i.username])

    #这里对用户名按照名称进行排序
    #print l
    lu = []
    for i in l:
        lu.append(i[1])
    #进行排序
    lu.sort()
    #print lu
    ln = copy.copy(l)
    for i in l:
        index = lu.index(i[1])
        ln[index] = i


    return ln                  


#获取非管理员组的所有用户
def get_AllUserInfo_NoDef():
    l = []
    l_i = []
    l_o = []
    #l.append([0,'默认值'])
    #l.append([0,'Default'])

    try:        
        g_o = Group.objects.get(name='users')
        u_o = g_o.user_set.all()
    except:
        u_o = []

            

    if len(u_o) == 0:
        pass
    else:
        #print u
        for u_i1 in u_o:
            l_o.append([u_i1.id,u_i1.username])


    #print l_o
    l_o.append([0,'-Default-'])
    
    l = l_o
    #这里对用户名按照名称进行排序
    #print l
    lu = []
    for i in l:
        lu.append(i[1])
    #进行排序
    lu.sort()
    #print lu
    ln = copy.copy(l)
    for i in l:
        index = lu.index(i[1])
        ln[index] = i


    return ln

def get_QAInfo_NoDef():
    l = []
    #这里只能是qas成员可以选择
    try:
        g = Group.objects.get(name='qas')
        u = g.user_set.all()
    except:
        u = []
    if len(u) == 0:
        pass
    else:
        #print u
        for u_i in u:
            l.append([u_i.id,u_i.username])

    #这里对用户名按照名称进行排序
    #print l
    lu = []
    for i in l:
        lu.append(i[1])
    #进行排序
    lu.sort()
    #print lu
    ln = copy.copy(l)
    for i in l:
        index = lu.index(i[1])
        ln[index] = i


    return ln            
     

class UserInfoQue(forms.Form):
    def __init__(self,*args,**kwargs):
        super(UserInfoQue,self).__init__(*args,**kwargs)
        self.fields['Group'] = forms.ChoiceField(
            choices = get_GroupInfo(),required = False
            )
    username = forms.CharField(max_length=30,required=False)
    EngName = forms.CharField(max_length=20,required=False)
    ChnName = forms.CharField(max_length=20,required=False)
    Dept = forms.CharField(max_length=20,required=False)
    passwd = forms.CharField(max_length=20,required=False,widget=forms.PasswordInput())
    email = forms.CharField(max_length=75,required=False)
    UserInfoAbout = forms.CharField(max_length=50,required=False)

class PhoneInfoQue(forms.Form):
    def __init__(self,*args,**kwargs):
        super(PhoneInfoQue,self).__init__(*args,**kwargs)
        self.fields['ProductInfo'] = forms.ChoiceField(
            choices = get_ProductInfo(),required=False
            )
        self.fields['ScreenSizeInfo'] = forms.ChoiceField(
            choices = get_ScreenSizeInfo(),required=False
            )
        #self.fields['ModelInfo'] = forms.ChoiceField(
        #    choices = get_ModelInfo(),required=False
        #    )
        self.fields['OsInfo'] = forms.ChoiceField(
            choices = get_OsInfo(),required=False
            )
        self.fields['OsVersionInfo'] = forms.ChoiceField(
            choices = get_OsVersionInfo(),required=False
            )
        self.fields['ResolutionInfo'] = forms.ChoiceField(
            choices = get_ResolutionInfo(),required=False
            )

        self.fields['MemoryInfo'] = forms.ChoiceField(
            choices = get_MemoryInfo(),required=False
            )            

        self.fields['SimInfo'] = forms.ChoiceField(
            choices = get_SimInfo(),required=False
            )

        self.fields['Owner'] = forms.ChoiceField(
            choices = get_AllUserInfo_NoDef(),required=False
            )

        self.fields['BorrowMan'] = forms.ChoiceField(
            choices = get_AllUserInfo_NoDef(),required=False
            )          

        self.fields['BorrowAuthMan'] = forms.ChoiceField(
            choices = get_QAInfo_NoDef(),required=False
            )             
        
        
    PhoneName = forms.CharField(max_length=50,required=False)
    CpuType = forms.CharField(max_length=200,required=False)
    CpuCoreNum = forms.ChoiceField(
        choices = (('1','单核'),('2','双核'),('4','四核'),('6','六核'),('8','八核')),required=False
        )
    IMEI = forms.CharField(max_length=20,required=False)
    #IfSim = forms.ChoiceField(
    #    choices = (('0','不关联'),('1','关联')),required=False
    #    )
    #Owner = forms.CharField(max_length=30,required=False)
    FundId = forms.CharField(max_length=30,required=False)
    HealthState = forms.ChoiceField(
        choices = (('0','正常'),('1','行政回收'),('2','保修')),required=False
        )
    IfTel = forms.ChoiceField(
        choices = (('0','非电信机'),('1','电信机')),required=False
        )        
    About = forms.CharField(max_length=50,required=False)
    InitInfo = forms.CharField(max_length=50,required=False)
    

class PhoneStateQue(forms.Form):
    PhoneName = forms.CharField(max_length=50,required=False)
    CurrState = forms.ChoiceField(
        choices = (('0','归属人所有'),('1','未借出'),('2','已借出'),('3','已归还')),
        required=False
        )
    BorrowMan = forms.CharField(max_length=30,required=False)
    BackMan = forms.CharField(max_length=30,required=False)

class SimStateQue(forms.Form):
    PhoneNum = forms.CharField(max_length=50,required=False)
    CurrState = forms.ChoiceField(
        choices = (('1','未借出'),('2','已借出'),('3','已归还')),
        required=False
        )
    BorrowMan = forms.CharField(max_length=30,required=False)
    BackMan = forms.CharField(max_length=30,required=False)    

def get_Carrier_info():
    l = []
    Carrier_list = Carrier.objects.all()
    for Carrier_i in Carrier_list:
        l.append([Carrier_i.id,Carrier_i.CarrierName])

    return l

def get_ProvinceInfo():
    l = []
    Province_list = Province.objects.all()
    for Province_i in Province_list:
        l.append([Province_i.id,Province_i.ProvinceName])

    return l

class SimInfoQue(forms.Form):
    def __init__(self,*args,**kwargs):
        super(SimInfoQue,self).__init__(*args,**kwargs)
        self.fields['CarrierInfo'] = forms.ChoiceField(
            choices = get_Carrier_info(),required=False
            )
        self.fields['SimWhiteList'] = forms.ChoiceField(
            choices = get_SimWhiteList(),required=False
            )
        self.fields['ProvinceInfo'] = forms.ChoiceField(
            choices = get_ProvinceInfo(),required=False
            )

        self.fields['CurrOwner'] = forms.ChoiceField(
            choices = get_AllUserInfo_NoDef(),required=False                    
            )
        self.fields['BorrowMan'] = forms.ChoiceField(
            choices = get_AllUserInfo_NoDef(),required=False                    
            )
        
        
    PhoneNum = forms.CharField(max_length=11,required=False)
    IMSI = forms.CharField(max_length=20,required=False)
    ServerPass = forms.CharField(max_length=10,required=False)
    SimAbout = forms.CharField(max_length=50,required=False)
    

class PhoneHisQue(forms.Form):
    PhoneName = forms.CharField(max_length=50,required=False)
    BorrowMan = forms.CharField(max_length=30,required=False)
    BackMan = forms.CharField(max_length=30,required=False)
    

class SimHisQue(forms.Form):
    PhoneNum = forms.CharField(max_length=50,required=False)
    BorrowMan = forms.CharField(max_length=30,required=False)
    BackMan = forms.CharField(max_length=30,required=False)
