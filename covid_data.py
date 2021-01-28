import pandas as pd
from fuzzywuzzy import fuzz


class CovidData:
    allLTCFData = ""
    dohfile = ""
    fppfile = ''
    global ltcfdf 
    global dohdf
    global fppdf
    global dohColumnName

    def __init__(self, allLTCFData, dohfilename, fppfile):
        self.ltcfdf = pd.DataFrame()
        self.allLTCFData = allLTCFData
        self.ltcfdf = pd.read_csv(allLTCFData)
        self.dohdf = pd.read_csv(dohfilename)
        self.fppdf = pd.read_csv(fppfile)
        self.addDOHData()
        
    def addDOHData(self):
        print
        print "Adding DOH Covid Data"
        print
        userDate = raw_input("When was DOH data last updated (month/day/year) : ")
        userDate = str(userDate)
        self.dohColumnName = "_DOH_last_updated_" + userDate
        
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
                    tempcensus = row.CURRENT_CENSUS
                    tempres = row.Resident_Cases_to_Display
                    tempresdeath = row.Resident_Deaths_to_Display
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
        print "Done Adding DOH Covid Data"
        print
        self.addFPPData()
        
    def addFPPData(self):
        self.ltcfdf['First Clinic'] = ''
        self.ltcfdf['First Clinic'] = self.ltcfdf["First Clinic"].astype(str)
        self.ltcfdf['2nd Clinic'] = ''
        self.ltcfdf['2nd Clinic'] = self.ltcfdf["2nd Clinic"].astype(str)
        self.ltcfdf['3rd Clinic'] = ''
        self.ltcfdf['3rd Clinic'] = self.ltcfdf["3rd Clinic"].astype(str)
        self.ltcfdf['4th Clinic'] = ''
        self.ltcfdf['4th Clinic'] = self.ltcfdf["4th Clinic"].astype(str)
        self.ltcfdf['5th Clinic'] = ''
        self.ltcfdf['5th Clinic'] = self.ltcfdf["5th Clinic"].astype(str)
        self.ltcfdf['6th Clinic'] = ''
        self.ltcfdf['6th Clinic'] = self.ltcfdf["6th Clinic"].astype(str)
        print "Adding FPP Data"
        print
        userDateFPP = raw_input("FPP Data is from week of (month/day/year) : ")
        userDateFPP = str(userDateFPP)
        FPPColName = "_FPP_Data_Week_of_" + userDateFPP
        print 
        for index, row in self.fppdf.iterrows():
            tempStr = (self.fppdf.at[index, 'Facility Name'])
            tempStr = str(tempStr)
            tempfacility = self.fppdf.at[index, 'Facility Name']
            tempaddress = self.fppdf.at[index, 'Address']
            temptype = self.fppdf.at[index, 'Type']
            temppharm = self.fppdf.at[index, 'Pharmacy']
            tempfirstc = self.fppdf.at[index, 'First Clinic']
            tempsecondc = self.fppdf.at[index, '2nd Clinic']
            tempthirdc = self.fppdf.at[index, '3rd Clinic']
            tempfourthc = self.fppdf.at[index, '4th Clinic']
            tempfifthc = self.fppdf.at[index, '5th Clinic']
            tempsixthc = self.fppdf.at[index, '6th Clinic']

            for index, row in self.ltcfdf.iterrows():
                Str1 = (self.ltcfdf.at[index, 'FACILITY_N'])
                Str1 = str(Str1)
                ratio = fuzz.ratio(Str1.lower(), tempStr.lower())
                if (85 < ratio < 90):
                    self.ltcfdf.at[index, 'flag_FPP'] = True
                    break
                elif (ratio >= 90):
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'Facility'] = tempfacility
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'Pharmacy'] = temppharm
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'Type'] = temptype
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'First Clinic'] = tempfirstc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, '2nd Clinic'] = tempsecondc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, '3rd Clinic'] = tempthirdc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, '4th Clinic'] = tempfourthc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, '5th Clinic'] = tempfifthc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, '6th Clinic'] = tempsixthc
                    break
                    
        facColName = 'Facility' + FPPColName
        self.ltcfdf.rename(columns={'Facility': facColName}, inplace=True)
        pharmColName = 'Pharmacy' + FPPColName
        self.ltcfdf.rename(columns={'Pharmacy': pharmColName}, inplace=True)
        typeColName = 'Type' + FPPColName
        self.ltcfdf.rename(columns={'Type': typeColName}, inplace=True)
        fcColName = 'First Clinic' + FPPColName
        self.ltcfdf.rename(columns={'First Clinic': fcColName}, inplace=True)
        scColName = '2nd Clinic' + FPPColName
        self.ltcfdf.rename(columns={'2nd Clinic': scColName}, inplace=True)
        tcColName = '3rd Clinic' + FPPColName
        self.ltcfdf.rename(columns={'Third Clinic': tcColName}, inplace=True)
        fcColName = '4th Clinic' + FPPColName
        self.ltcfdf.rename(columns={'4th Clinic': fcColName}, inplace=True)
        ftcColName = '5th Clinic' + FPPColName
        self.ltcfdf.rename(columns={'5th Clinic': ftcColName}, inplace=True)
        scColName = '6th Clinic' + FPPColName
        self.ltcfdf.rename(columns={'6th Clinic': scColName}, inplace=True)
        
        self.ltcfdf = self.ltcfdf
        print "Done Adding FPP Data"      
        self.writeToFile()
        
    def writeToFile(self):
        print
        self.ltcfdf.columns
        userName = raw_input("csv file name: ")
        userName = str(userName)
        b = userName + "_LTCF_Covid_Data.csv"
        b = str(b)
        self.ltcfdf.columns
        self.ltcfdf.to_csv(b)
        print("output file: "),
        print(b)
