import requests
import re
import os
import time
from bs4 import BeautifulSoup
from progress.bar import Bar, IncrementalBar
import random
from multiprocessing import Process,Pipe
from Download import Downloader


def get_html(html):
    html_list = []
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'}
    cook ={"Cookie":'JSESSIONID=4DC92CB4BAF1936E66C223BDD0E61972;Hm_lvt_307de5a4815acb9da76ced3a8b25b867=1564188967'}   
    try:
        print('Get Html Collecting... %s'%html)
        r = requests.get(html, cookies=cook, headers=headers).content
        soup = BeautifulSoup(r, 'lxml')
        datas = soup.findAll(attrs={"data-lightbox":"a"})
        for data in datas:
            href = data.get('href')
            html_list.append('https://www.duotoo.com'+href)
        print('html_list len:',len(html_list))
        return html_list
    except requests.exceptions.ConnectionError:
        print('ConnectionError:%s'%html)
    except requests.exceptions.ChunkedEncodingError:
        print('ChunkedEncodingError:%s'%html)

def get_jpg_urls(html):
    html_list = []
    url_list = []
    title = ''
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'}
    cook ={"Cookie":'JSESSIONID=4DC92CB4BAF1936E66C223BDD0E61972;Hm_lvt_307de5a4815acb9da76ced3a8b25b867=1564188967'}   
    jpg_nums = 0
    try:
        print('Get Jpg Collecting... %s'%html)
        r = requests.get(html, cookies=cook, headers=headers, timeout=10).content
        soup = BeautifulSoup(r, 'lxml')
        datas = soup.find(attrs={"class":"pages"})
        data = datas.find('a')
        title = html.split('/')[-2]+'-'+html.split('/')[-1][:-5]+'-'+soup.find('title').text[:-4]
        jpg_nums = int(data.text[data.text.index('共')+1:data.text.index('页')])
        try:
            datas = soup.findAll('section')
            data = datas[1].find('p')
            data = data.find('img')
            url_list.append(data.get('src'))
            html_head = html[:html.index('.html')]
            for i in range(2, jpg_nums+1):
                html_list.append(html_head+'_'+str(i)+'.html')
        except:
            print('Find error! %s'%html)
            pass
    except requests.exceptions.ConnectionError:
        print('ConnectionError:%s'%html)
        return []
    except requests.exceptions.ChunkedEncodingError:
        print('ChunkedEncodingError:%s'%html)
        return []

    print("This page have %d"%jpg_nums)
    bar = IncrementalBar("Collect Process", max=jpg_nums, suffix='%(index)d/%(max)d')
    for html in html_list:
        r = requests.get(html, cookies=cook, headers=headers, timeout=10).content
        soup = BeautifulSoup(r, 'lxml')
        try:
            datas = soup.findAll('section')
            data = datas[1].find('img')
            url_list.append(data.get('src'))
            bar.next()        
        except:
            pass
    bar.finish()
    return (title, url_list)

def download(url,path):
    down = Downloader(url, path)
    down.isBar = True
    down.start()

def downloader(task):
    path = './downloads/'+task[0]+'/'
    if len(task[1]) == 0:
        try:
            os.makedirs(path[:path[:-1].rindex('/')]+'/(Error)'+task[0]+'/')
        except:
            pass
    for i in range(len(task[1])):
        p1 = Process(target=download, args = (task[1][i], path+'(%d)'%i+task[1][i].split('/')[-1]))
        p1.start()

def download_jpg(down_start,down_end):
    htmls_head = 'https://www.duotoo.com/meinvtupian/index'
    htmls_list = []
    for i in range(down_start, down_end+1):
        if i == 1:
            htmls_list.append(htmls_head+'.html')
        else:
            htmls_list.append(htmls_head+'_'+str(i)+'.html')
    print(htmls_list)
    
    for htmls in htmls_list:
        html_list = get_html(htmls)
        for html in html_list:
            task_ones = get_jpg_urls(html)
            p1 = Process(target=downloader, args = (task_ones,))
            p1.start()
            p1.join()

#download_jpg(2,2)  # pages:1-398
print('All done')
