import sys
import CompanyListParser
import companydataparser
import hierarchyparser
import controller
import gui

import logging
import sys

sys.stderr = sys.stdout
logging.basicConfig(level=logging.DEBUG)

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    #CompanyListParser.CompanyListParser().callme();
    #parser = companydataparser.CompanyDataParser(
    #    "https://www.corporateaffiliations.com/Subscriber/HistoricalComparison?selName=Aastrom+Biosciences%2c+Inc.&selID=000139270-0000&selYear=2015"
    #)

    #parser.load()
    #parser.parse(1)

    #h=hierarchyparser.HierarchyParser("https://www.corporateaffiliations.com/HierarchyByYear.aspx?pid=1941770000&cid=1941770000&year=2011")
    #h.parse()

    #parserController = controller.ParserController(["/Users/man9527/Downloads/2836"])
    #parserController.run()

    gui.MainWindow().show()

if __name__ == "__main__":
    main()