# Made with love by Karl
# Contact me on Telegram: @karlpy

import requests
import csv
import lxml.html as lh

import config

from util.UnitConverter import ConvertToSystem
from util.Parser import Parser
from util.Utils import Utils

# configuration
stations_file = open('stations.txt', 'r')
URLS = stations_file.readlines()
# Date format: YYYY-MM-DD
START_DATE = config.START_DATE
END_DATE = config.END_DATE

# set to "metric" or "imperial"
UNIT_SYSTEM = config.UNIT_SYSTEM
# find the first data entry automatically
FIND_FIRST_DATE = config.FIND_FIRST_DATE


def scrap_station(weather_station_url):

    session = requests.Session()
    timeout = 5
    global START_DATE
    global END_DATE
    global UNIT_SYSTEM
    global FIND_FIRST_DATE

    if FIND_FIRST_DATE:
        # find first date
        first_date_with_data = Utils.find_first_data_entry(weather_station_url=weather_station_url, start_date=START_DATE)
        # if first date found
        if(first_date_with_data != -1):
            START_DATE = first_date_with_data
    
    url_gen = Utils.date_url_generator(weather_station_url, START_DATE, END_DATE)
    station_name = weather_station_url.split('/')[-1]
    file_name = f'{station_name}.csv'

    with open(file_name, 'a+', newline='') as csvfile:
        fieldnames = ['Date', 'Time','Temperature_High', 'Temperature_Avg', 'Temperature_Low', 
                         'DewPoint_High', 'DewPoint_Avg', 'DewPoint_Low', 
                         'Humidity_High', 'Humidity_Avg', 'Humidity_Low', 
                         'WindSpeed_High', 'WindSpeed_Avg', 'WindSpeed_Low', 
                         'Pressure_High', 'Pressure_Low', 'Precip_Sum']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the correct headers to the CSV file
        if UNIT_SYSTEM == "metric":
            # 12:04 AM	24.4 C	18.3 C	69 %	SW	0.0 km/h	0.0 km/h	1,013.88 hPa	0.00 mm	0.00 mm	0	0 w/m²
            writer.writerow({'Date': 'Date', 'Time': 'Time', 'Temperature_High': 'Temperature_High_C', 'Temperature_Avg':'Temperature_Avg_C', 'Temperature_Low':'Temperature_Low_C', 
                         'DewPoint_High':'DewPoint_High_C', 'DewPoint_Avg':'DewPoint_Avg_C', 'DewPoint_Low': 'DewPoint_Low_C', 
                         'Humidity_High':'Humidity_High', 'Humidity_Avg':'Humidity_Avg', 'Humidity_Low':'Humidity_Low', 
                         'WindSpeed_High':'WindSpeed_High_kmh', 'WindSpeed_Avg_kmh':'WindSpeed_Avg_kmh', 'WindSpeed_Low':'WindSpeed_Low_kmh', 
                         'Pressure_High':'Pressure_High_hPa', 'Pressure_Low':'Pressure_Low_hPa', 'Precip_Sum':'Precip_Sum_mm'})
        elif UNIT_SYSTEM == "imperial":
            # 12:04 AM	75.9 F	65.0 F	69 %	SW	0.0 mph	0.0 mph	29.94 in	0.00 in	0.00 in	0	0 w/m²
            writer.writerow({'Date': 'Date', 'Time': 'Time', 'Temperature_High': 'Temperature_High_F', 'Temperature_Avg':'Temperature_Avg_F', 'Temperature_Low':'Temperature_Low_F', 
                         'DewPoint_High':'DewPoint_High_F', 'DewPoint_Avg':'DewPoint_Avg_F', 'DewPoint_Low': 'DewPoint_Low_F', 
                         'Humidity_High':'Humidity_High', 'Humidity_Avg':'Humidity_Avg', 'Humidity_Low':'Humidity_Low', 
                         'WindSpeed_High':'WindSpeed_High_mph', 'WindSpeed_Avg':'WindSpeed_Avg_mph', 'WindSpeed_Low':'WindSpeed_Low_mph', 
                         'Pressure_High':'Pressure_High_in', 'Pressure_Low':'Pressure_Low_in', 'Precip_Sum':'Precip_Sum_in'})
        else:
            raise Exception("please set 'unit_system' to either \"metric\" or \"imperial\"! ")

        for date_string, url in url_gen:
            try:
                print(f'Scraping data from {url}')
                history_table = False
                while not history_table:
                    html_string = session.get(url, timeout=timeout)
                    doc = lh.fromstring(html_string.content)
                    history_table = doc.xpath('//*[@id="main-page-content"]/div/div/div/lib-history/div[2]/lib-history-table/div/div/div/table/tbody')
                    if not history_table:
                        print("refreshing session")
                        session = requests.Session()

                # parse html table rows
                data_rows = Parser.parse_html_table(date_string, history_table)

                # convert to metric system
                converter = ConvertToSystem(UNIT_SYSTEM)
                data_to_write = converter.clean_and_convert(data_rows)
                    
                print(f'Saving {len(data_to_write)} rows')
                writer.writerows(data_to_write)
            except Exception as e:
                print(e)



for url in URLS:
    url = url.strip()
    print(url)
    scrap_station(url)