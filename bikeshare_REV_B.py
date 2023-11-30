import time
import pandas as pd
import numpy as np
# Data pulled into the program.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_VAL = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_data = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    # Loops are instituted for invalid inputs and casing is adjusted from inputs to ensure any variation works.
    city=''
    while city not in CITY_DATA.keys():
        print('\nPlease choose a city: washington, new york, or chicago')
        city=input().lower()
        if city not in CITY_DATA.keys():
            print('\nTry again. Be sure the casing is identical to the list provided')

    # Get user input for month (all, january, february, ... , june).
    # Added .lower to ensure casing is not a limiting factor.
    month =''
    while month not in MONTH_VAL:
        print('\nOk, now pick a month of the year to filter by from january to june. you may also pick all if you would like to view them all.')
        month=input().lower()
        if month not in MONTH_VAL:
            print('\nTry again')

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    # Added .lower to ensure casing is not a limiting factor.
    day=' '
    while day not in day_data:
        print('\nEnter a day of the week. If you would like to view all days, please pick all.')
        day=input().lower()
        if day not in day_data:
            print('\ntry again. Be sure to pick a day of the week, or pick all of you want to see everything')


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
   # Load city.
    print('loading your selected data... \n')
    df = pd.read_csv(CITY_DATA[city])
    # Convert from Start Time to datetime.
    df['Start'] = pd.to_datetime(df['Start Time'])
    #Extract dates and convert
    df['month'] = df['Start'].dt.month
    df['day'] = df['Start'].dt.weekday_name
    df['hour'] = df['Start'].dt.hour
    # Filter by month, if not all is selected.
    if month != 'all':
        # Use the index of the months list to get the corresponding integer.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Filter by month.
        df = df[df['month'] == month]
    # Filter by day of week if not all is selected.
    if day != 'all':
        # Filter by day of week.
        df = df[df['day'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the median month.
    # This section gathers the median (middle) month traveled numerically and prints. A key is provided to correlate numbers to months.
    # Revised from mode to median.
    median_month = df['month'].median()[0]
    print('\nThe median month is:', median_month,'\n 1 is jan, 2 is feb,...,6 is june')
    # Display the median day of week.
    # This section gathers the median (middle) day traveled and prints.
    median_week = df['day'].median()[0]
    print('\nThe median day is:', median_week)
    # Display the most common start hour.
    # This section gathers the mode (most common) hour traveled and prints.
    common_hour=df['hour'].mode()[0]
    print('\nThe most Common Hour of Travel is: ', common_hour,':00')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    # This section gathers the mode (most common) starting station and prints.
    strt_station=df['Start Station'].mode()[0]
    print('\nThe most common start station is', strt_station)

    # Display most commonly used end station.
    # This section gathers the mode (most common) ending station and prints.
    end_station=df['End Station'].mode()[0]
    print('\nThe most common end station is',end_station)
    # Display most frequent combination of start station and end station trip.
    # This section gathers the mode (most common) trip and prints.
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    Trip=df['trip'].mode()[0]
    print('\nThe most common combination is ',Trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_seconds = df['Trip Duration'].sum()
    average_seconds = total_seconds/len(df)
    # Display total travel time.
    # Updated to remove hours display.
    # This section breaks down total travel time in two intervals. First is hours (roughly) and then it is broken out in minutes and seconds for additional detail.
    print('\nThe overall travel time is {} minutes and {} seconds'.format(int(total_seconds/60), int(total_seconds%60)))
    # Display mean travel time.
    # This section breaks down total travel time in two intervals. First is hours (roughly) and then it is broken out in minutes and seconds       for additional detail.
    print('\nThe average travel time is {} minutes and {} seconds'.format(int(average_seconds/60), int(average_seconds%60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    types=df['User Type'].value_counts()
    print('\nUser types are broken out as follows\n',types)

    # Display counts of gender.
    # A try/except is utilized to print gender breakdowns, where applicable. Some instances do not have data available, which is where the         except portion ensures the program completes.
    try:
        gender=df['Gender'].value_counts()
        print('\nUser genders are broken out as follows\n',gender)
    except:
        print('\nUh oh, an error was encountered...it appears there is no gender data available')
        
    # Display earliest, most recent, and most common year of birth.
    # A try/except is utilized to print birth year breakdowns, where applicable. Some instances do not have data available, which is where         the except portion ensures the program completes.
    try:
        newest=int(df['Birth Year'].min())
        oldest=int(df['Birth Year'].max())
        popular=int(df['Birth Year'].mode()[0])
        print('\nThe earilest birth year is',newest, '\nThe latest birth year is',oldest,'\nThe most popular birth year is',popular)
    except:
        print('\nUh oh, an error was encountered...it appears there is no birth year data available')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Viewing raw data.
# Updated to display 10 lines at a time rather than 5.
    view_data='yes'
    view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no?')
    start_loc = 0
    while view_data != 'no':
        print(df.iloc[start_loc:start_loc+10])
        start_loc += 10
        view_data = input('Do you wish to see the next 5 rows?: ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
