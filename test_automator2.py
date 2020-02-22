#encoding utf-8
import uiautomator2 as u2
from time import sleep
from uiautomator2.ext.htmlreport import HTMLReport
import unittest
'''
（1）连接：
wifi连接：
d=u2.connect('192.168.1.89')#手机和电脑同一个WIFI,此为手机IP地址
usb连接：
u2.connect('3ac86305')#device:3ac86305
（2）包名：
手机管家APP包名：com.coloros.phonemanager
（3）定位：
ResourceId定位：
d(resourceId="com.coloros.phonemanager:id/item_entry_img")
Text定位：
d(text="清理存储")
Description定位：
d(description=" ")
ClassName定位：
d(className="android.widget.RelativeLayout")
（4）报告：
        from uiautomator2.ext.htmlreport import HTMLReport
        html_report=HTMLReport(self.d,'report')
        html_report.patch_click()
（5）执行:
规范unnitest:
class名：首字母大写，包含Test
初始化环境：setUp()，U大写
清理环境：tearDown()，D大写
测试用例方法：test开头，加上和测试模块相关的字母缩写（自定义发挥，能看懂测撒）

'''
class PhmTest(unittest.TestCase):
    def setUp(self):
        self.d=u2.connect('3ac86305')
        html_report=HTMLReport(self.d,'report')
        html_report.patch_click()
        self.d.app_start("com.coloros.phonemanager")
        pass

    def testclear(self):
        # 点击清理缓存
        self.d(resourceId="com.coloros.phonemanager:id/item_entry_img").click()
        # 点击一键清理
        onece_clear="com.coloros.phonemanager:id/clear_advice_preference_button_layout"
        self.d(resourceId=onece_clear).click()
        #等待清理完成
        sleep(2)
        assert self.d(resourceId=onece_clear).exists()==False
        sleep(5)

    def tearDown(self):
        self.d.app_stop("com.coloros.phonemanager")
        pass

if __name__=='__main__':
    unittest.main()


