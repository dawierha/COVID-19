#from numpy import genfromtxt
import numpy as np
import csv

# class ListNotSameSizeError(Error):
#    """Raised when the input value is too small"""
#    pass

class CV19_data:

    def __init__(self, country, province, time_stamps, data):
        self.country = country
        self.province = province
        self.time_stamps = time_stamps
        self.general_data = data
        self.confirmed_cases = np.empty((np.size(self.general_data)))
        self.deaths = np.empty((np.size(self.general_data)))

    #Adds the lists of confirmed cases and total deaths
    #TODO
    def add_cases_death(self, other):
        if np.size(self.general_data) != np.size(other.general_data):
            #The lists are not the same size, raise error
            #raise ListNotSameSizeError
            print("deaths and confirmed_cases not same size")
            return 

        self.confirmed_cases = self.general_data
        self.deaths = other.general_data

        self.general_data = np.empty
        

    #Merges to data objects with the same country
    #TODO
    def merge(self, other):
        pass
    
    def __repr__(self):
        return "COVID_19 "+self.country+':'+self.province
    
    def __str__(self):
        return "COVID_19\n"+"Country: "+self.country+"\nProvince:"+self.province+"\nTime:"+str(self.time_stamps)+"\nData:"+str(self.general_data)

    
'''
Inputs:
    file_name - Name of the file containgin the cvs data
    countries - list of the countries to save data from. Takes all the provinces in that country. Empty returns all the countries.
    provinces - list of provinces to save data from. Empty returns no provinces.
    ig_provinces - list of provinces to ignore for a country specified in countries

Outputs a list of CV19_data objects

TODO:
    *Split US states correctly
    *raise error if the specified country or province is not found
    *include ignore list
        
'''
def read_cvs(file_name, countries=[], provinces=[], ig_provinces=[], data_start=4):
    #checks to see if 'countries' and 'provinces' are lists
    if not isinstance(countries, list):
        raise TypeError("\'countries\' must be a list")
    if not isinstance(provinces, list):
        raise TypeError("\'provinces\' must be a list")

    if countries == []:
        all_countries = True
    else:
        all_countries = False
      
    data_list = []
    added_countries = []
    with open(file_name) as file:
        csv_reader = csv.reader(file, delimiter=',')
        #line = file.readline()
        header = True
        for row in csv_reader:
            if header:
                time_stamps = np.array(row[data_start:]) #removes the first 4 elements since they does not contain time stamps
                header = False
            
            else:
                # print(line)
                if all_countries:
                    countries = [row[1]]

                for country in countries:
                    if country in row:
                        # print(line)
                        #parse the line and save data from country to cv19_data object
                        data = np.array(row[data_start:])
                        data = data.astype(np.float)
                        # print(data)
                        
                        #If the country exists in data_list, the data is appended
                        if country in added_countries:
                            for cv19_object in data_list:
                                if cv19_object.country == country:
                                    cv19_object.general_data += data
                                    break
                        else:
                            cv19_object = CV19_data(country, 'All', time_stamps, data)
                            data_list.append(cv19_object)
                            added_countries.append(country)
                    
                for province in provinces:
                    if province in row:
                        # print(line)
                        #parse the line and save data from province to cv19_data object
                        data = np.array(row[data_start:])
                        data = data.astype(np.float)
                        cv19_object = CV19_data(row[1], province, time_stamps, data)
                        data_list.append(cv19_object)
    
    return data_list
            
# path = '../csse_covid_19_data/csse_covid_19_time_series/'
# objects = read_cvs(path+'time_series_covid19_confirmed_global.csv', countries=['Canada', 'Australia'], provinces=['Alberta'])
# print(objects)
#objects = read_cvs(path+'time_series_19-covid-Confirmed.csv', countries=['Canada'])