# pip install requests
# pip install bs4
# pip install lxml

import re
import os
import requests
import tkinter as tk
import time
from time import gmtime, strftime
from tkinter import ttk
from tkinter import messagebox as mBox
from tkinter import scrolledtext
from bs4 import BeautifulSoup


window = tk.Tk()
window.title('Spider Web v0.1')   # 窗口标题
window.geometry('460x340')      # 窗口尺寸
# window.maxsize(600, 400)
window.minsize(460, 340)
# window.resizable(width=False, height=False) # 设置窗口是否可以变化长 / 宽，False 不可变，True 可变
window.iconbitmap(r'icon.ico')

# htmlGet = "http://www.nationalgeographic.com.cn/animals/"
start_flag = 0

def butn_Start_hit():
    global start_flag
    if ent_htmlGet.get() != '' and ent_findGet.get() != '':
        start_flag = 1
        htmlGet = ent_htmlGet.get()
        findGet = ent_findGet.get()
        html = requests.get(htmlGet).text
        soup = BeautifulSoup(html, 'lxml')
        # img_ul = soup.find_all('ul', {"class": "img_list"})
        #<ul class="img_list">
        #...
        #</ul>
        img_src = soup.find_all('img',{'src': re.compile('.*?\.%s'%findGet)})

        for img in img_src:
            url = img['src']
            scrText.insert('end',url+'\n')
    else:
        tk.messagebox.showwarning(title='Warning',message='You must input the HEML and Search Content!')

def butn_DownL_hit():
    global start_flag
    folder_str1 = ''
    for i in range(6):
        if time.localtime()[i] < 10:
            folder_str1 += '0' + str(time.localtime()[i])
        else:
            folder_str1 += str(time.localtime()[i])
    os.mkdir('./%s/'% folder_str1)#创建文件夹

    if start_flag == 1:
        start_flag = 0
        htmlGet = ent_htmlGet.get()
        findGet = ent_findGet.get()
        html = requests.get(htmlGet).text
        soup = BeautifulSoup(html, 'lxml')
        img_src = soup.find_all('img',{'src': re.compile('.*?\.%s'%findGet)})
        for img in img_src:
            url = img['src']
            r = requests.get(url, stream=True)
            image_name = url.split('/')[-1]
            with open('./%s/%s' %(folder_str1,image_name), 'wb') as file:
                for chunk in r.iter_content(chunk_size=128):
                    file.write(chunk)
            print('Saved %s' % image_name)

def butn_clear_hit():
    global start_flag
    start_flag = 0
    scrText.delete(1.0, 'end')

def butn_Save_hit():
    global start_flag
    start_flag = 0
    print(scrText.get(1.0, 'end'))

def butn_OpDir_hit():
    # dir_list = os.listdir()
    scrText.insert('end','当前路径:\n')
    scrText.insert('end','%s\n'% os.getcwd())#当前路径
    scrText.insert('end','路径下目录:\n')
    for i in range(len(os.listdir())):
        scrText.insert('end', '%s\n'% os.listdir()[i])

def butn_Qiut_hit():
    qiut_ok = tk.messagebox.askquestion(title='Bye! Bye?',message='Are you sure to Qiut?')
    if qiut_ok == 'yes':
        window.quit()
        window.destroy()
        exit()

ttk.Label(window, text='Html:'      ).pack(side='top',padx=10,pady=0,expand=0,fill=tk.X)#

ent_htmlGet = ttk.Entry(window)
ent_htmlGet.pack(padx=10,pady=0,expand=0,fill=tk.X)

frm = tk.Frame(window)#Frame无外框
frm.pack(side='right',padx=0,pady=0,expand=0,fill=tk.Y)

ttk.Label(window, text='Search Type of File:'   ).pack(padx=10,pady=0,expand=0,fill=tk.X)

ent_findGet = ttk.Entry(window)
ent_findGet.pack(padx=10,pady=0,expand=0,fill=tk.X)

ttk.Label(window, text='Result:'    ).pack(padx=10,pady=0,expand=0,fill=tk.X)

scrText = scrolledtext.ScrolledText(window,wrap='none')#, width=70, height=38, wrap=tk.WORD 换行使单词移到下一行
scrText.pack(padx=10,pady=0,expand=1,fill=tk.BOTH)#

butn_Start = ttk.Button(frm, text='Start'        ,command=butn_Start_hit ).pack(side='top',padx=10,pady=19,expand=0)
butn_DownL = ttk.Button(frm, text='Download'     ,command=butn_DownL_hit ).pack(side='top',padx=10,pady=0,expand=0)
butn_clear = ttk.Button(frm, text='Clear Test'   ,command=butn_clear_hit ).pack(side='top',padx=10,pady=15,expand=0)
butn_Save  = ttk.Button(frm, text='Save Test'    ,command=butn_Save_hit  ).pack(side='top',padx=10,pady=0,expand=0)
butn_OpDir = ttk.Button(frm, text='Open Dir'     ,command=butn_OpDir_hit ).pack(side='top',padx=10,pady=15,expand=0)
butn_Qiut  = ttk.Button(frm, text='Qiut'         ,command=butn_Qiut_hit  ).pack(side='bottom',padx=10,pady=10,expand=0)

window.mainloop()
