from django.db import models

#权限表

class MyAuthAll(models.Model):
    class Meta:
        permissions = (
            #用户登录1
            #('UserLoginAuth_CanLogin','1.1_用户登录'),
            #用户注册2
            #('UserRegAuth_UserRegMenu','2.1_访问用户注册菜单'),
            #('UserRegAuth_CanReg','2.2_可以注册用户'),
            #@@@用户管理3
            ('UserMgr_UserMgrMenu','3.1_访问用户管理菜单'),
            ('UserMgr_CanReg','3.2_可以注册用户'),
            ('UserMgr_QueUserInfo','3.3_搜索用户信息'),
            ('UserMgr_ResetPasswd','3.4_重置密码'),
            ('UserMgr_UpdateUserInfo','3.5_更新用户信息'),
            #added
            ('UserMgr_DelUserInfo','3.6_删除用户信息'),
            #设备录入4
            #('DeviceRecord_DeviceRecordMenu','4.1_访问设备录入菜单'),
            #('DeviceRecord_AddNewDevice','4.2_添加新的设备'),
            #SIM卡录入5
            #('SimRecord_SimRecordMenu','5.1_显示SIM录入菜单'),
            #('SimRecord_AddNewSim','5.2_添加新的SIM卡信息'),
            #@@@设备维护 6  -> 设备管理
            ('DeviceMaintain_DeviceMaintainMenu','6.1_访问设备维护菜单'),
            ('DeviceMaintain_AddNewDevice','6.2_添加新设备'),
            ('DeviceMaintain_QueAllDevice','6.3_查询所有设备状态'),
            ('DeviceMaintain_UpdateDeviceState','6.4_更新设备状态'),
            #added
            ('DeviceMaintain_AssignDevice','6.5_分配设备'),
            ('DeviceMaintain_CancelAssignDevice','6.6_取消分配设备'),
            ('DeviceMaintain_BorrowDevice','6.7_借出设备'),
            ('DeviceMaintain_AskBackDevice','6.8_催还设备'),
            ('DeviceMaintain_ReturnDevice','6.9_归还设备'),
            #@@@SIM卡维护 7   -> sim卡管理
            ('SimMaintain_SimMaintainMenu','7.1_访问SIM卡维护菜单'),
            ('SimMaintain_AddNewSim','7.2_添加SIM卡权限'),
            ('SimMaintain_QueSimInfo','7.3_SIM卡信息查询权限'),
            ('SimMaintain_UpdateSimInfo','7.4_SIM卡信息修改权限'),
            #added
            ('SimMaintain_AssignSim','7.5_分配SIM'),
            ('SimMaintain_CancelAssignSim','7.6_取消分配SIM'),
            ('SimMaintain_BorrowSim','7.7_借出SIM'),
            ('SimMaintain_AskBackSim','7.8_催还SIM'),
            ('SimMaintain_ReturnSim','7.9_归还SIM'),
            #公共池设备管理8
            #('PubDeviceMan_PubDeviceManMenu','8.1_访问公共池设备管理菜单'),
            #('PubDeviceMan_BorrowDevice','8.2_能够借从公共池借设备'),
            #('PubDeviceMan_AssignDevice','8.3_将公告池设备分配给QA成员'),
            #下面的权限暂时不用
            #('PubDeviceMan_BatchBorrowDevice','8.4_批量从公共池借设备权限'),
            #@@@待确定借出9
            #('ConfirmBorrow_ConfirmBorrowMenu','9.1_访问待确定借出菜单'),
            #('ConfirmBorrow_SureBorrowOne','9.2_确定借出一个设备'),
            #('ConfirmBorrow_SureBorrowAll','9.3_确定借出任何设备'),
            #@@@已分配设备10
            #('AssignedDevice_AssignedDeviceMenu','10.1_访问已分配设备菜单'),
            #('AssignedDevice_AssDeviceBorrowOne','10.2_将分配给自己的设备借出去'),
            #('AssignedDevice_AssDeviceBorrowAll','10.3_将分配的任何设备借出去'),
            #('AssignedDevice_UnAssDevice','10.4_将分配的设备上交'),
            #@@@已借出设备11
            #('BorrowedDevice_BorrowedDeviceMenu','11.1_访问已借出去的设备'),
            #('BorrowedDevice_BackDevice','11.2_归还设备'),
            #('BorrowedDevice_AskBackDeviceOne','11.3_催还自己借出去的设备'),
            #('BorrowedDevice_AskBackDeviceAll','11.4_催还任何借出去的设备'),
            #@@@待确定归还12
            #('ConfirmBack_ConfirmBackMenu','12.1_访问待确定归还设备菜单'),
            #('ConfirmBack_SureBackOne','12.2_确定自己的设备归还了'),
            #('ConfirmBack_SureBackAll','12.3_确定任何设备归还了'),
            #权限管理13
            #('AuthMan_AuthManMenu','13.1_访问权限管理菜单'),
            #('AuthMan_CreateGroup','13.2_可以创建一个权限组'),
            #('AuthMan_GroupAssAuth','13.3_可以给组分配权限'),
            #('AuthMan_AssUserGroup','13.4_可以将一个用户分配到权限组'),
            #@@密码管理14  ->本人自动拥有，不设置单独权限
            #('PasswordMan_PasswdManMenu','14.1_访问密码管理菜单'),
            #('PasswordMan_ModPasswd','14.2_修改密码'),
            #@@@日志管理15
            ('LogView_LogViewMenu','15.1_访问日志查看菜单'),
            ##added
            ('LogView_AccessOtherLog','15.2_访问其他日志'),
            #@@@我的设备16
            ##added
            ('MyDevice_MyDeviceMenu','16.1_访问我的设备菜单'),
            )
            
            

