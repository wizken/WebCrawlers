import requests
import re
import time
from bs4 import BeautifulSoup
from progress.bar import Bar, IncrementalBar
import random
from multiprocessing import Process,Pipe
from Download import Downloader

def download(url,path):
    down = Downloader(url, path)
    down.isBar = True
    down.start()

def download_mp3(down_start,down_end):
    list_url = []
    down_url_head = 'https://ting55.com/book/2989'
    for num_index in range(down_start,down_end+1):
        url = '%s-%d'%(down_url_head,num_index)
        #反爬虫机制，1修改User-Agent
        headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'}
        cook ={"Cookie":'JSESSIONID=4DC92CB4BAF1936E66C223BDD0E61972;Hm_lvt_307de5a4815acb9da76ced3a8b25b867=1564188967'}
        
        r = requests.get(url, cookies=cook, headers=headers).content
        soup = BeautifulSoup(r, 'lxml')
        
        ting_m4as = soup.findAll(attrs={"type":"text/javascript"})
        print(ting_m4as)









    for i in list_url:
        print(i)
        if '.m4a' in i[1]:
            #p1 = Process(target = download, args = (i[1],'./tttmp3/%d)'%i[0]+i[1].split('/')[-1]))
            pass
        else:
            #p1 = Process(target = download, args = (i[1],'./tttmp3/'+i[1].split('/')[-1])) 
            pass
        #p1.start()

down = Downloader('http://miloli.info/asdb/fiction/xuanhuan/quanzhigaoshou/6irkrsrm.mp3','./123456/1234.mp3')
down.start()
#
#for i in range(1):
#    download_mp3(1,5)
#    print("The page of %d is done!Now waiting for the next one!"%i)
#    suffix = '%(eta)s'
#    times = 6
#    bar_count = IncrementalBar('Wait Progress',max=times, suffix=suffix)
#    for i in range(times):
#        bar_count.next()
#        time.sleep(1)
#    bar_count.finish()
# 

