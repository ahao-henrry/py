#!/usr/bin/python3
#-*-coding:utf-8-*-


import sys
import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup
from hashlib import md5
from requests.exceptions import RequestException


def get_time_str(time):
    strtime = time.strftime("%Y-%m-%d %H:%M:%S")
    return strtime.replace("-","").replace(" ", "").replace(":", "").replace(".", "")[0:8]

def get_elem(pageurl, selector):
    try:
        page_info = requests.get(pageurl, timeout=10)
        soup4 =  BeautifulSoup(page_info.content, "html.parser")
        return soup4.select(selector)
    except RequestException:
        print("--****Request netpage error.")
        raise

def download_img(imgurl, type):
    try:
        img_response = requests.get(imgurl, timeout=30)
        if img_response.status_code == 200:
            save_img(img_response.content, type)
        return None
    except RequestException:
        print("--****Request imgurl error.")
        raise
        # return None

def save_img(content, type):
    '''file_path = '{0}/{1}.{2}'.format(os.getcwd()+"\img\\"+type,
       md5(content).hexdigest(), "jpg")
    '''   
    file_path = '{0}\{1}.{2}'.format(os.getcwd()+"\img\\"+type,
            get_time_str(datetime.now()) + md5(content).hexdigest(),
            "jpg")
    if not os.path.exists(file_path):
        with open(file_path, "wb") as fi:
            fi.write(content)
            fi.close()
            
def fetch_landscape(pages=2):
    n = 0
    alinks = None
    while True:
        print("--****Begin download page %d" % (n+1))
        if n == 0:
            alinks = get_elem("https://fstoppers.com/groups/landscape-and-nature-photography", ".inner .post-title a")
        else:
            alinks = get_elem("https://fstoppers.com/groups/landscape-and-nature-photography?page="+str(n), ".inner .post-title a")
        print("--****pagesize=", len(alinks))
        for i in range(len(alinks)):
            if i == 0:
                continue
            alink = alinks[i]
            if alink and alink.get("href"):
                if alink.get("href") == "/groups/landscape-and-nature-photography":
                    break
                print("https://fstoppers.com"+alink.get("href"))
                imglinks = get_elem("https://fstoppers.com"+alink.get("href"), ".images-wrapper .image a")
                for imglink in imglinks:
                    if imglink and imglink.get("href"):
                        download_img(imglink.get("href"), "landscape")
                        print(imglink.get("href"))
        n += 1 
        if n == pages:
            break

def fetch_main():
    alinks = get_elem("https://fstoppers.com/community", ".photo a")
    for alink in alinks:
        if alink and alink.get("href"):
            print("https://fstoppers.com"+alink.get("href"))
            imglinks = get_elem("https://fstoppers.com"+alink.get("href"), ".inner .photo img")
            for imglink in imglinks:
                download_img(imglink.get("src"), "mainpage")
                print(imglink.get("src"))


if __name__ == "__main__":
    try:
        fetch_landscape(10)

        '''if sys.argv[1] == "landscape":
            fetch_landscape(int(sys.argv[2]))
        elif sys.argv[1] == "mainpage":    
            fetch_main()
            '''
    except IndexError:
        print("--****Please input argv.")
