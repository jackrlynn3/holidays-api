from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests

# Make sure to add config.py file
from config import holidays_api

# Holiday: Class to hold holidays, including name and date
class Holiday:

    # Docstring
    """
    Holiday
    --------
    + name: str
    + date: datetime
    --------
    __init__(name, date_str, date_format='%Y-%m-%d'): None
    __str__(): str
    Getters: name, date
    Setters: name, date
    """
    
    # Initializer: takes in holiday name and date and sets variables
    def __init__(self, name, date_str, date_format='%Y-%m-%d'):
        self._name = name
        self._date = datetime.strptime(date_str, date_format)    
    
    # String format: return name of holiday
    def __str__ (self):
        return self._name
    
    # Getters

    # Name getter
    @property
    def name(self):
        return self._name
    
    # Date getter
    @property
    def date(self):
        return self._date
    
    # Setters

    # Name setter
    @name.setter
    def name(self, new_name):
        self._name = new_name
    
    # Date setter
    @date.setter
    def date(self, new_date_str, date_format):
        self._date = datetime.strptime(new_date_str, date_format)  
          
           
class HolidayList:

    def __init__(self):
        self._inner_holidays = []

    # inner_holidays getter
    @property
    def inner_holidays(self):
        return self._inner_holidays
   
    # addHoliday: add holiday to holiday list
    #   holidayObj: (Holiday) instance of holiday to add
    #   verbose: (bool) whether or not to print out message; default False
    def addHoliday(self, holiday_obj, verbose=False):
        
        # Make sure the input holiday is a holiday object
        if (type(holiday_obj) == Holiday):
            
                # Add holiday to holiday list
                self._inner_holidays.append(holiday_obj)

                # Print add message
                if (verbose):
                    print(f'New holiday ("{holiday_obj}") added!\n')

        # If not holiday instance, throw an exception
        else:
            raise Exception("Input obejct must be Holiday type!")

    # findHoliday: search and return specific holiday in list
    #   holiday_name: (str) name of the holiday
    #   date_str: (str) string format of date
    #   date_format: (str) format of the date; default is '%Y-%m-%d'
    #   return: (Holiday) holiday object if found; None otherwise
    def findHoliday(self, holiday_name, date_str, date_format='%Y-%m-%d'):
        
        # Find holiday that matches name and date
        date = datetime.strptime(date_str, date_format)
        for holiday in self._inner_holidays:
            if (holiday.name == holiday_name and holiday.date == date):
                return holiday
        
        # Return none if no holiday found
        return None
    
    # removeHoliday: search and remove specific holiday in list
    #   holiday_name: (str) name of the holiday
    #   date_str: (str) string format of date
    #   date_format: (str) format of the date; default is '%Y-%m-%d'
    #   verbose: (bool) whether or not to print out message; default False
    def removeHoliday(self, holiday_name, date_str, date_format='%Y-%m-%d', verbose=False):

        # Find index of item
        j = -1
        date = datetime.strptime(date_str, date_format)
        for i in range(len(self._inner_holidays)):
            holiday = self._inner_holidays[i]
            if (holiday.name == holiday_name and holiday.date == date):
                j = i
        
        # If never found, return error
        if (j == -1):
            if (verbose):
                print(f'Holiday ("{holiday_name}", "{date_str}") could not be found, so no holiday has been deleted!')
        
        # Delete object
        else:
            self._inner_holidays.pop(j)
            if (verbose):
                print(f'Holiday ("{holiday_name}", "{date_str}") has been deleted!')

    # readJSON: read in holiday data as JSON format and save to _inner_holidays
    #   f_loc: (str) location of JSON file
    def readJSON(self, f_loc):

        # Read in data from json file location
        with open(f_loc, 'r') as f:
            data = json.load(f)['holidays']

            # Iterate through each JSON obj and create a new holiday
            for holiday_json in data:
                holiday = Holiday(holiday_json['name'], holiday_json['date'])
                self.addHoliday(holiday)

    # saveToJSON: save JSON file with holidays
    #   f_loc: (str) location and name of file to save
    #   date_format: (str) format of the date; default is '%Y-%m-%d'
    def saveToJSON(self, f_loc, date_format='%Y-%m-%d'):

        # Convert data into dictionary format
        holiday_dict = []
        for holiday in self._inner_holidays:
            this_holiday = dict()
            this_holiday['name'] = holiday.name
            this_holiday['date'] = holiday.date.strftime(date_format)
            holiday_dict.append(this_holiday)

        # Write file
        with open(f_loc, 'w') as f:
            json.dump(holiday_dict, f)
    
    # scrapeHolidays: used to scrape holidays from TimeAndDate holidays API
    #   verbose: (bool) whether or not to print out message; default False
    #   NOTE: URL of website should be saved in the config.py file as holiday_api
    def scrapeHolidays(self, verbose=False):

        # Get 5 year period
        for year in range(int(datetime.today().year)-2, int(datetime.today().year)+3):

            try:

                # Make connection
                connection = requests.get(holidays_api + str(year))

                # Pass into beautiful Soup
                soup = BeautifulSoup(connection.text,'html.parser')
                table = soup.find('table', attrs={'id':'holidays-table'})
                table_data = table.find('tbody')
                
                # Iterate through each holiday
                for datum in table_data.find_all_next('tr'):
                    
                    # Surround in try-except block to try to get as many data as possible
                    try:

                        # Get the date
                        date_str = str(datum.find('th', attrs={'class': 'nw'}))
                        date = f'{date_str[date_str.index("nw")+4 : date_str.index("</th>")]}, {year}'

                        # Get the holiday
                        holiday_str = str(datum.find('a'))
                        holiday = holiday_str[holiday_str.index('>')+1:]
                        holiday = holiday[:holiday.index('<')]

                        # Add holiday to list
                        if (self.findHoliday(holiday, date, date_format='%b %d, %Y') == None):
                            this_holiday = Holiday(holiday, date, date_format='%b %d, %Y')
                            self._inner_holidays.append(this_holiday)

                            # Print success message
                            if (verbose):
                                print(f'"{holiday}" ({date}) has been added!')

                        # Add message if holiday is already in list
                        else:
                            if (verbose):
                                print(f'"{holiday}" ({date}) is already in the list!')
                    
                    # Rows that could not be formed into holidays
                    except:
                        if (verbose):
                            print('A holiday could not be added!')  
            
            # Throw a connection error if arrises
            except:
                print('Connection error! Please check your connection!')

    # numHolidays(): get the number of holidays
    #   return: (str) the count of holidays contained in project
    def numHolidays(self):
        return len(self._inner_holidays)
    
    # filterHolidaysByWeek: get the holidays of a certain week in a certain year
    #   year: (int) year of the holidays
    #   week_number: (int) week number (range is 1 to 52, inclusive)
    #   return: (list(Holiday)) holidays withing that timeframe
    def filterHolidaysByWeek(self, year, week_number):

        # Get only dates with week number
        holidays = list(filter(lambda holiday: holiday.date.isocalendar()[1] == week_number
            and holiday.date.year == year, self._inner_holidays))

        # return your holidays
        return holidays


    def displayHolidaysInWeek(self, holiday_list, should_print=False):

        format_holidays = []
        for holiday in holiday_list:
            format_holidays.append(f'{holiday} ({holiday.date.date()})')

        # Give option to print holidays within function 
        if (should_print):
            for string in format_holidays:
                print(string)

        # Return list of formatted holidays
        return format_holidays

    #def getWeather(self, weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    #def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

def main():

    holiday = Holiday('My birthday', '1999-09-03')
    christmas = Holiday('Christmas', '2022-12-25')
    print(type(holiday) == Holiday)

    holidays = HolidayList()
    holidays.addHoliday(holiday)
    holidays.addHoliday(holiday)
    holidays.addHoliday(christmas)
    print(f'Search holidays, should return Holiday obj: {holidays.findHoliday("My birthday", "1999-09-03")}')
    print(f'Search holidays, should return None: {holidays.findHoliday("My birthday", "1999-09-04")}')
    print(f'Search holidays, should return Holiday obj: {holidays.findHoliday("My birthday", "1999-09-03")}')
    print(f'Delete holidays, should succeed: {holidays.removeHoliday("My birthday", "1999-09-03")}')
    print(f'Delete holidays, should fail: {holidays.removeHoliday("My birthday", "1999-09-03")}')
    holidays.readJSON('data/holidays.json')
    holidays.saveToJSON('data/holidays_temp.json')
    holidays.scrapeHolidays()
    print(holidays.numHolidays())
    fourth_wk_holidays = holidays.filterHolidaysByWeek(2022, 4)
    print('Fourth week holidays of 2022:')
    holidays.displayHolidaysInWeek(fourth_wk_holidays, should_print=True)

    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main()