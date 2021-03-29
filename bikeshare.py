import time
import pandas as pandas
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    city_list = ['chicago','new york city','washington']
    while city not in city_list:
        city = str(input("Enter a city to filter by from chicago, new york city, washington: ")).lower()


    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in month_list:
        month = str(input("Enter the month you want to filter by from all, january, february, ... , june: ")).lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in day_list:
        day = str(input("Enter the day you want to filter by from all, monday, tuesday, ... sunday: ")).lower()

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
        # load data file into a dataframe
    df = pandas.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pandas.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pandas.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].value_counts().idxmax()

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].value_counts().idxmax()

    # TO DO: display the most common start hour
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    most_common_hour = df['hour'].value_counts().idxmax()

    print("Most common month: ",str(most_common_month))
    print("Most common day: ",str(most_common_day))
    print("Most common hour: ",str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("Most common start station: ", str(most_common_start_station))

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("Most common end station: ", str(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    most_frequent_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most frequent combination of start and end station: ", str(most_frequent_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean = df['Trip Duration'].mean()

    print("Total travel time: ",total)
    print("Mean travel time: ",mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types: ", user_types)


    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].dropna(axis = 0)
        gender = gender.value_counts()
        print("Counts of gender: ", gender)
    except KeyError:
        print("No gender information for city!")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        birth_year = df['Birth Year'].dropna(axis = 0)
        earliest_birth_year = birth_year.min()
        most_recent_birth_year = birth_year.max()
        most_common_birth_year = birth_year.value_counts().idxmax()

        print("Earliest birth year: ",earliest_birth_year)
        print("Most recent birth year: ",most_recent_birth_year)
        print("Most common birth year: ",most_common_birth_year)
    except KeyError:
        print("No birth year information for city!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    sort_by_list = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type']
    sort_by_prompt = str(input('Sort by the data column you want displayed from, Start Time, End Time, Trip Duration, Start Station, End Station, and User Type: '))
    if sort_by_prompt in sort_by_list:
        df = df.sort_values(by=[sort_by_prompt])
    user_input = str(input('Would you like to display 5 lines of raw data? Answer with yes or no: ')).lower()
    row_num = 0
    while user_input == 'yes' and row_num+5 < df.shape[0]:
        print(df.iloc[row_num:row_num+5])
        row_num += 5
        user_input = str(input('Would you like to display 5 additional lines of raw data? Answer with yes or no: ')).lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
