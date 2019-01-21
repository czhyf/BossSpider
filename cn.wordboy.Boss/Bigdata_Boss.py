from  selenium import webdriver
import csv
import re
from time import sleep
from ProxyPool import get_proxy
import tqdm
#要爬取的字段


#获取dirver

def get_driver(ip):
   driver_path = 'D:\project\pythonProject\BaiduSpdier\cn.wordboy.Boss\chromedriver.exe'
   option = webdriver.ChromeOptions()
   option.add_argument("headless")
   option.add_argument("--proxy-server=http://"+ip)
   driver = webdriver.Chrome(driver_path, chrome_options=option)
   driver.set_page_load_timeout(70)
   driver.set_script_timeout(70)
   return  driver

def get_url(keyword,driver):
   print("获取岗位信息时没发生超时异常,正在重新进行调整")
   driver.close()
   ip = get_proxy.get_proxy()
   driver = get_driver(ip)
   try:
      driver.get('https://www.zhipin.com/c101010100/y_3-e_102/?query=' + keyword + '&ka=sel-salary-3')
   except Exception:
      print("放弃此项目")
#获得岗位信息的url
def get_info(driver,keyword,job_url_list):
      try:
         driver.get('https://www.zhipin.com/c101010100/y_3-e_102/?query=' + keyword + '&ka=sel-salary-3')
      except Exception:
         get_url(keyword,driver)
      while True:
         """
         获取a标签的点击状态，如果是和javasc一样，证明下一页到此结束。
         """
         #得到下一页状态，可能有的页面没有，则需要进行try cath
         try:
            a_flag=driver.find_element_by_class_name("next").get_attribute("href")
            print("有下一页，开始点击")
            #证明没有下一页了
            if a_flag=='javascript:;':
               break
            #获得职位详细页面的属性
            job_bloks=driver.find_elements_by_class_name('info-primary')
            for job_blok in job_bloks:
               try:
                  job_url_list.append(job_blok.find_element_by_class_name('name').find_element_by_tag_name("a").get_attribute("href"))
               except Exception as e:
                  continue
            print("本页码数获取完成")
         #点击下一页
            click=driver.find_element_by_class_name('next')
            click.click()
         #假如一页没有下一页的按钮，直接进行元素拿取
         except Exception:
            try:
               print("没有下一页，直接开始获取本业元素")
               # 获得职位详细页面的属性
               job_bloks = driver.find_elements_by_class_name('info-primary')
               for job_blok in job_bloks:
                  try:
                     job_url_list.append(
                        job_blok.find_element_by_class_name('name').find_element_by_tag_name("a").get_attribute("href"))
                  except Exception as e:
                     continue
               print('元素获取完成')
            except Exception:
               print("还是没有拿到，疯了,算了，不拿了")
         print("此模块获取完成，返回url集合")
         break
      return job_url_list

#获取详细信息的url
def get_info_proxy(driver,url):
   print("发生超时异常,重新更换代理ip进行加载")
   driver.close()
   ip_load = get_proxy.get_proxy()
   driver = get_driver(ip_load)
   try:
      driver.get(url)
   except Exception:
      print("放弃，重新调整")
#通过拿到岗位信息的url进行详细岗位的爬取
def get_job_info(job_url_list,jobs_info_list):
   i=1
   ip1=get_proxy.get_proxy()
   driver=get_driver(ip1)
   for url in job_url_list:
      i+=1
      #每五次循环进行一次替换ip代理
      if i%5==0:
         driver.close()
         ip2=get_proxy.get_proxy()
         driver=get_driver(ip2)
      try:
         job_info_list=[]

         try:
            driver.get(url)
         except Exception:
            get_info_proxy(driver,url)
         post=driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/h1').text
         salar=driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span').text
         time=driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[1]/span').text
         a_e_x=driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[2]/p').text
         a_e_x_r=re.match(r'城市：(.*?)经验：(.*?)学历：(.*)',a_e_x)
         City=a_e_x_r.group(1)
         experience=a_e_x_r.group(2)
         Education=a_e_x_r.group(3)
         Corporate_name=driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[3]/h3/a').text
         Job_description=driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div').text
         job_info_list.append(post)
         job_info_list.append(salar)
         job_info_list.append(time)
         job_info_list.append(City)
         job_info_list.append(experience)
         job_info_list.append(Education)
         job_info_list.append(Corporate_name)
         Job_description=str(Job_description).replace("\n","——")
         job_info_list.append(Job_description)
         print(job_info_list)
         jobs_info_list.append(job_info_list)
      except Exception:
         continue
   return jobs_info_list

#写文件csv
def write_csv(jobs_info_list,job_info_text,csv_path):
   with open(csv_path,'w',encoding='utf-8') as csvfile:
      writer =csv.writer(csvfile)
      # 先写入columns_name
      writer.writerow(job_info_text)
      # 写入多行用writerows
      writer.writerows(jobs_info_list)

#开始任务
def start(path):
   print("程序开始执行")
   # 岗位
   keywords = ["数据分析师","大数据应用开发工程师",'大数据开发','大数据产品经理','大数据平台运维','大数据研发工程师']
   #存储url集合
   job_url_list=[]
   for keyword in keywords:
      #得到随机代理
      ip1=get_proxy.get_proxy()
      #每一页进行换一个ip代理
      driver = get_driver(ip1)
      job_url_list=get_info(driver, keyword,job_url_list)
   print("所有的模块的url集合已经获取完毕，开始获取详细页面的信息")
   #职位信息的list集合
   # 职位 薪资 发布时间  地点 经验 公司名称 公司规模 岗位职责
   jobs_info_list=[]
   jobs_info_list=get_job_info(job_url_list,jobs_info_list)
   #职位信息
   job_info_text=["职位","薪资","发布时间","地点","经验","学历","公司名称","工作职责"]
   print(len(jobs_info_list))
   write_csv(jobs_info_list,job_info_text,path)


if __name__ == '__main__':
   path='C:\\Users\\Administrator\\Desktop\\job3.csv'
   start(path)
