from datetime import datetime
import datetime as dt
import json
from bs4 import BeautifulSoup
import requests

# Make sure to add config.py file
from config import holidays_api
from config import weather_api_future
from config import weather_api_past
from config import weather_headers

# int_input: used for integer inputs (PULLED FROM TOURNAMENT TRACKER ASSIGNMENT)
#   minimum: (int, def -1) the minimum of acceptable range, inclusive; leave -1 no lower bound
#   maximum: (int, def -1) the maximum of acceptable range, inclusive; leave -1 no upper bound
#   input_string: (str, def "  Selection: ") the input prompt message
#   return: (int) integer input
def int_input(minimum=-1, maximum=-1, input_string="  Selection: "):

    # Initialize helper variables
    input_1_valid = False
    input_1 = 0

    # Keep going until valid input is reached
    while (not input_1_valid):
        try:
            input_1 = int(input(input_string)) # Get integer input

            # Case 1: unbounded
            if (minimum == -1 & maximum == -1):
                input_1_valid = True
            
            # Case 2: max bounded
            elif (minimum == -1): # Error: out of bounds
                if (input_1 > maximum):
                    print(f'\nPlease enter an integer less than or equal to {maximum}.')
                else:
                    input_1_valid = True

            # Case 3: min bounded
            elif (maximum == -1):
                if (input_1 < minimum): # Error: out of bounds
                    print(f'\nPlease enter an integer greater than or equal to {minimum}.')
                else:
                    input_1_valid = True

            # Case 4: max and min bounded
            else: # Error: out of bounds
                if (input_1 < minimum or input_1 > maximum):
                    print(f'\nPlease enter an integer between {minimum} and {maximum}, inclusive.')
                else:
                    input_1_valid = True
        
        except: # Error: Not an integer
            print('\nPlease enter an integer!')
    return input_1

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
            raise Exception("Input object must be Holiday type!")

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

    # displayHolidaysInWeek: display a list of holidays with proper formatting
    #   holiday_list: (list(Holiday)) list of holidays
    #   should_print: (bool, default: False) True to include prints of each; False otherwise
    #   if_weather: False to not show weather; True otherwise (BE CAREFUL! ONLY WORKS FOR CURRENT WEEK!)
    #   return: (list(str)) list of properly formatted holidays
    def displayHolidays(self, holiday_list, should_print=False, if_weather=False):

        format_holidays = []
        weather = []

        # Add in weather upon request
        if (if_weather):
            weather = self.getWeather()

        # Format strings
        for holiday in holiday_list:
            date = str(holiday.date.date())
            if (if_weather):
                format_holidays.append(f'{holiday} ({date}) - {weather[date]}')
            else:
                format_holidays.append(f'{holiday} ({holiday.date.date()})')

        # Give option to print holidays within function 
        if (should_print):
            for string in format_holidays:
                print(string)

        # Return list of formatted holidays
        return format_holidays

    # getWeather: create dictionary of days of week and corresponding weathers; because of limitations of API, can only be used on current week
    def getWeather(self):

        # May run into querying limits
        try:

            # Get what day of the week it is
            curr_dow = datetime.today().weekday()

            # Create weather dictionary and date list
            dates = []
            weather = {}
            j = 0
            add_date = datetime.today() - dt.timedelta(days=curr_dow)
            while (j < 7):
                date = add_date.strftime('%Y-%m-%d')
                dates.append(date)
                weather[date] = 'n/a'
                add_date = add_date + dt.timedelta(days=1)
                j += 1

            # Future weather forcast

            # First determine how many forcast days are needed
            future_n = 6 - curr_dow

            # Query those days to get forcast weather
            query_str_future = {"q":"minneapolis,us","cnt":f'{future_n}',"units":"imperial"}
            response_future = requests.request("GET", weather_api_future, headers=weather_headers, params=query_str_future)
            data_future = json.loads(response_future.text)
            future_weather = data_future['list']

            # Add that weather to list
            for i in range(curr_dow+1, 7):
                current_day = future_weather[i-curr_dow-1]
                weather[dates[i]] = current_day['weather'][0]['main']
            
            # Past weather historical data
            j = 0
            for i in range(curr_dow, -1, -1):

                # Makes sure never to query beyond 5 days in past (no data after that)
                if (j < 5):

                    # Get the change in date and query that date
                    date = datetime.today() - dt.timedelta(j)
                    query_str_past = {"lat":"44.986656","lon":"-93.2650","dt":f'{int(date.timestamp())}'}
                    response_past = requests.request("GET", weather_api_past, headers=weather_headers, params=query_str_past)

                    # Save that dates weather
                    data_past = json.loads(response_past.text)
                    curr_weather = data_past['current']['weather'][0]['main']
                    weather[dates[i]] = curr_weather

                j += 1

            # Return weather
            return weather
        
        except:
            print('Ran out of queries to Weather API!')

    # viewCurrentWeek: view current week of holidays and weather
    #   if_weather: (bool) False to not show weather; True otherwise
    def viewCurrentWeek(self, weather=False):

        # Use the Datetime Module to look up current week and year
        year = datetime.now().year
        week = datetime.now().isocalendar()[1]

        # Use your filterHolidaysByWeek function to get the list of holidays 
        holidays = self.filterHolidaysByWeek(year, week)

        # Use your displayHolidaysInWeek function to display the holidays in the week
        self.displayHolidays(holidays, should_print=True, if_weather=weather)

# main: main function runner
def main():

    # Set up variables
    holidays = HolidayList()

    # Load in variables, both from JSON and API
    holidays.readJSON('data/holidays.json')
    holidays.scrapeHolidays()

    # Print welcome message
    f = open('messages/welcome.txt', 'r')
    welcome = f.read()
    print()
    print(welcome.format(num=str(holidays.numHolidays())))
    print()

    # Create while loop to keep user going
    keep_going = True
    saved = True
    while (keep_going):

        # Display user menu
        f = open('messages/options.txt', 'r')
        options = f.read()
        print(options)
        print()

        # Get user choice
        choice = int_input(minimum=1, maximum=5, input_string="Selection: ")
        print()

        # Add a holiday option
        if (choice == 1):

            # Display page info
            print("Add a Holiday")
            print("=============")

            # Get holiday name
            good_input = False
            name = ""
            while (not good_input):
                name = input("Holiday: ")
                if (name == ""):
                    print("Please enter a name that isn't blank!")
                else:
                    good_input = True
            
            # Get date
            good_input = False
            date = ""
            while (not good_input):
                date = input("Date [YYYY-MM-DD]: ")

                # Immediately reject blank entries
                if (date == ""):
                    print("Please enter a name that isn't blank!")
                
                # Try to convert date to datetime to see if properly formatted
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                    good_input = True
                except:
                    print("Date is not formatted correctly; please use YYYY-MM-DD!")

            # Check to see if holiday already exists
            exists = holidays.findHoliday(name, date)
            if (exists == None):

                # Add holiday if not already there
                holiday = Holiday(name, date)
                holidays.addHoliday(holiday)
                print(f'\n{name} ({date}) is now added!\n')
                saved = False

            # Don't add holiday if already in list
            else:
                print(f'\n{name} ({date}) has already been entered into the system!\n')

            # Return to main menu
            print('Returning to main menu!\n')

        # Remove a holiday option
        if (choice == 2):
            # Display page info
            print("Remove a Holiday")
            print("=============")

            # Get holiday name
            good_input = False
            name = ""
            while (not good_input):
                name = input("Holiday: ")
                if (name == ""):
                    print("Please enter a name that isn't blank!")
                else:
                    good_input = True
            
            # Get date
            good_input = False
            date = ""
            while (not good_input):
                date = input("Date [YYYY-MM-DD]: ")

                # Immediately reject blank entries
                if (date == ""):
                    print("Please enter a name that isn't blank!")
                
                # Try to convert date to datetime to see if properly formatted
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                    good_input = True
                except:
                    print("Date is not formatted correctly; please use YYYY-MM-DD!")

            # Check to see if holiday already exists
            exists = holidays.findHoliday(name, date)
            if (exists != None):

                # Remove holiday if there
                holidays.removeHoliday(name, date)
                print(f'\n{name} ({date}) is now removed!\n')
                saved = False

            # Don't add holiday if already in list
            else:
                print(f'\n{name} ({date}) is not in system, so it cannot be removed!\n')

            # Return to main menu
            print('Returning to main menu!\n')

        # Save holidays option
        if (choice == 3):
            
            # Display page info
            print("Saving Holiday List")
            print("====================")
            print("Are you sure you want to save your changes?")

            # Get response
            good_input = False
            while (not good_input):
                choice = input('[y/n] ')

                # Save data
                if (choice.lower().strip() == 'y'): # Save data

                    # Get file name
                    good_input_2 = False
                    name = ""
                    while (not good_input_2):
                        name = input("Please input a file name, excluding JSON tag: ")
                        if (name == ""):
                            print("Please enter a name that isn't blank!")
                        elif (".json" in name):
                            print("Please do not include '.json' in input!")
                        else:
                            good_input_2 = True
                    
                    # Save file
                    holidays.saveToJSON(f'{name}.json')
                    saved = True
                    
                    # Print success message
                    print()
                    print("Success:")
                    print(f'Your changes have been saved to {name}.json')

                    # Return to main menu
                    print()
                    print('Returning to main menu!\n')
                    good_input = True

                # Don't do any thing
                elif (choice.lower().strip() == 'n'):
                    
                    # Print message
                    print()
                    print("Canceled:")
                    print("Holiday list file save canceled.\n")

                    # Return to main menu
                    print()
                    print('Returning to main menu!\n')
                    good_input = True
                
                # Bad input
                else:
                    print("Please enter 'y' or 'n'!")

        # View holidays option
        if (choice == 4):

            # Display page info
            print("View Holidays")
            print("=================")
            
            # Get year range
            year_min = None
            year_max = None
            for holiday in holidays.inner_holidays:
                if (year_min == None or year_min > holiday.date.year):
                    year_min = holiday.date.year
                if (year_max == None or year_max < holiday.date.year):
                    year_max = holiday.date.year
            
            # Get year and month
            which_year = int_input(minimum=year_min, maximum=year_max, input_string="Which year?: ")
            which_week = int_input(minimum=1, maximum=52,
                input_string=f'Which week (current week: {datetime.today().isocalendar()[1]})? [1-52]: ')

            # If the week is the current week and year is current year, then offer to show weather as well
            weather = False
            if (which_week == datetime.today().isocalendar()[1] and which_year == datetime.today().year):
                
                # Ask if user would like to the weather
                print("Include weather?")

                # Determine if the user wants to see weather
                good_input = False
                while (not good_input):
                    choice = input('[y/n] ')
                    if (choice.lower().strip() == 'y'): # Get weather option
                        weather = True
                        good_input = True
                    elif (choice.lower().strip() == 'n'): # Don't get weather option
                        good_input = True
                    else: # Bad input
                        print("Please enter 'y' or 'n'!")
            
            # Display results
            print()
            print(f'These are the holidays for {which_year} week #{which_week}:')
            holidays.displayHolidays(holidays.filterHolidaysByWeek(which_year, which_week), should_print=True, if_weather=weather)
            print()
        
        # Exit option
        if (choice == 5):

            # Display options
            print("Exit")
            print("=====")
            print("Are you sure you want to exit?")
            if (not saved): # Only display if changes have been made that haven't been saved
                print("Your changes will be lost!")

            # Get response
            good_input = False
            while (not good_input):
                choice = input('[y/n] ')
                if (choice.lower().strip() == 'y'): # Leave system
                    keep_going = False
                    good_input = True
                elif (choice.lower().strip() == 'n'): # Leave menu
                    print()
                    print('Returning to main menu!\n')
                    good_input = True
                else: # Bad input
                    print("Please enter 'y' or 'n'!")
    
    # Sign off message
    print()
    print('Thanks for using Holidays API! Auf Wiedersehen!\n')

# Call main function
if __name__ == "__main__":
    main()