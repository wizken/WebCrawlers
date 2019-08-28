import requests
import threading
import time
import os
from progress.bar import IncrementalBar

class DownloadBar(IncrementalBar):
    
    @property
    def speed_(self):
        chunkSize = 1024
        if self.avg > 1:  # B
            show = '%.1f'%(chunkSize/self.avg)+'B/s'
        elif self.avg > 1/1024:  # KB
            show = '%.1f'%(chunkSize/self.avg/1024)+'KB/s'
        else:  # MB
            show = '%.1f'%(chunkSize/self.avg/1024/1024)+'MB/s'
        return show

class Downloader:
    def __init__(self, url, path):
        self.url = url
        self.startTime = 0
        self.isBar = False
        self.isRun = False
        self.fileName = path.split('/')[-1]
        self.path = ''
        for i in path.split('/')[:-1]:
            self.path += i
            self.path += '/'
        try:
            os.makedirs(self.path)
        except OSError:
            pass
        self.timeout = 20
        self.chunkSize = 1024
        self.status_source = ('Starting', 'Requests not allow', 
                              'Done', 'ConnectionError', 
                              'ChunkedEncodingError', 'Stay', 
                              'Donenot', 'Writing')
        self.status_index = 5
        self.size_show = ''
    
    def start(self):
        self.startTime = time.time()
        if not self.isRun:
            thread1 = threading.Thread(target=self.runing)
            thread1.start()
            self.isRun = True
            thread1.join()
        pass
    
    def stop(self):
        self.isRun = False
        pass

    def set_filename(self, name):
        self.fileName = name
        pass

    def set_timeout(self, time):
        self.timeout = time
        pass

    def set_chunksize(self, size):
        self.chunkSize = size
        pass
    
    #@staticmethod
    def runing(self):
        self.status_index = 0
        try:
            print('Collecting... %s'%self.url)
            response = requests.get(self.url, stream=True, 
                    timeout=self.timeout)#stream mode is must be select
            chunk_size = self.chunkSize#pack size
            content_size = int(response.headers['content-length'])#main size
            time_count = time.time()
#            print(response.status_code)
            if response.status_code == 200:
                with open(self.path+self.fileName,"wb") as file:
                    self.status_index = 7
                    step_num = content_size/chunk_size
                    if content_size < 1024**2:  # KB
                        self.size_show = '%.1fKB'%(content_size/1024)
                    elif content_size < 1024**3:
                        self.size_show = '%.1fMB'%(content_size/(1024**2))
                    elif content_size < 1024**4:
                        self.size_show = '%.1fGB'%(content_size/(1024**3))
                    else:
                        self.size_show = 'The file is too large'

                    print('  Downloading %s (%s)'%(self.url, self.size_show))
                    if self.isBar:
                        bar = DownloadBar('    %(percent).2f%%', max=step_num, 
                                suffix='[%(speed_)s][%(eta_td)s]')
                    else:
                        pass

                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)

                        if self.isBar:
                            bar.next()
                        else:
                            pass

                        if self.isRun == False:
                            self.status_index = 6
                            break
                    if self.isBar:
                        bar.finish()
                    else:
                        pass
                    file.close()
                self.endTime = time.time()
                print("[%s(%s)]Download Done! Used time%.2fs"
                        %(self.fileName, self.size_show, self.endTime - self.startTime))
                self.status_index = 2
            else:
#                print('Requests is not allow!')
                self.status_index = 1
        except requests.exceptions.ConnectionError:
#            print('ConnectionError')
            self.status_index = 3
        except requests.exceptions.ChunkedEncodingError:
#            print('ChunkedEncodingError')
            self.status_index = 4
        else:
            pass
        self.isRun = False

