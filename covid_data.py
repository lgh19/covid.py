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

    def __init__(self, allLTCFData, dohfilename, dhsfile1, dhsfile2, dhsfile3, fppfile):
        self.ltcfdf = pd.DataFrame(data=None, columns=None)
        self.allLTCFData = allLTCFData
        self.ltcfdf = pd.read_csv(allLTCFData)

        print(self.ltcfdf)
        
        self.dohdf = pd.read_csv(dohfilename)
        self.dhsdf1 = pd.read_csv(dhsfile1)
        self.dhsdf2 = pd.read_csv(dhsfile2)
        self.dhsdf3 = pd.read_csv(dhsfile3)
        self.fppdf = pd.read_csv(fppfile)
        userDate = raw_input("When was DOH data last updated: (day/month/year) : ")
        userDate = str(userDate)
        self.dohColumnName = "_DOH_last_updated_" + userDate
        
    def addDOHData(self):
        def isNaN(string):
            return string != string

        self.dohdf.rename(columns={'Resident Cases to Display': 'Resident_Cases_to_Display'}, inplace=True)
        self.dohdf.rename(columns = {'Resident Deaths to Display':'Resident_Deaths_to_Display'}, inplace = True)
        self.dohdf.rename(columns = {'Staff Cases to Display':'Staff_Cases_to_Display'}, inplace = True) 
        ltcfdf['ALL_BEDS'] = ''
        ltcfdf['CURRENT_CENSUS'] = ''
        ltcfdf['Resident_Cases_to_Display'] = ''
        ltcfdf['Resident_Deaths_to_Display'] = ''
        ltcfdf['Staff_Cases_to_Display']= ''
        
        for index, row in ltcf.iterrows():
            tempfacid = row.FACID
            tempbeds = ''
            tempcensus = ''
            tempres = ''
            tempresdeath = ''
            tempstaff = ''
            for index, row in df.iterrows():
                if row.FACILITY_I != tempfacid:
                    pass
                else:
                    tempbeds = row.ALL_BEDS
                    tempcensus = row.CURRENT_CENSUS
                    tempres = row.Resident_Cases_to_Display
                    tempresdeath = row.Resident_Deaths_to_Display
                    tempstaff = row.Staff_Cases_to_Display
            df2.set_value(index, 'ALL_BEDS', tempbeds)
            df2.set_value(index, 'CURRENT_CENSUS', tempcensus)
            df2.set_value(index, 'Resident_Cases_to_Display', tempres)
            df2.set_value(index, 'Resident_Deaths_to_Display', tempresdeath)
            df2.set_value(index, 'Staff_Cases_to_Display', tempstaff)
            
            resCaseColumnName = 'Resident_Cases_to_Display'+ self.dohColumnName
            resDeathsColumnName = 'Resident_Deaths_to_Display' + self.dohColumnName
            staffColumnName = 'Staff_Cases_to_Display' + self.dohColumnName
            bedColName = 'ALL_BEDS' + self.dohColumnName
            censusColName = 'CURRENT_CENSUS' + self.dohColumnName
            self.ltcfdf.rename(columns={'Resident_Cases_to_Display': resCaseColumnName }, inplace=True)
            self.ltcf.rename(columns={'Resident_Deaths_to_Display':resDeathsColumnName}, inplace=True)
            self.ltcf.rename(columns={'Staff_Cases_to_Display': staffColumnName}, inplace=True)
            self.ltcf.rename(columns={'ALL_BEDS': bedColName}, inplace=True)
            self.ltcf.rename(columns={'CURRENT_CENSUS': censusColName}, inplace=True)


            
    
    #Then do one for dhs data
    #& create new date column for this
    
    #then do for fpp data
    #& new date column for this
    
    
