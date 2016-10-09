from pyquery import PyQuery as pq
import domainjob

import logging

logger = logging.getLogger( __name__ )

class HierarchyParser:
    def __init__(self, url):
        self.url=url
        self.results=[]

    def parse(self):
        return self.__doParse__(self.url)

    def __doParse__(self, url):
        d = pq(url=url)
        p = d("#TreeView1 table")

        for ele in p:
            tr=pq(ele)
            tdCount = tr("td").length

            if tdCount > 1:
                tds = tr("td")
                td1=pq(tds[tdCount-2]).html()
                logger.debug(td1)
                idStartIndex = td1.index("'")
                idEndIndex = td1.index("'", idStartIndex+1)
                companyId = td1[idStartIndex+1:idEndIndex]

                td2=pq(tds[tdCount-1])
                companyName=td2(".unselected").text()

                if (companyName==""):
                    temp = td2(".selected").text()
                    companyName = temp[0:temp.index("(")]
                    location = temp[temp.index("("):]
                else:
                    location=td2(".location").text()

                city=location[1:location.index(", ")]
                state=location[location.index(", ")+2:-1]
                type = (td2("a").attr("title"))

                current = domainjob.HNode(companyId, type, tdCount, companyName, city, state)
                self.results.append(current)

        # build relation
        parent = {}

        prev = None
        logger.debug(url)
        for current in self.results:
            # handle the top node
            if prev==None and str(current.levelCount) not in parent:
                current.parent = current
                parent[str(current.levelCount+2)]=current
            else:
                if prev is not None:
                    if current.levelCount>prev.levelCount:
                        parent[str(current.levelCount)] = prev
                    current.parent=parent[str(current.levelCount)]

            prev=current

        return (self.results)