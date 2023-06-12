import requests
import json
import argparse
import csv
import os

def int_type(arg_value):
    try:
        return int(arg_value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{arg_value} is not a valid integer")


def is_exist(filename):
    if os.path.exists(filename+'.csv'):
        raise argparse.ArgumentTypeError(f"File {filename}.csv already exists")
    return filename
        
        
parser = argparse.ArgumentParser()
parser.add_argument('-t', action='store', dest='temp', default=10, type=int_type, help='int temp value to data filter (def. 10)')
parser.add_argument('-f', action='store', dest='filename', default='result',type=is_exist, help='csv file name without extension')
args = parser.parse_args()


def next_week_weather(highest_min_temp):
    """Check in which days of next week in Cracow the minimal temperature is lees than passed in int argument

    Args:
        highest_min_temp (int): Minmal temperature above the days will be skipped

    Returns:
        list: List of lists contains date and minimal temperature
    """
    
    api_key = "1cc9ea60b7d041e29b6220436231005"
    city = "Cracow"
    days = 7

    url_base = "http://api.weatherapi.com/v1/forecast.json"
    url = f"{url_base}?key={api_key}&q={city}&days={days}&aqi=no&alerts=no"

    response = requests.get(url)
    data = response.json()
    data = data['forecast']['forecastday']

    check_temp = lambda day_data : day_data["day"]["mintemp_c"] < highest_min_temp
    tidy_data = lambda day_data : [day_data["date"],day_data["day"]["mintemp_c"]]
    
    data_filtered = list(filter(check_temp,data))
    data_tidied = list(map(tidy_data, data_filtered));
    
    with open(args.filename+'.csv', mode='w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['data', 'temp'])
        writer.writerows(data_tidied)
    
    return data_tidied
    
    
def main():
    highest_min_temp = args.temp
    days_temps = next_week_weather(highest_min_temp)
    for days in days_temps:
        print(f'Data: {days[0]}, TempMin: {days[1]}\u00b0C')
    
    
if __name__ == "__main__":
    main()