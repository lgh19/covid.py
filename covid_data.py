
#example of how to run code:
# a = CovidData('DOH_PASDA.csv')
# the PASDA file is passed into the CovidData class, which then scrapes the DOH LTFC data set and FPP data set from the web
#the output of the code is one csv file with the relevant columns of these 3 files  combined

from bs4 import BeautifulSoup
import requests
import pandas as pd
from fuzzywuzzy import fuzz
from openpyxl import load_workbook
import re

class CovidData:
    pasdaData = ""
    dohfile = ""
    fppfile = ''
    global ltcfdf
    global dohdf
    global fppdf
    global dohColumnName
    global doh_last_updated
    global fpp_last_updated

    def __init__(self, pasdaData):
        self.ltcfdf = pd.DataFrame
        self.ltcfdf = pd.read_csv(pasdaData)
        from bs4 import BeautifulSoup
        import requests


        r = requests.get("https://www.health.pa.gov/topics/disease/coronavirus/Pages/LTCF-Data.aspx")
        soup = BeautifulSoup(r.text, 'html.parser')

        doc_urls = []
        doh_dates = []
        for link in soup.find_all('a'):
            url = link.get('href', 'No Link Found')
            if re.search('xlsx', url) is not None:
                doh_dates.append(link.next_sibling)
                doc_urls.append(url)
        # print doc_urls
        # print doh_dates
        assert len(doc_urls) == 4  # Verify that the web site only lists four XSLX files.
        self.doh_last_updated = doh_dates[0]
        fullurl = "https://www.health.pa.gov" + doc_urls[0]

        r = requests.get(fullurl)

        open('DOH_Data.xlsx', 'w').write(r.content)

        r = requests.get(
            "https://www.health.pa.gov/topics/programs/immunizations/Pages/COVID-19-Vaccine-Providers.aspx")
        soup = BeautifulSoup(r.text, 'html.parser')

        doc_urls = []
        fpp_dates = []
        for link in soup.find_all('a'):
            url = link.get('href', 'No Link Found')
            if re.search('xlsx', url) is not None:
                fpp_dates.append(link.next_sibling)
                doc_urls.append(url)

        fullurl = "https://www.health.pa.gov" + doc_urls[5]
        self.fpp_last_updated = fpp_dates[5]
        r = requests.get(fullurl)
        open('FPP_Data.xlsx', 'w').write(r.content)

        wb = load_workbook('FPP_Data.xlsx')
        wb2 = load_workbook('DOH_Data.xlsx')

        ws = wb['contour-export']

        ws2 = wb2['Sheet1']

        df = pd.DataFrame(ws.values)
        df.rename(columns={0: u"Facility Name", 1: u'Address', 2: u"City", 3: u"County", 4: u"Zip Code", 5: u'Contact',
                           6: u'Phone', 7: u'Group', 8: u'Phase', 9: u'Program', 10: u'Number_Beds', 11: u"clinicdt1",
                           12: u"clinicdt2", 13: u"clinicdt3", 14: u"clinicdt4", 15: u"clinicdt5", 16: u"clinicdt6",
                           17: u"clinicdt7", 18: u"clinicdt8", 19: u"clinicdt9", 20: u"clinicdt10"}, inplace=True)

        df2 = pd.DataFrame(ws2.values)

        df2.rename(columns={0: u"FACID", 1: u"NAME", 2: u"CITY", 3: u"COUNTY", 4: u"ALL_BEDS", 5: u"CURRENT_CENSUS",
                            6: u"Resident Cases to Display",
                            7: u"Resident Deaths to Display", 8: u"Staff Cases to Display"}, inplace=True)

        df = df.iloc[1:]
        df2 = df2.iloc[1:]

        df.to_csv("FPP_CSV1.csv", encoding='utf-8')

        df2.to_csv("DOH_CSV1.csv", encoding='utf-8')

        self.fppdf = pd.read_csv("FPP_CSV1.csv")

        self.dohdf = pd.read_csv("DOH_CSV1.csv")

        self.addDOHData()
        

    def addDOHData(self):
        print
        print "Adding DOH Covid Data"
        print


        def isNaN(string):
            return string != string

        self.dohdf.rename(columns={'Resident Cases to Display': 'Resident_Cases_to_Display'}, inplace=True)
        self.dohdf.rename(columns={'Resident Deaths to Display': 'Resident_Deaths_to_Display'}, inplace=True)
        self.dohdf.rename(columns={'Staff Cases to Display': 'Staff_Cases_to_Display'}, inplace=True)
        self.ltcfdf['ALL_BEDS'] = ''
        self.ltcfdf['CURRENT_CENSUS'] = ''
        self.ltcfdf['Resident_Cases_to_Display'] = ''
        self.ltcfdf['Resident_Deaths_to_Display'] = ''
        self.ltcfdf['Staff_Cases_to_Display'] = ''

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
                    #print "match"
                    tempbeds = row.ALL_BEDS
                    tempcensus = row.CURRENT_CENSUS
                    tempres = row.Resident_Cases_to_Display
                    tempresdeath = row.Resident_Deaths_to_Display
                    tempstaff = row.Staff_Cases_to_Display

                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] == tempfacid, 'ALL_BEDS'] = tempbeds
                  #  print(tempbeds)
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] == tempfacid, 'CURRENT_CENSUS'] = tempcensus
                  #  print(tempcensus)
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] == tempfacid, 'Resident_Cases_to_Display'] = tempres
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] == tempfacid, 'Resident_Deaths_to_Display'] = tempresdeath
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_I'] == tempfacid, 'Staff_Cases_to_Display'] = tempstaff

        self.ltcfdf['DOH_Data_Last_Updated'] = self.doh_last_updated
        self.ltcfdf = self.ltcfdf
        print "Done Adding DOH Covid Data"
        print
        self.addFPPData()

    def addFPPData(self):
        self.ltcfdf['clinicdt1'] = ''
        self.ltcfdf['clinicdt1'] = self.ltcfdf["clinicdt1"].astype(str)
        self.ltcfdf['clinicdt2'] = ''
        self.ltcfdf['clinicdt2'] = self.ltcfdf["clinicdt2"].astype(str)
        self.ltcfdf['clinicdt3'] = ''
        self.ltcfdf['clinicdt3'] = self.ltcfdf["clinicdt3"].astype(str)
        self.ltcfdf['clinicdt4'] = ''
        self.ltcfdf['clinicdt4'] = self.ltcfdf["clinicdt4"].astype(str)
        self.ltcfdf['clinicdt5'] = ''
        self.ltcfdf['clinicdt5'] = self.ltcfdf["clinicdt5"].astype(str)
        self.ltcfdf['clinicdt6'] = ''
        self.ltcfdf['clinicdt6'] = self.ltcfdf["clinicdt6"].astype(str)
        self.ltcfdf['clinicdt7'] = ''
        self.ltcfdf['clinicdt7'] = self.ltcfdf["clinicdt7"].astype(str)
        self.ltcfdf['clinicdt8'] = ''
        self.ltcfdf['clinicdt8'] = self.ltcfdf["clinicdt8"].astype(str)
        self.ltcfdf['clinicdt9'] = ''
        self.ltcfdf['clinicdt9'] = self.ltcfdf["clinicdt9"].astype(str)
        self.ltcfdf['clinicdt10'] = ''
        self.ltcfdf['clinicdt10'] = self.ltcfdf["clinicdt10"].astype(str)
        print "Adding FPP Data"
        print

        
        print
        for index, row in self.fppdf.iterrows():
            tempStr = (self.fppdf.at[index, 'Facility Name'])
            tempStr = str(tempStr)
            tempfacility = self.fppdf.at[index, 'Facility Name']
            tempaddress = self.fppdf.at[index, 'Address']
        #    temptype = self.fppdf.at[index, 'Facility Type']
            tempphase = self.fppdf.at[index, 'Phase']
            tempfirstc = self.fppdf.at[index, 'clinicdt1']
            tempsecondc = self.fppdf.at[index, 'clinicdt2']
            tempthirdc = self.fppdf.at[index, 'clinicdt3']
            tempfourthc = self.fppdf.at[index, 'clinicdt4']
            tempfifthc = self.fppdf.at[index, 'clinicdt5']
            tempsixthc = self.fppdf.at[index, 'clinicdt6']
            tempseventhc = self.fppdf.at[index, 'clinicdt7']
            tempeightc = self.fppdf.at[index, 'clinicdt8']
            temp9thc = self.fppdf.at[index, 'clinicdt9']
            temp10thc = self.fppdf.at[index, 'clinicdt10']

            for index, row in self.ltcfdf.iterrows():
                Str1 = (self.ltcfdf.at[index, 'FACILITY_N'])
                Str1 = str(Str1)
                ratio = fuzz.ratio(Str1.lower(), tempStr.lower())
                if (85 < ratio < 90):
                    self.ltcfdf.at[index, 'flag_FPP'] = True
                    break
                elif (ratio >= 90):
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'Facility'] = tempfacility
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'Phase'] = tempphase
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicdt1'] = tempfirstc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicdt2'] = tempsecondc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicdt3'] = tempthirdc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicdt4'] = tempfourthc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicdt5'] = tempfifthc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicd6'] = tempsixthc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicdt7'] = tempseventhc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicdt8'] = tempeightc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicdt9'] = temp9thc
                    self.ltcfdf.loc[self.ltcfdf['FACILITY_N'] == Str1, 'clinicd10'] = temp10thc
                    break
        
        self.ltcfdf['FPP_Data_Last_Updated'] = self.fpp_last_updated
        self.ltcfdf = self.ltcfdf
        print "Done Adding FPP Data"
        self.writeToFile()

    def writeToFile(self):
        print
        b = "COVID19_Vaccine_Data_LTCF.csv"
        b = str(b)
        self.ltcfdf.to_csv(b)
        print("output file: "),
        print(b)
        
