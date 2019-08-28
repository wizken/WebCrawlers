from Download import Downloader
from multiprocessing import Process


def download(url,path):
    down = Downloader(url, path)
    #down.isBar = True
    down.start()

readed_list = []
with open('readed2.txt', 'r') as file:
    while True:
        line = file.readline()
        if len(line) < 3:
            break
        line = line[2:-3].split('\', \'')
        readed_list.append(line)
    file.close()

print(len(readed_list))
def download_ten(in_list):
    for i in in_list:
        p1 = Process(target = download, args = (i[1],'./downloads/'+i[0]+'/'+i[1].split('/')[-1])) 
        p2 = Process(target = download, args = (i[2],'./downloads/'+i[0]+'/'+i[2].split('/')[-1])) 
        p1.start()
        p2.start()
items_num=5
for index in range(len(readed_list)//items_num+1):
    if index == len(readed_list)//items_num:
        i = readed_list[items_num*index:]
    else:
        i = readed_list[items_num*index:items_num*(index+1)]
    p1 = Process(target = download_ten, args = (i,)) 
    p1.start()
    p1.join()



