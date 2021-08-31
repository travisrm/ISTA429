"""
Name: Travis Myers
Section Leader: Charlie Stancik
Date: 1/28/2021
ISTA 131
HW3
Collaborated with Charlie Stancik in office hours, Anna Fergusun and Julia Rudolph
at the library.
"""
import pandas as pd
import sqlite3, os
from datetime import timedelta

def A_students(conn, tbl_name="ISTA_131_F17", standing=None, results=10):
    """
    This function takes connection object, table name, class standing string with none
    as default, and a maximum number of results to display with default of 10.
    Functions sets the cursor, and checks if standing is none, or if not and
    executes the respective query. Returns a list by traversing through
    rows according to where the cursor has moved.
    """
    c=conn.cursor()
    #complete for loop for max in list
    if not standing:
        query = "SELECT last || ', ' || first AS name FROM " + tbl_name + " WHERE grade='A'"+" ORDER BY name LIMIT "+str(results)+";"
    else:
        query = "SELECT last || ', ' || first AS name FROM " + tbl_name + " WHERE lower(level) LIKE '"+standing+"' AND grade='A'"+' ORDER BY name LIMIT '+str(results)+';'
    c.execute(query)
    return [row[0] for row in c.fetchall()]

def read_frame():
    """
    This function creates an index of every month, and then turns
    index into the respective rise and set of the sun, then reads 
    the csv file with pandas, keeps data type as string, and uses
    index to create the x-axis labels and index the colums starting at 1
    then returns the panda grid.
    """
    index = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    index = [m + suffix for m in index for suffix in ['_r','_s']]
    data = pd.read_csv('sunrise_sunset.csv', header=None, names=index, dtype=str, index_col=0)
    return data

def get_series(sun_frame):
    """
    This function first creates an index for the months of the year, then
    creates concatenates the periods from the data returned in the 
    last function with _r and _s as sunRise and sunSet respectively.
    for each it then drops periods that have no data.  Then for each 
    rise and set Series it returns the date range through a given period
    of time.  It then returns the modified rise and set series.
    """
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    rise=pd.concat([sun_frame[m + '_r'] for m in months])
    sunset=pd.concat([sun_frame[m + '_s'] for m in months])
    rise = rise.dropna()
    sunset = sunset.dropna()
    sunset.index = rise.index = pd.date_range('010118', '123118')
    return rise, sunset

def longest_day(sunrise, sunset):
    """
    This function takes sunrise and sunset series as parameters
    and returns the longest day of the year by changing all hhmm
    strings into integers and then dividing by 100 and multiplying by 60
    then adding the minutes to that number for both.  The longest day
    is determined by subtracting the sunset time from the sunrise time
    To check for the longest we check for the id with the highest
    number using idxmax and figures out the length of the day for the
    longest length day length hours added to the minutes.  It returns the timestamp of the
    longest day and the hour and minute string representing the length
    of the day in hhmm
    """
    rise_min = sunrise.astype(int) // 100 * 60 + sunrise.astype(int) % 100
    sunset_min = sunset.astype(int) // 100 * 60 + sunset.astype(int) % 100
    len_day = sunset_min - rise_min
    longest = len_day.idxmax()
    longest_hours = str(len_day[longest] // 60) + str(len_day[longest] % 60)
    
    return longest, longest_hours    

def sunrise_dif(sunrise, timestamp):
    """
    This function takes the sunrise and timestamp as parameters
    cunverts the sunrise into an int, and calculates sunrise minutes
    of the times stamp. It then checks the sunrise times 90 days before and
    90 days after then returns that.
    """
    rise_min = sunrise.astype(int) // 100 * 60 + sunrise.astype(int) % 100
    return(rise_min.loc[timestamp - timedelta(90)]-rise_min.loc[timestamp + timedelta(90)])

#def student_report(sql_fname, student_id):