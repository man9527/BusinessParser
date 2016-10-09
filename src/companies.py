import filelist
import domainjob
import collections
from pyquery import PyQuery as pq

class CompanyManager:

    def __init__(self, location):
        self.location=location;
        self.companies=[];

    def load(self):
        self.__parseFile__(self.location);

    def __parseFile__(self, fileName):
        list = collections.OrderedDict({})
        d = pq(filename=fileName)
        p=d(".ResultsBody")

        for row in p.children():
            rowp = pq(row.find("li")[0])
            url = rowp.attr("href")
            id=url[url.index("selID=")+6:url.index("selYear")-1]
            company = domainjob.Company(id, rowp.text(), url, fileName)

            if id not in list:
                list[id]=company

        for key, value in list.iteritems():
            self.companies.append(value)

