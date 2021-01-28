df = pasda data
df2 = doh data
# to do:
make a class where you pass in the doh, dhs, and fpp data
set the "doh_as_of_x_x_x" date as a variable


for index, row in df2.iterrows():
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
    
    #after this loop, rename columns to have _doh_as_of_x at the end
    #have user input x date at the beginning and add it to _DOH_as_of_ **
    
    
    #Then do one for dhs data
    #& create new date column for this
    
    #then do for fpp data
    #& new date column for this
    
    
