'''This module retrieves and formats Covid data'''
import json
import logging
from uk_covid19 import Cov19API
from config_handler import get_location

def parse_csv_data(csv_filename: str) -> list:
    '''Converts each line of a CSV file into an array.'''
    #Prevents program crashing in the event the file nation_2021-10-28 does not exist.
    try:
        with open(csv_filename, encoding='utf-8') as csv_file:
            data = csv_file.read().splitlines()
        csv_file.close()
        logging.info('Data sucesfully added to array.')
        return data
    except FileNotFoundError:
        logging.error('No CSV file present')

def process_covid_csv_data(covid_csv_data: list) -> tuple:
    '''Returns key COVID stats from the CSV module produced by the COV19 API'''
    try:
        split_hospital_row = covid_csv_data[1].split(',')
        current_hospital_cases = int(split_hospital_row[5])
        count = 1
        total_deaths = ''
        while total_deaths == '':
            count += 1
            split_death_row = covid_csv_data[count].split(',')
            total_deaths = split_death_row[4]
        last7days_cases = 0
        for cases in range(3,10):
            #Iterates over cases in the last 7 days from the array, ignoring invalid data.
            split_cases_row = covid_csv_data[cases].split(',')
            #Index 6 contains the cases in the row.
            last7days_cases += int(split_cases_row[6])
        return last7days_cases, int(current_hospital_cases), int(total_deaths)
    except IndexError:
        return logging.error('CSV in incorrect format, so no data has been extracted.')

def covid_API_request(location: str = 'Exeter', location_type: str = 'ltla') -> json:
    '''Uses the COV19 API to return Covid data in JSON format.
    :param location: location of COVID data.
    :param ltla: location type (national, ltla for local etc.)
    '''
    england_only = [
    'areaType=' + location_type,
    'areaName=' + location
    ]
    structure_of_json = {
    'areaCode': 'areaCode',
    'areaName': 'areaName',
    'areaType': 'areaType',
    'date': 'date',
    'cumDailyNosDeathsByDeathDate': 'cumDeaths28DaysByDeathDate',
    'hospitalCases': 'hospitalCases',
    'newCasesBySpeceminDate': 'newCasesByPublishDate',
    }

    api = Cov19API(filters = england_only, structure = structure_of_json)
    data = api.get_json()
    logging.info('Connection to COV19 API established, parsing data...')
    return data

def process_covid_json_data() -> dict:
    '''Returns live formatted covid statistics to be utilized by the dashboard.'''
    #get_location fetches the location specified in config.json
    local_data = covid_API_request(get_location()[0])['data']
    national_data = covid_API_request(get_location()[1], 'nation')['data']
    #Finds covid stats from previous day (index 1), as current day stats are incomplete.
    local_total_deaths = local_data[1]['cumDailyNosDeathsByDeathDate']
    national_total_deaths = national_data[1]['cumDailyNosDeathsByDeathDate']
    #Uses index 2, as hospitalisations show up on day 2.
    national_hospital_cases = national_data[2]['hospitalCases']
    national_last7days_cases = 0
    local_last7days_cases = 0
    for cases in range(1, 8):
        #For loop calculates cases in last 7 days ignoring first entry
        local_last7days_cases += int(local_data[cases]['newCasesBySpeceminDate'])
        national_last7days_cases += int(national_data[cases]['newCasesBySpeceminDate'])
    parsed_data = [
        {'cases': local_last7days_cases, 'deaths': local_total_deaths},
        {'cases': national_last7days_cases, 'deaths': national_total_deaths,
        'hospitalisations': national_hospital_cases }
    ]
    return parsed_data
