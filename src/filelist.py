from pyquery import PyQuery as pq
import os
import glob

class FileManager:

    def __init__(self, location):
        self.location = location
        self.files=[]

    def getFiles(self):
        for filename in glob.glob(os.path.join(self.location, '*.html')):
            self.files.append(filename)

        return self.files


class Test:

    def parse_page1(self):
        d = pq(url='http://www.cyberlink.com/index_en_US.html?r=1')
        p=d("body")
        print(p.html())