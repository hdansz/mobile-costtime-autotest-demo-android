#encoding utf-8
import uiautomator2 as u2
from time import sleep
from uiautomator2.ext.htmlreport import HTMLReport
import pytest
import allure
import os
from Tools import logger
import time
import datetime

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
规范pytest:
class名：首字母大写，包含Test
初始化环境：setup()，u小写
清理环境：teardown()，d小写
测试用例方法：test开头，加上和测试模块相关的字母缩写（自定义发挥，能看懂测撒）
'''

LOG = logger.Logger("TestPhm").getlog()
class TestPhm():
    def setup(self):
        self.log = LOG
        self.log.debug("连接设备")
        self.d=u2.connect('3ac86305')
        self.d.healthcheck()  # 解锁屏幕并启动uiautomator服务
        html_report=HTMLReport(self.d,'report')
        html_report.patch_click()
        self.log.debug("启动手机管家APP")
        self.d.app_start("com.coloros.phonemanager")
        pass

    @allure.MASTER_HELPER.step("清理缓存")
    def test_clear(self):
        # 点击清理缓存
        self.log.debug("点击清理缓存")
        self.d(resourceId="com.coloros.phonemanager:id/item_entry_img").click()
        start_time=datetime.datetime.now()

        path = os.path.dirname(os.path.abspath(__file__))
        onece_clear = "com.coloros.phonemanager:id/clear_advice_preference_button_layout"
        clear_sector="com.coloros.phonemanager:id/clear_stage_sector"
        # while 1:
        #     temp_img=self.d.screenshot(path + "/temp_screenshot/"+"except.jpg")
        #     if self.d(resourceId=clear_sector).exists()==True:
        #         end_time=datetime.datetime.now()
        #         break
        # print('相差：%s微秒' % (start_time-end_time).microseconds)
        # print('相差：%s秒' % (start_time - end_time).seconds)
        # 点击一键清理
        # self.log.debug("点击一键清理")
        # self.d(resourceId=onece_clear).click()
        #等待清理完成
        sleep(4)
        self.log.debug("清理完成")
        temp_img = self.d.screenshot(path + "/temp_screenshot/" + "except.jpg")
        sleep(1)
        assert self.d(resourceId=onece_clear).exists()==False

    def teardown(self):
        self.log.debug("退出APP")
        self.d.app_stop("com.coloros.phonemanager")
        pass

if __name__ == '__main__':
    '''
    cmd生成HTML报告
    allure generate <xml路径> -o <html路径> --clean
    cmd查看HTML报告
    allure open -h 127.0.0.1 -p 8083 <html路径>
    xml、html的报告路径
    '''
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_result = path + "/py_result/xml"
    file_report=path+"/py_result/html"
    pytest.main(['-s', '-q', '--alluredir', file_result])


