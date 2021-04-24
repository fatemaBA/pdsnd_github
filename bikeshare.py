import time
import pandas as pd
import numpy as np
import calendar as cal

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
days = ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']
response = ['yes', 'no']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington)
    city = input("\nWould you like to see data for Chicago, New York, or  Washington? Please type out the full city name.\n")
    while city.strip().lower() not in CITY_DATA:
        city = input("\nYour choice must be Chicago, New York, or  Washington. Please try again.\n")

    # get user input for month (all, january, february, ... , june)
    month = input("\nWhich month? Please type type Jan, Feb, Mar, Apr, May, Jun, or All.\n")
    while (month.strip().title() != 'All') == (month.strip().title() not in months):
        month = input("\nYour choice must be Jan, Feb, Mar, Apr, May, Jun, or All. Please try again.\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nWhich day? Please type type M, Tu, W, Th, F, Sa, Su, or All.\n")
    while (day.strip().title() != 'All') == (day.strip().title() not in days):
        day = input("\nYour choice must be M, Tu, W, Th, F, Sa, Su or All. Please try again.\n")

    print('-'*40)
    return city.strip().lower(), month.strip().title(), day.strip().title()


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
    #Load Data From .csv File
    df = pd.read_csv(CITY_DATA[city])

    #Convert Start Time to Datetime Type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding in
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # use the index of the days list to get the corresponding int
        day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    month_count = df['month'].value_counts()[common_month]
    print('The Most Common Month is: {}, count: {}\n'.format(cal.month_name[common_month],month_count))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    day_count = df['day_of_week'].value_counts()[common_day]
    print('The Most Commn Day of Week is: {}, count: {}\n'.format(cal.day_name[common_day],day_count))


    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour
    common_hour = df['hour'].mode()[0]
    hour_count = df['hour'].value_counts()[common_hour]
    print('The Most Commn Start Hour is: {}, count: {}\n'.format(common_hour,hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    start_station_count = df['Start Station'].value_counts()[common_start_station]
    print('The Most Common Satrt Station is: {}, count: {}\n'.format(common_start_station, start_station_count))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    end_station_count = df['End Station'].value_counts()[common_end_station]
    print('The Most Common End Station is: {}, count: {}\n'.format(common_end_station, end_station_count))

    # display most frequent combination of start station and end station trip
    #Extract combinations of start to end stations
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' -> ')
    #find most common start to end
    common_start_end = df['Start To End'].mode()[0]
    start_end_count = df['Start To End'].value_counts()[common_start_end]
    print('The Most Common Start To End Station is: {}, count: {}\n'.format(common_start_end, start_end_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #get the sum of trip duration in seconds
    total_duration  = df['Trip Duration'].sum()
    #get total travel as hours minutes seconds format
    min, sec = divmod(total_duration, 60)
    hour, min = divmod(min, 60)
    print('Total Travel Time is: {} Hours {} Minutes and {} Seconds\n'.format(hour,min,sec))

    # display mean travel time
    avg_duration = df['Trip Duration'].mean()
    #get total travel as hours minutes seconds format
    min, sec = divmod(avg_duration, 60)
    hour, min = divmod(min, 60)
    print('Average Travel Time is: {} Hours {} Minutes and {} Seconds\n'.format(hour,min,sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_count = df['User Type'].value_counts()
    print('Total Users for Each Type is:\n{}\n'.format(type_count.to_string()))

    # Display counts of gender
    #check if the df has gender column
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Total Users for Each Gender is:\n{}\n'.format(gender_count.to_string()))

    # Display earliest, most recent, and most common year of birth
    #check if the df has birth year column
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('The Earliest Year of Birth is: {}\n'.format(earliest))
        print('The Most Recent Year of Birth is: {}\n'.format(recent))
        print('The Most Common Year of Birth is: {}\n'.format(common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""

    index = 0
    last_index = df.shape[0]
    #remove unwanted columns
    df = df.drop(['month', 'day_of_week','hour','Start To End'], axis = 1)
    #check if user wants to see raw data
    show_data = input('Whould you like to see raw data? Enter yes or no.\n')
    while show_data.strip().lower() not in response:
        show_data = input('\nYour choice must be yes or no.\n')

    #check if user wants to see more rows of raw data and that more data exists
    while show_data.strip().lower() == 'yes':
        if index+5 >= last_index:
            print('{}\n'.format(df[index:last_index]))
            print('\nYou have Reached to the Last Row. There is No More Raw Data.\n')
            break
        else:
            print('{}\n'.format(df[index:index+5]))
            index = index + 5

        show_data = input('\nWould you like to see more? Enter yes or no.\n')
        while show_data not in response:
            show_data = input('\nYour choice must be yes or no.\n')

    print('-'*40)

def main():
    print('\nHello! Let\'s explore some US bikeshare data!')
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print('\nNo Data Exists For the Chosen City Month and Day')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.strip().lower() not in response:
            restart = input('\nYour choice must be yes or no.\n')

        if restart.strip().lower() != 'yes':
            break


if __name__ == "__main__":
	main()
