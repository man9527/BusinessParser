import companies

class CompanyListParser:
    def callme(self):
        #fileManager = filelist.FileManager("/Users/man9527/Downloads/2836")
        #print(fileManager.getFiles())

        companyManager = companies.CompanyManager("/Users/man9527/Downloads/2836")
        companyManager.load()