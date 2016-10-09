import companydataparser
import companies
import writeexcel
import filelist
import collections
import time

class ParserController:
    def __init__(self, paths, sleep, logger, callback, designatedYears):
        self.paths=paths
        self.companies=collections.OrderedDict({})
        self.logger = logger
        self.callback = callback
        self.sleep = sleep
        self.designatedYears = designatedYears
        self.isRunning = False
        self.__load__()

    def __load__(self):
        # loop through all files and load companies
        for path in self.paths:
            fileManager = filelist.FileManager(path);
            files = fileManager.getFiles();
            for file in files:
                if (file.endswith(".html")):
                    companyManager = companies.CompanyManager(file)
                    try:
                        companyManager.load()
                        self.companies[file]=companyManager.companies
                    except:
                        self.logger(file + " is not a valid html file")

    def parseCompanyData(self):
        # parse company data
        self.isRunning = True

        for file, companyCollection in self.companies.items():
            writer = writeexcel.CompanyDataWriter(file.replace(".html", ".xlsx"))
            i=0

            if not self.isRunning:
                self.logger("Interrupted by user. Abort")
                break

            for company in companyCollection:
                if not self.isRunning:
                    self.logger("Interrupted by user. Abort")
                    break

                self.logger("===============================")
                self.logger("Begin to parse company data:" + company.name)
                self.logger("Url:" + company.url)

                try:
                    parser = companydataparser.CompanyDataParser(company.url, self.designatedYears)
                    result = parser.parse()
                    writer.append(company, result)
                    self.logger("End to parse " + company.name)

                except Exception as e:
                    self.logger("Failed to parse " + company.name)
                    self.logger(str(e))

                time.sleep(self.sleep)
                i = i+1
                #if i>4:
                #    break

            writer.save()

        self.isRunning = False
        self.callback()


    def parseHierarchyData(self):
        self.isRunning = True

        i = 0
        for file, companyCollection in self.companies.items():
            if not self.isRunning:
                self.logger("Interrupted by user. Abort")
                break

            for company in companyCollection:

                if not self.isRunning:
                    self.logger("Interrupted by user. Abort")
                    break

                self.logger("===============================")
                self.logger("Begin to parse company hierarchy:" + company.name)
                self.logger("Url:" + company.url)

                try:
                    parser = companydataparser.CompanyDataParser(company.url, self.designatedYears)
                    hierarchy = parser.parseHierarchy()
                    self.__writeHierarchy__(company, hierarchy)
                    self.logger("End to parse " + company.name)
                except Exception as e:
                    self.logger("Failed to parse " + company.name)
                    self.logger(e)

                time.sleep(self.sleep)

                i = i + 1
                #if i > 5:
                #    break

        self.isRunning = False
        self.callback()

    def __writeToExcel(self, company, result):
        writer = writeexcel.CompanyDataWriter(company.name)
        writer.append(company, result)
        writer.save()

    def __writeHierarchy__(self, company, result):
        writer = writeexcel.HierarchyWriter()
        writer.write(company, result)




