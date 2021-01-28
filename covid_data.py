class CovidData:
    allLTCFData = ""
    dohfile = ""
    dhsfile1 = ''
    dhsfile2 = ''
    dhsfile3 = ''
    fppfiel = ''
    global ltcfdf 
    global dohdf
    global dhsdf1
    global dhsdf2
    global dhsdf3
    global fppdf
    global dohColumnName
    global dhs1ColumnName

    def __init__(self, allLTCFData, dohfilename):
        self.ltcfdf = pd.DataFrame()
        self.allLTCFData = allLTCFData
        self.ltcfdf = pd.read_csv(allLTCFData)
        
        self.dohdf = pd.read_csv(dohfilename)
      #  self.dhsdf1 = pd.read_csv(dhsfile1)
      #  self.dhsdf2 = pd.read_csv(dhsfile2)
      #  self.dhsdf3 = pd.read_csv(dhsfile3)
      #  self.fppdf = pd.read_csv(fppfile)
        userDate = raw_input("When was DOH data last updated: (day/month/year) : ")
        userDate = str(userDate)
        self.dohColumnName = "_DOH_last_updated_" + userDate
        self.addDOHData()
        
    def addDOHData(self):
        def isNaN(string):
            return string != string

        self.dohdf.rename(columns={'Resident Cases to Display': 'Resident_Cases_to_Display'}, inplace=True)
        self.dohdf.rename(columns = {'Resident Deaths to Display':'Resident_Deaths_to_Display'}, inplace = True)
        self.dohdf.rename(columns = {'Staff Cases to Display':'Staff_Cases_to_Display'}, inplace = True) 
        self.ltcfdf['ALL_BEDS'] = ''
        self.ltcfdf['CURRENT_CENSUS'] = ''
        self.ltcfdf['Resident_Cases_to_Display'] = ''
        self.ltcfdf['Resident_Deaths_to_Display'] = ''
        self.ltcfdf['Staff_Cases_to_Display']= ''
        
        i = 0

        for index, row in self.ltcfdf.iterrows():
            tempfacid = row.FACILITY_I
            tempbeds = ''
            tempcensus = ''
            tempres = ''
            tempresdeath = ''
            tempstaff = ''
            for index, row in self.dohdf.iterrows():
                if row.FACID != tempfacid:
                    pass
                else:
                    tempbeds = row.ALL_BEDS
                 #   print(tempbeds)
                    tempcensus = row.CURRENT_CENSUS
                  #  print(tempcensus)
                    tempres = row.Resident_Cases_to_Display
                  #  print(tempres)
                    tempresdeath = row.Resident_Deaths_to_Display
                  #  print(tempresdeath)
                    tempstaff = row.Staff_Cases_to_Display

                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] ==tempfacid, 'ALL_BEDS']= tempbeds
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] ==tempfacid, 'CURRENT_CENSUS'] =  tempcensus
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] ==tempfacid, 'Resident_Cases_to_Display'] = tempres
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] ==tempfacid, 'Resident_Deaths_to_Display'] =  tempresdeath
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] ==tempfacid, 'Staff_Cases_to_Display'] = tempstaff

                
        resCaseColumnName = 'Resident_Cases_to_Display' + self.dohColumnName
        resDeathsColumnName = 'Resident_Deaths_to_Display' + self.dohColumnName
        staffColumnName = 'Staff_Cases_to_Display' + self.dohColumnName
        bedColName = 'ALL_BEDS' + self.dohColumnName
        censusColName = 'CURRENT_CENSUS' + self.dohColumnName
        self.ltcfdf.rename(columns={'Resident_Cases_to_Display': resCaseColumnName}, inplace=True)
        self.ltcfdf.rename(columns={'Resident_Deaths_to_Display': resDeathsColumnName}, inplace=True)
        self.ltcfdf.rename(columns={'Staff_Cases_to_Display': staffColumnName}, inplace=True)
        self.ltcfdf.rename(columns={'ALL_BEDS': bedColName}, inplace=True)
        self.ltcfdf.rename(columns={'CURRENT_CENSUS': censusColName}, inplace=True)
        self.ltcfdf = self.ltcfdf
        self.writeToFile()
        
    def writeToFile(self):
        self.ltcfdf.columns
        userName = raw_input("csv file name (ish): ")
        userName = str(userName)
        b = userName + "_LTCF_Covid_Data.csv"
        b = str(b)
        self.ltcfdf.columns
        self.ltcfdf.to_csv(b)
        print("output file: "),
        print(b)

