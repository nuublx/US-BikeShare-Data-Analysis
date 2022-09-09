import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA=['January', 'February', 'March', 'April', 'May', 'June']
DAY_DATA=['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city=input("Would you like to see data for which city chicago, new york city or washington?\n")
        if city in CITY_DATA:
            print()
            break
        else:
            print("Invalid Choice!!!")

    while True:
        choice=input("Would you like to filter data by month, day or both , type 'none' to apply no filters:\n")
        if choice in ['month','day','both','none']:
            print()
            break
        else:
            print("Invalid Choice!!!")

    # get user input for month (all, january, february, ... , june)
    month='All'
    if choice =='month' or choice =='both':
        while True:
            month=input("which month? January, February, March, April, May, June:\n")
            if month in MONTH_DATA:
                print()
                break
            else:
                print("Invalid Choice!!!")



    # get user input for day of week (all, monday, tuesday, ... sunday)
    day='All'

    if choice =='day' or choice =='both':
        while True:
            day=input("which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday:\n")
            if day in DAY_DATA:
                print()
                break
            else:
                print("Invalid Choice!!!")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])

    df['Start Time']=pd.to_datetime(df['Start Time'])

    df['End Time']=pd.to_datetime(df['End Time'])

    df['Start Hour']=df['Start Time'].dt.hour #for later use in time_stats function

    df['month']=df['Start Time'].dt.month

    df['day_of_week']=df['Start Time'].dt.day_name()

    if month !='All':
        month=MONTH_DATA.index(month)+1
        df=df[ df['month']==month ]

    if day !='All':
        df=df[ df['day_of_week']==day ]

    return df


def time_stats(df,m,d):
    """
    Displays statistics on the most frequent times of travel,
    doesn't show common month or day or both if any filters are applied on them
    """
    if len(df.index):
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()
    # display the most common month
        if m=="All":
            month=df['month'].mode()[0]
            print(f'The most common month is: {month}\n')

    # display the most common day of week
        if d=="All":
            day=df['day_of_week'].mode()[0]
            print(f'The most common day of week is: {day}\n')

    # display the most common start hour

        hour=df['Start Hour'].mode()[0]
        print(f'The most common start hour is: {hour}\n')

        print("\nThis took %s seconds.\n" % (time.time() - start_time))
    else:
        print("No Data To Print\n")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    if len(df.index):
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

    # display most commonly used start station
        start_station=df['Start Station'].mode()[0]
        print(f'The most commonly used start station is: {start_station}\n')

    # display most commonly used end station
        end_station=df['End Station'].mode()[0]
        print(f'The most commonly used end station is: {end_station}\n')

    # display most frequent combination of start station and end station trip
        most_common_combination=df[['Start Station','End Station']].value_counts().sort_values(ascending=False).reset_index()
    
        combination_start_station=most_common_combination.iloc[0]['Start Station']
        combination_end_station=most_common_combination.iloc[0]['End Station']

        print(f'The most frequent combination of start station and end station is "{combination_start_station}" to "{combination_end_station}"\n')

        print("\nThis took %s seconds.\n" % (time.time() - start_time))
    else:
        print("No Data To Print\n")
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if len(df.index):
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

    # display total travel time
        total_travel_time=df['Trip Duration'].sum()
        print(f'Total Travel Time is: {total_travel_time} seconds\n')

    # display mean travel time
        average_travel_time=df['Trip Duration'].mean()
        print(f'Total Travel Time is: {average_travel_time} seconds\n')

        print("\nThis took %s seconds.\n" % (time.time() - start_time))
    else:
        print("No Data To Print\n")
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    if len(df.index):
        print('\nCalculating User Stats...\n')
        start_time = time.time()

    # Display counts of user types
        try:
            Users=df['User Type'].value_counts()
            print(f'The count of users for each type:\n{Users}\n')
    # Display counts of gender
        
            genders=df['Gender'].value_counts()
            print(f'The count of users for each gender:\n{genders}\n')
    # Display earliest, most recent, and most common year of birth

            earliest=df['Birth Year'].min()
            most_recent=df['Birth Year'].max()
            most_common=df['Birth Year'].mode()[0]
            print(f'Year of Birth:\nEarliest: {earliest}\nMost Recent: {most_recent}\nMost Common: {most_common}\n')

            print("\nThis took %s seconds." % (time.time() - start_time))
        except:
            print("No Data to print\n")
    else:
        print("No Data To Print\n")
    print('-'*40)

def print_trip_data(df):
    """
    Prints raw trip data from the dataframe after its filtered according to the user choices
    """
    while True:
        answer=input("Would you like to see raw trip data?\n").lower()
        if answer=='yes' or answer=='no':
            break
        else:
            print("Invalid Choice!!!\n")
    if answer=="yes":
        i=0
        j=i+5
        while len(df.index)>=j and answer=="yes":
            print(df.iloc[i:j])
            i+=5
            j=i+5
            answer=input("Show more raw data?\n").lower()

        if i<len(df.index)<j and answer=='yes':
            print(df.iloc[i:])
            print("\nNo more raw trip data\n")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_trip_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
