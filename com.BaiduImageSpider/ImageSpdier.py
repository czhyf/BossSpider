import requests
import urllib.parse
import re
from tqdm import  tqdm
import os
import urllib.request
import pymssql
#得到所有图片的url
def get_url(img_name,index_start,img_list):
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.44',
        'Host':'image.baidu.com'
    }
    img_name=urllib.parse.unquote(img_name)
    url='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&fp=result&oe=utf-8&word='+img_name+'&pn='+str(index_start)+'&rn=30'
    url_text=requests.get(url,header).text
    imgs=re.findall(r'"thumbURL":"(.*?)",',url_text)
    for img in imgs:
        img_list.append(img)
    return  img_list
#下载的方法
def dowload_img(img_list,save_path):
    print()
    print("拿取图片url集合结束")
    print("开始下载")
    index=0
    for img in tqdm(img_list):
        img_path=save_path+str(index)+".jpg"
        urllib.request.urlretrieve(img,img_path)
        index+=1
    print("下载完成")
#拿到url_list的集合
def get_url_list(img_name):
    img_list = []
    print("开始拿取图片的url集合")
    for i in tqdm(range(40)):
        index_start = i * 30
        if len(img_list) == 0:
            img_list = get_url(img_name,index_start,img_list)
        else:
            img_list = get_url(img_name,index_start,img_list)
    return img_list

#判断路径
def path(save_path):
    if os.path.exists(save_path):
        if str(save_path).endswith("/"):
            return  save_path
        else:
            return save_path+"/"
    else:
        os.mkdir(save_path)
        save_path=save_path+"/"
        return save_path
#开始的方法
def start():
    img_name=input("请输入爬取图片的名称\n")
    save_path=input("请输入保存的路径\n")
    save_path=path(save_path)
    img_list=get_url_list(img_name)
    dowload_img(img_list,save_path)


if __name__ == '__main__':
    start()

