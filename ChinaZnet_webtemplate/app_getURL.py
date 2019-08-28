import requests
import re
import time
from bs4 import BeautifulSoup
from progress.bar import Bar

import time
from progress.bar import Bar
suffix='%(percent)d%% [%(eta_td)s]'
bar = Bar('Processing', max=10800, suffix=suffix)
download_list = []

with open("./lists/list_title_url.txt", "r") as url_file_readed:
    while True:
        lineReaded = url_file_readed.readline()[2:-3].split('\', \'')
        bar.next()
        
        if len(lineReaded) == 1:
            break
#        print(lineReaded)
        r = requests.get(lineReaded[1])
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            down_a = soup.find(attrs={"class":"image_gall"})
            img_url = down_a.get("href")
#            print(img_url)
            title = down_a.get("href").split('/')[-1][:-4]+down_a.get("title")
#            print(title)

            down_div = soup.findAll(attrs={"class":"dian"})
            down_b = down_div[1].find(href=re.compile(r'^http:.'))
            rar_url = down_b.get("href")
#            print(rar_url)
            download_list.append((title,img_url,rar_url))
    
        except:
            pass
        finally:
            pass
    bar.finish()

#print(download_list)


with open("download_title_url.txt","w") as file:
    for i in download_list:
        file.write(str(i)+"\n")
    file.close

