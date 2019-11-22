import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*85)
    print('( - - - - - - - - - - - - - - - - - W E L C O M E - - - - - - - - - - - - - - - - - )')
    print('-'*85)
    print('      (Let\'s explore some US bikeshare data!)')

    # user input by city
    city = input('\nThe available cities are Chicago, New York City, and Washington DC; which city do you choose?\n').lower()  #lower used to accept values in any format

    # while loop checking correct input
    while(True):
        if(city == 'chicago' or city == 'new york' or city == 'washington'):
            break
        else:
            city = input('\nWrong input, please choose from the city list: \n').lower()

    # user input by month
    month = input('\nThe available months are: January, February, March, April, May, June or all; which month do you choose?\n').lower()

    # while loop checking correct input
    while(True):
        if(month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'all'):
            break
        else:
            month = input('\nWrong input, please choose from the months list: \n').lower()

    # user input by day
    day =  input('\nChoose a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday , Sunday, or all?\n').lower()

    # while loop checking correct input
    while(True):
        if(day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all'):
            break
        else:
            day = input('\nWrong input, please choose from the list: \n').lower()

    print('-'*85)
    # user selection
    print('Your selection is ...\n  city: {},\n  month: {},\n  day: {}'.format(city, month, day).title())
    print('-'*85)

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

    # load date into dateframe
    df = pd.read_csv(CITY_DATA[city])

    # to_datetime convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

  # condition
    if  month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Used to find index of month

        df = df[df['Start Time'].dt.month == month]

    # condition
    if  day != 'all':
        df = df[df['Start Time'].dt.weekday_name == day.title()]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # condition to filter common month from all
    if(month == 'all'):
        common_month = df['Start Time'].dt.month.value_counts().idxmax()
        print('The most common month is {}'.format(common_month))

    # condition to filter common day from all
    if(day == 'all'):
        common_day = df['Start Time'].dt.weekday_name.value_counts().idxmax()
        print('The most common day is ', common_day)

    # the most common start hour
    common_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print('The most popular hour is {}'.format(str(common_hour)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # common start station
    start_station = (df['Start Station']).mode()
    print('The most common start station:\n {}'.format( str(start_station)))

    # common end station
    end_station = (df['End Station']).mode()
    print('\nThe most common end station:\n {} '.format( str(end_station)))

    # frequent combination trip
    combination_trip = df['Start Station'].astype(str) + ") TO (" + df['End Station'].astype(str)
    frequent_trip = combination_trip.value_counts().idxmax()
    print('\nThe most popular trip:\n FROM ({})'.format(str(frequent_trip)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    total_travel = df['Trip Duration'].sum()
    minute, second = divmod(total_travel, 60)
    hour, minute = divmod(minute, 60)

    print('Total travel time:\n ({}) hours\n  ({}) minutes\n  ({}) seconds'.format(hour, minute, second))

    # display mean travel time
    mean_travel = round(df['Trip Duration'].mean())
    minute2, second2 = divmod(total_travel, 60)
    hour2, minute2 = divmod(minute, 60)

    print('\nMean travel time:\n   ({})  hours\n  ({}) minutes\n  ({}) seconds'.format(hour2, minute2, second2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # counts of user types
    subscribers = df['User Type'].str.count('Subscriber').sum()
    customers = df['User Type'].str.count('Customer').sum()
    print(' -- Subscribers = {}\n -- Customers   = {}\n'.format(int(subscribers), int(customers)))

    # counts of gender
    if('Gender' in df):
        male_g = df['Gender'].str.count('Male').sum()
        female_g = df['Gender'].str.count('Female').sum()
        print('\n Number of -( MALE )- users are {}\n Number of -(FEMALE)- users are {}\n'.format(int(male_g), int(female_g)))

    # earliest, most recent, and most common year of birth
    if('Birth Year' in df):
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_birth = (df['Birth Year']).mode()
        print('\n -- Oldest Birth Year is {}\n -- Youngest Birth Year is {}\n -- Popular Birth Year is {}\n'.format(int(earliest_year), int(recent_year), int(common_birth)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
        print("\nWould you like see five rows of data ?? Enter yes or no.")
        set_data = input().lower()

        # while loop prompt if the user wants to display more than 5 lines of data
        i = 5
        while set_data == 'yes':
            print(df[:i])
            print('\nWould you like to see five more rows of data ?? Enter yes or no.')
            set_data = input().lower()
            i += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
