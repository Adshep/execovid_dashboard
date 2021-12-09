'''This module deals with extracting information from the config file.'''
import json
with open('../config.json', encoding='utf-8') as config_file:
    #Converts json file to dictionary format
    settings = json.load(config_file)

def get_API_key():
    '''Fetches the API key from the config.json'''
    api_key = settings['covid_handler']['api_key']
    return api_key

def get_picture():
    '''Fetches the name of the picture from config.json'''
    picture = settings['covid_handler']['picture']
    return picture

def get_location():
    '''Fetches the local location to be used in covid_data_handler.'''
    location = (
        settings['covid_handler']['local_location'],
        settings['covid_handler']['national_location']
    )
    return location
