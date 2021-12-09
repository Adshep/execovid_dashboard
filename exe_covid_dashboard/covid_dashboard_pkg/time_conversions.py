'''This module deals with the time conversions required for my '''
import time
import logging

def hhmm_to_seconds( hhmm: str ) -> int:
    '''Converts time in the format hhmm to seconds'''
    seperated_time = hhmm.split(':')
    if len(seperated_time) != 2:
        return logging.error('Calculation failed as time is not in hhmm format')
    else:
        try:
            return (int(seperated_time[0]) * 60 * 60) + (int(seperated_time[1]) * 60)
        except ValueError:
            return logging.error('Calculation failed as the value inputted contains letters.')

def current_time() -> str:
    '''Returns the current time in format HH:MM'''
    unformatted_time = time.localtime()
    time_now = time.strftime('%H:%M', unformatted_time)
    return time_now




