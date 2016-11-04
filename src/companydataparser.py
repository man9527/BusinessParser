from pyquery import PyQuery as pq
import collections
import logging
import hierarchyparser
import Connector
import time

logger = logging.getLogger( 'first_logging' )

class CompanyDataParser:

    def __init__(self, url, designatedYears, sleepYear=0):
        self.url=url

        pageHtml = Connector.get(self.url)

        self.d = pq(pageHtml.decode(encoding='UTF-8',errors='ignore'))

        self.realYears = []
        self.__parseYear__()
        self.sleepYear = sleepYear

        if not designatedYears:
            self.years = self.realYears
        else:
            self.years = designatedYears

    def parse(self):

        result = collections.OrderedDict({})

        yearCheck = dict()

        for y in self.years:
            if y in self.realYears:
                yearIndex = self.getIndex(yearCheck, y)
                index = self.realYears.index(y) + yearIndex +1

                if yearIndex > 0:
                    result[y + "." + str(yearIndex)] = (self.__parseData__(index))
                else:
                    result[y]=(self.__parseData__(index))

        logger.debug(result)
        return result

    def getIndex(self, yearCheck, year):
        if year in yearCheck:
            yearCheck[year] = yearCheck[year]+1
        else:
            yearCheck[year] = 0

        return yearCheck[year]

    def parseHierarchy(self):
        data = collections.OrderedDict({})

        for year in self.years:
            url = self.__parseHierarchyUrl__(self.url + year)
            h = hierarchyparser.HierarchyParser(
                "https://www.corporateaffiliations.com" + url)
            result = h.parse()
            data[year]=result
            logger.debug("sleep ...")
            time.sleep(self.sleepYear)
            logger.debug("sleep done ...")

        return data

    def __parseData__(self, yearIndex):
        p = self.d("#tablecol > tbody")

        data=collections.OrderedDict({})

        for row in p.children():
            rowEle = pq(row)
            rowClass = rowEle.attr("class")

            if (rowClass!=None and rowClass!="sectionsubhead"):
                tdEle=rowEle.children()
                name=tdEle[0].text
                tdEleRemain=tdEle.next();
                colspan=0

                for e in tdEleRemain:
                    originalE = e
                    e = pq(e)

                    if (e.attr("colspan")==None):
                        colspan+=1
                    else:
                        colspan+=int(e.attr("colspan"))

                    if (colspan>=yearIndex):
                        value=pq(unicode(str(e), errors='ignore')).html()
                        break

                if value=="":
                    data[name] = value
                    continue

                if (pq(value).children("strong").length>0):
                    if (name.startswith("sic")):
                        function = pq(value).children("strong").text()
                        data[name]=function
                    elif (name.startswith("outside firm")):
                        data["function " + name] = (str(pq(value).children().next()).replace("<br/>", ""))
                        function = pq(value).children("strong").text()
                        data[name] = function
                    elif (name.startswith("stock exchange")):
                        value = pq(value).text()
                        data[name] = value
                    else:
                        data[name]=(str(pq(value).children().next()).replace("<br/>", ""))
                        function = pq(value).children("strong").text()
                        data["function " + name]=function
                else:
                    value=pq(value).text()
                    if (name.startswith("sic")):
                        data[name]=value[0:4]
                    else:
                        data[name]=value

        return data

    def stringify_children(self, node):
        from lxml.etree import tostring
        from itertools import chain

        for x in node.itertext():
            pass

        parts = ([node.text] +
                 list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
                 [node.tail])
        # filter removes possible Nones in texts and tails
        return ''.join(filter(None, parts))

    def __parseYear__(self):
        p = self.d("#tablecol > tbody")
        tds=pq(p.children())[1]

        for e in tds:
            ee=pq(e).text()
            if (ee!=""):
                self.realYears.append(ee)

    def __parseHierarchyUrl__(self, url):
        d = pq(url=url)
        p = d("#hierarchy")
        div=pq(p.html())
        return (div.find("#iframeHierarchy").attr("src"))
