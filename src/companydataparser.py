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

        self.d = pq(Connector.get(self.url))

        self.realYears = []
        self.__parseYear__()
        self.sleepYear = sleepYear

        if not designatedYears:
            self.years = self.realYears
        else:
            self.years = designatedYears

    def parse(self):

        result = collections.OrderedDict({})

        for y in self.years:
            if y in self.realYears:
                index = self.realYears.index(y)+1
                result[y]=(self.__parseData__(index))

        logger.debug(result)
        return result

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
                    e = pq(e)

                    if (e.attr("colspan")==None):
                        colspan+=1
                    else:
                        colspan+=int(e.attr("colspan"))

                    if (colspan>=yearIndex):
                        value=e.html()
                        break

                if (pq(value).children("strong").length>0):
                    if (name.startswith("sic")):
                        function = pq(value).children("strong").text()
                        data[name]=function
                    if (name.startswith("outside firm")):
                        data["function " + name] = (str(pq(value).children().next()).replace("<br/>", ""))
                        function = pq(value).children("strong").text()
                        data[name] = function
                    if (name.startswith("stock exchange")):
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
