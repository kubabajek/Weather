import requests, json

def main():
    api_key = "1cc9ea60b7d041e29b6220436231005"
    city = "Cracow"
    days = 7

    url_base = "http://api.weatherapi.com/v1/forecast.json"
    url = f"{url_base}?key={api_key}&q={city}&days={days}&aqi=no&alerts=no"

    response = requests.get(url)
    data = response.json()
    data = data['forecast']['forecastday']

    temp = 10
    check_temp = lambda day_data : day_data["day"]["mintemp_c"]<temp
    print_day = lambda day_data : print(f'Data: {day_data["date"]}, TempMin: {day_data["day"]["mintemp_c"]}\u00b0C')

    data_filtered = list(filter(check_temp,data))
    list(map(print_day, data_filtered));

if __name__ == "__main__":
    main()