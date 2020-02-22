#encoding utf-8
import uiautomator2 as u2
from time import sleep
from uiautomator2.ext.htmlreport import HTMLReport
import pytest
import allure
import os
from Tools import logger
from Tools import compimgs_similar
import time
import datetime
import xlwt

'''
（1）连接：
wifi连接：
d=u2.connect('192.168.1.89')#手机和电脑同一个WIFI,此为手机IP地址
usb连接：
u2.connect('3ac86305')#device:3ac86305
（2）包名：
随手记APP包名：com.mymoney
（3）定位：
ResourceId定位：
d(resourceId="com.mymoney:id/item_entry_img")
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

LOG = logger.Logger("TestMym").getlog()
class TestMym():
    path = os.path.dirname(os.path.abspath(__file__))
    loadtime=[]
    def setup(self):
        self.log = LOG
        self.log.debug("连接设备")
        self.d=u2.connect('3ac86305')
        self.d.healthcheck()  # 解锁屏幕并启动uiautomator服务
        #html_report=HTMLReport(self.d,'report')
        #html_report.patch_click()
        self.log.debug("启动APP")
        self.d.app_start("com.mymoney")
        #启动页有个几秒的闪屏，也可以点击跳过
        sleep(3)
        pass

    @allure.MASTER_HELPER.step("投资")
    @pytest.mark.repeat(10)#用例执行N次：pip3 install pytest-repeat
    def test_invest(self):
        self.d(resourceId="com.mymoney:id/main_top_nav_button_second").click()
        #点击页面入口时开始记录时间start_time
        start_time=datetime.datetime.now()
        temp_img2 = self.path + "/expected_resultimg/" + "ss_except.jpg"
        # 边加载页面边截图
        # 定义一个标准，哈希值范围是0-64，哈希值越小，图片越相似
        # 当加载完成的页面和预期页面相似度高，即哈希值小于某个值，判断为加载完成
        # 记录此时的时间点end_time
        # 终止截图、图片对比循环过程
        # 计算时间差，即页面加载时间=start_time-end_time
        while 1:
            temp_img1=self.d.screenshot(self.path + "/temp_screenshot/"+"ss_test.jpg")
            h=compimgs_similar.runImgSimilar(temp_img1,temp_img2)
            if h<5:
                end_time=datetime.datetime.now()
                print('[差值]哈希=', h)
                break
            print('[差值]哈希=', h,'>=5')
        #print('相差：%s微秒' % (start_time-end_time).microseconds)
        self.page_loadtime= (end_time - start_time  ).total_seconds()
        #把每次页面加载时间的值存在数组里面
        self.loadtime.append(self.page_loadtime)
        print('页面加载时间：%s秒' % self.page_loadtime)

    #求最大值、最小值、平均值，写入EXCEL
    def test_datadeal(self):
        #加载时间从小到大排序
        or_list=self.loadtime
        list1=sorted(self.loadtime)
        #取最大值
        max_loadtime=list1[-1]
        #取最小值
        min_loadtime=list1[0]
        #数组元素求平均值，取小数点后6位
        sumtimes=0
        for i in list1:
            sumtimes+=i
        ever_loadtime=format(sumtimes/(len(list1)),'.6f')
        #打印
        print('页面加载时间\nmax值:%s\nmin值:%s\n平均值:%s'%(max_loadtime,min_loadtime,ever_loadtime))

        #写入excel
        # 创建一个workbook 设置编码
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('app_page_loadingtime')
        # 参数对应 行, 列, 值
        sheet.write(0, 0, '测试页面')
        sheet.write(1, 0, 'vest')
        sheet.write(0, 1, '第N次加载')
        sheet.write(0, 2, '加载耗时')
        for i in range(len(or_list)):
            sheet.write(i+1, 1, i+1)
            sheet.write(i+1,2,or_list[i])

        sheet.write(0, 3, 'N次加载最大值')
        sheet.write(1, 3, max_loadtime)
        sheet.write(0, 4, '最小值')
        sheet.write(1, 4, min_loadtime)
        sheet.write(0, 5, '平均值')
        sheet.write(1, 5, ever_loadtime)
        # 保存
        book.save(self.path + "/loadingtime_data/"+"test_loadingtime.xls")

        #for i in list1:
            #print('第 %s 次加载页面时间%s'% (list1.index(i) + 1, i))
            #print('加载页面时间%s' % i)
        #sleep(6)
        # self.log.debug("完成")
        #获取预期结果图片，用来对比加载中的图片
        # temp_img = self.d.screenshot(path + "/expected_resultimg/" + "ss_except.jpg")
        # sleep(1)

    def teardown(self):
        self.log.debug("退出APP")
        self.d.app_stop("com.mymoney")
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


