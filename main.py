from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

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
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:

    def __init__(self):
        self._inner_holidays = []
   
    # addHoliday: add holiday to holiday list
    #   holidayObj: Holiday instance of holiday to add
    def addHoliday(self, holiday_obj):
        
        # Make sure the input holiday is a holiday object
        if (type(holiday_obj) == Holiday):

            # Make sure holiday isn't already in list
            try:
                self._inner_holidays.index(holiday_obj)
                print(f'New holiday ("{holiday_obj.name}", "{holiday_obj.date}") already added!\n')
            
            # Go here if not already in list
            except:

                # Add holiday to holiday list
                self._inner_holidays.append(holiday_obj)

                # Print add message
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
    def removeHoliday(self, holiday_name, date_str, date_format='%Y-%m-%d'):

        # Find index of item
        j = -1
        date = datetime.strptime(date_str, date_format)
        for i in range(len(self._inner_holidays)):
            holiday = self._inner_holidays[i]
            if (holiday.name == holiday_name and holiday.date == date):
                j = i
        
        # If never found, return error
        if (j == -1):
            print(f'Holiday ("{holiday_name}", "{date_str}") could not be found, so no holiday has been deleted!')
        
        # Delete object
        else:
            self._inner_holidays.pop(j)
            print(f'Holiday ("{holiday_name}", "{date_str}") has been deleted!')

    #def readJSON(self, f_loc):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    #def saveToJSON(self, f_loc):
        # Write out json file to selected file.
        
    #def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    #def numHolidays(self):
        # Return the total number of holidays in innerHolidays
    
    #def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    #def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

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


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.