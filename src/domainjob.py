
class HNode:
    def __init__(self, id, type, levelCount, name, city, state):
        self.levelCount=levelCount
        self.name=name
        self.children=[]
        self.id=id
        self.type=type
        self.visited=False
        self.city=city
        self.state=state
        self.parent=None

    def addChild(self, child):
        self.children.append(child)

class Company:
    def __init__(self, id, name, url, exportFileName):
        self.id=id
        self.name = name
        self.url = url
        self.exportFileName=exportFileName

    def __str__(self):
        return self.id + "," + self.name + "," + self.url

    def __repr__(self):
        return self.id + "," + self.name + "," + self.url