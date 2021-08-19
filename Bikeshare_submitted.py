import time
import pandas as pd
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter one city name out these 3 cities - chicago , washington, new york city: ")
        if(city.lower() == 'chicago' or city.lower() == 'washington' or city.lower() == 'new york city'):
            print("Input Accepted")
            break
        else:
            print("Invalid input, please enter a valid city")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month name between january to june or enter enter word \'all\' : ")
        if(month.lower() == 'january' or month.lower() == 'february' or month.lower() == 'march' or month.lower() == 'april' or month.lower() == 'may' or month.lower() == 'june'):
            print("Input Accepted and applying filters with input month as "+str(month.title()))
            break
        elif(month.lower() == 'all'):
            print("Input Accepted and No month filters applied")
            break
        else:
            print("Invalid input, please enter a valid month as (January,February,March,April,May,June)")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the day of the week('Monday'....'Sunday') else enter enter word \'all\' : ")
        if(day.lower() == 'monday' or day.lower() == 'tuesday' or day.lower() == 'wednesday' or day.lower() == 'thursday' or day.lower() == 'friday' or day.lower() == 'saturday' or day.lower() == 'sunday'):
            print("Input Accepted and applying filters with input day as "+str(day.title()))
            break
        elif(day.lower() == 'all'):
            print("Input Accepted and No day filters applied")
            break
        else:
            print("Invalid input, please enter a valid day as (Monday,tuesday,wednesday....)")
    print("The inputs are\n1.City name :{}\n2.Month_name or all months :{}\n3.Weekday_name or all week days :{}".format(city,month,day))

    print('*'*120)
    return city,month,day


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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.strftime("%A")
    if month!='all':
        print("Applying filters by month")
        #print(df.head(5))
        months = ['january','february','march','april','may','june']
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day!='all':
        print("Applying filters by day")
#         print(df.head(5))
        df = df[df['day'] == day.title()]
    print('*'*120)
    print("Successfully loaded the data for the specific city with appropriate filters")
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    frequent_month = df['month'].mode()[0]

    # display the most common day of week
    df['week'] = df['Start Time'].dt.week
    frequent_week = df['day'].mode()[0]
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    frequent_hour = df['hour'].mode()[0]

    sample_months = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June'}

    print("Frequent hour in 24 hour format is :{}".format(frequent_hour))
    print("Frequent month is :{}".format(sample_months[frequent_month]))
    print("Frequent day is : ".format(frequent_week))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*120)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    Popular_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    Frequent_combination = df.groupby(['Start Station','End Station']).size().idxmax()

    print("The most popular start station is :{}".format(Popular_start_station))
    print("The most popular end station is :{}".format(Popular_end_station))
    print("The most frequent combinations of start and end stations are :{}".format(Frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*120)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    Total_mean_travel_time = df['Trip Duration'].mean()

    print("The Total travel time is :{}".format(Total_travel_time))
    print("The Mean travel time is :{}".format(Total_mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*120)


def user_stats(df,city_name):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    User_types_count = df['User Type'].value_counts()

    # Display counts of Gender
    try:
        Gender_count = df['Gender'].value_counts()
    except KeyError:
        print("There is no Gender Data in the specified city of {}".format(city_name.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        Earliest_birth_year = df['Birth Year'].min()
        Recent_birth_year = df['Birth Year'].max()
        Common_Birth_year = df['Birth Year'].mode()[0]
        print("The Oldest person's to be a user is born in the year {}".format(str(Earliest_birth_year).split('.')[0]))
        print("The youngest person's to be a user is born in the year {}".format(str(Recent_birth_year).split('.')[0]))
        print("We have more number of users who are born in the year of {}".format(str(Common_Birth_year).split('.')[0]))
    except KeyError:
        print("There is no Birth Year Data in the specified city of {}".format(city_name.title()))




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*120)

def raw_data_display(df,last_mark):
    """
    Displays the raw data of the specific inputted city to visualize and understand the data better
    """
    print('*'*50+"Displaying the Raw Data input"+'*'*50)

    if last_mark!=0:
        last_place = input("Do you want to continue from the last place you left off or from the start? , Say 'last' or 'start'")
        if(last_place.lower() == 'start'):
            last_mark = 0

    while True:
        for i in range(last_mark,len(df.index)):
            print("-"*50)
            print(df.iloc[last_mark:last_mark+5].to_string())
            print("-"*50)
            last_mark += 5


            output = input("Do you want to keep continuing, enter 'yes' or 'no'")
            if(output.lower() == "yes"):
                continue
            else:
                break
        break

    return last_mark


def main():
    """
    Main function that gets input from the user and responds with appropriate statistical data
    """
    while True:
        last_mark = 0
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print("\nThe Following Details can be viewed\n1.Time statistics on the most frequent rides\n2.Station statistics on the popular stations and trips\n3.Trip statistics\n4.User Statistics\n")
        while True:
            input_var = int(input("Enter the number for which the details you want to be displayed : "))
            if(input_var == 1):
                time_stats(df)
                break
            elif(input_var == 2):
                station_stats(df)
                break
            elif(input_var == 3):
                trip_duration_stats(df)
                break
            elif(input_var == 4):
                user_stats(df,city)
                break
            else:
                print("Enter a valid input")
#         time_stats(df)
#         station_stats(df)
#         trip_duration_stats(df)
#         user_stats(df,city)

        raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
        if(raw_data.lower() == "yes" or raw_data.lower() == "no"):
            if(raw_data.lower() == 'yes'):
                if city.lower() == 'washington':
                    print("Warning - Washington city has not sufficient user data to display")
                last_left_mark = raw_data_display(df,last_mark)
            else:
                print("Sure , You opted to not view the Raw data")
        else:
            print("Enter a valid input , say 'yes' or 'no'")

#         print("The last left mark is : ",last_left_mark)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
