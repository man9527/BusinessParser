import companydataparser
import companies
import writeexcel
import filelist
import collections
import time
import logging

logger = logging.getLogger( __name__ )

class ParserController:
    def __init__(self, paths, sleep, sleepYear, logger, callback, designatedYears, filterCompanies):
        self.paths=paths
        self.companies=collections.OrderedDict({})
        self.failed_companies = collections.OrderedDict({})
        self.logger = logger
        self.callback = callback
        self.sleep = sleep
        self.sleepYear = sleepYear
        self.designatedYears = designatedYears
        self.filterCompanies = filterCompanies
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
            writer = writeexcel.CompanyDataWriter(file.replace(".html", ""))

            failedCompanies = []
            if not self.isRunning:
                self.logger("Interrupted by user. Abort")
                break

            for company in companyCollection:
                if not self.isRunning:
                    self.logger("Interrupted by user. Abort")
                    break

                if self.filterCompanies and company.id not in self.filterCompanies:
                    continue

                self.logger("===============================")
                self.logger("Begin to parse company data:" + company.name)
                self.logger("Url:" + company.url)

                try:
                    parser = companydataparser.CompanyDataParser(company.url, self.designatedYears)
                    result = parser.parse()
                    writer.append(company, result)
                    self.logger("End to parse " + company.name)

                except Exception as e:
                    failedCompanies.append(company)
                    self.logger("Failed to parse " + company.name)
                    self.logger(str(e))

                time.sleep(self.sleep)

            if failedCompanies:
                self.failed_companies[file]=failedCompanies
                self.saveSingleFailedCompanies(file, failedCompanies)

            self.logger("Writing to excel ...........................")
            writer.save()
            self.logger("Writing to excel done")

        self.isRunning = False
        self.callback()

    def parseHierarchyData(self):
        self.__parseHierarchyData__(self.companies)

    def parseHierarchyDataForFailedCompanies(self):
        failedCompanies = collections.OrderedDict(self.failed_companies)
        self.failed_companies.clear()
        self.__parseHierarchyData__(failedCompanies)

    def __parseHierarchyData__(self, companiesDict):

        self.isRunning = True

        for file, companyCollection in companiesDict.items():
            failedCompanies = []
            if not self.isRunning:
                self.logger("Interrupted by user. Abort")
                break

            for company in companyCollection:

                if not self.isRunning:
                    self.logger("Interrupted by user. Abort")
                    break

                if self.filterCompanies and company.id not in self.filterCompanies:
                    continue

                self.logger("===============================")
                self.logger("Begin to parse company hierarchy:" + company.name)
                self.logger("Url:" + company.url)

                try:
                    parser = companydataparser.CompanyDataParser(company.url, self.designatedYears, self.sleepYear)
                    hierarchy = parser.parseHierarchy()
                    logger.debug("Get parse result")
                    self.__writeHierarchy__(company, hierarchy)
                    self.logger("End to parse " + company.name)
                except Exception as e:
                    failedCompanies.append(company)
                    logger.debug("Get exception")
                    self.logger("Failed to parse " + company.name)
                    self.logger(str(e))

                logger.debug("Before sleep")
                time.sleep(self.sleep)

            if failedCompanies:
                self.failed_companies[file]=failedCompanies
                self.saveSingleFailedCompanies(file, failedCompanies)

        self.isRunning = False
        self.callback()

    def __writeToExcel(self, company, result):
        writer = writeexcel.CompanyDataWriter(company.name)
        writer.append(company, result)
        writer.save()

    def __writeHierarchy__(self, company, result):
        writer = writeexcel.HierarchyWriter()
        writer.write(company, result)

    def saveFailedCompanies(self):
        for file, companyCollection in self.failed_companies.items():
            output = []

            for company in companyCollection:
                output.append(company.id)

            file_ = open(file + "-failed-" + time.strftime("%Y%m%d-%H%M%S") + ".txt", 'w')
            file_.write(",".join(output))
            file_.close()

    def saveSingleFailedCompanies(self, file, companyCollection):
         output = []

         for company in companyCollection:
             output.append(company.id)

         file_ = open(file + "-failed-" + time.strftime("%Y%m%d-%H%M%S") + ".txt", 'w')
         file_.write(",".join(output))
         file_.close()





