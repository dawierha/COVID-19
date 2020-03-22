#from numpy import genfromtxt
import numpy as np


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
        return "COVID_19\n"+"Country: "+self.country+"\nProvince:"+self.province+"\nTime:"+str(self.time_stamps)+"\nData:"+str(self.data)

    
'''
Inputs:
    file_name - Name of the file containgin the cvs data
    countries - list of the countries to save data from. Takes all the provinces in that country. Empty returns all the countries.
    provinces - list of provinces to save data from. Empty returns no provinces.

Outputs a list of CV19_data objects

TODO:
    *Split US states correctly
    *Merge countries marked with all
    *raise error if the specified country or province is not found
        
'''
def read_cvs(file_name, countries=[], provinces=[], data_start=4):
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
    with open(file_name) as file:
        line = file.readline()
        time_stamps = np.array(line.strip('\n').split(',')[data_start:-1]) #removes the first 4 elements since they does not contain time stamps
        for line in file:
            # print(line)
            if all_countries:
                line_list = line.strip('\n').split(',')
                countries = [line_list[1]]

            for country in countries:
                if country in line:
                    #print(line)
                    #parse the line and save data from country to cv19_data object
                    data = np.array(line.strip('\n').split(',')[data_start:-1])
                    data = data.astype(np.float)
                    cv19_object = CV19_data(country, 'All', time_stamps, data)
                    data_list.append(cv19_object)
                
            for province in provinces:
                if province in line:
                    #print(line)
                    #parse the line and save data from province to cv19_data object
                    line_list = line.strip('\n').split(',')
                    data = np.array(line_list[data_start:-1])
                    data = data.astype(np.float)
                    cv19_object = CV19_data(line_list[1], province, time_stamps, data)
                    data_list.append(cv19_object)
    
    #Merges objects with the same country and province==All
    #TODO
    for obj_1 in data_list:
        for obj_2 in data_list:
            if (obj_1.country == obj_2.country) and (obj_1.province == 'All') and (obj_2.province == 'All'):
                pass
                #print("merge")
                
    return data_list
            
#path = '../csse_covid_19_data/csse_covid_19_time_series/'
#path+'/time_series_19-covid-Deaths.csv'
#objects = read_cvs(path+'time_series_19-covid-Confirmed.csv', countries=['Sweden', 'Norway'], provinces=['French Guiana'])
#objects = read_cvs(path+'time_series_19-covid-Confirmed.csv', countries=['Canada'])