import requests
import time
import os
from progress.bar import Bar,ChargingBar,IncrementalBar 
from multiprocessing import Process,Pipe

def downloader(url, path):
    start = time.time()
    size = 0
    response = requests.get(url, stream=True)#stream mode is must be select
    chunk_size = 1024#pack size
    content_size = int(response.headers['content-length'])#file main size

    time_count = time.time()
    if response.status_code == 200:
        print("[File Size]:%0.2f MB"% (content_size/chunk_size/1024))
        with open(path,"wb") as file:
            step_num = content_size/chunk_size
            suffix='%(percent).2f%% [%(eta_td)s]'
            bar = IncrementalBar('Down Processing', max=step_num, suffix=suffix)
            
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                bar.next()
            bar.finish()
    end = time.time()
    print('\n'+"Download Done! Used time%.2fs"%(end-start))

aaa=0
with open("./download_title_url.txt", "r") as url_file_readed:
    while True:
        lineReaded = url_file_readed.readline()[2:-3].split('\', \'') 
        if len(lineReaded) == 1:
            break
        new_dir = "./downloads/%s"%lineReaded[0]
        try:
            os.makedirs(new_dir)
        except OSError:
            pass
        aaa+=1;
        p1 = Process(target = downloader,args =(lineReaded[1],new_dir+'/'+lineReaded[1].split('/')[-1]))
        p1.start()
        p2 = Process(target = downloader,args =(lineReaded[2],new_dir+'/'+lineReaded[2].split('/')[-1]))
        p2.start()
print("ok") 
