#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:26:46 2021

@author: michaeljehl
"""
import pandas as pd

def fix_date(df):
    
    '''
    This function goes through the dates in the weather dataframe and if there is more than one record for each
    hour, we pick the record closest to the hour and drop the rows with the remaining records for that hour.
    This is so we can align this dataframe with the one containing electricity data.'''
    new_dates = []
    df = df.reset_index()
    df['DATE'] = pd.to_datetime(df['DATE'])
    # we append the first value to fix indexing
    new_dates.append(df['DATE'][0].replace(minute=00))
    hour_dict = {}
    keys_drop = []
    for j,date in enumerate(df['DATE']):
        current_hour = date.hour
        # skip the first value
        if j == 0: 
            continue
        # once we reach the end, just append the last value with minutes replaced to the hour
        if j == len(df['DATE'])-1:
            new_dates.append(date.replace(minute=00))
            continue
        # if the current hour we're on has another entry in the same hour (the one after, since they are ordered 
        # chronologically), add this date to a dictionary
        if current_hour == df['DATE'][j+1].hour:
            hour_dict[date] = j
        # once there are no more entries for the same hour
        # we pick the entry closest to the hours and record the index of the rows to drop
        elif len(hour_dict) >= 1:
            hour_dict[date] = j
            min_date = min(hour_dict.keys())
            new_dates.append(min_date.replace(minute=00))
            del hour_dict[min_date]
            keys_del = hour_dict.values()
            keys_drop.extend(keys_del)
            hour_dict = {}
        # for the base case, when there is only one entry per hour
        else:
            new_dates.append(date.replace(minute=00))
    # drop rows designated before (multiple values in a single hour)
    # and relabel the date column and set it as the index
    df_return = df.drop(keys_drop)
    #df_return['DATE'] = new_dates
    #df_return = df_return.set_index('DATE')
    return df_return, new_dates

def EIA_API_Call(req, value_name):
    '''
    Makes request to EIA API and unpacks JSON file of hourly electricity demand into a pandas dataframe
    
    Inputs: request URL, specific set of data to extract
    Outputs: dataframe of hourly electricity demand
    '''
    
    data = req['series'][0]['data']
    dates = []
    values = []
    for date, value in data:
        if value is None:
            continue
        dates.append(date)
        values.append(float(value))
    df = pd.DataFrame({'DATE': dates, value_name: values})
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df.set_index('DATE')
    df = df.sort_index()
    return df

def PrecipFix(amount):
    """
    Convert precipitation amount to int. Considers edge cases where "T" == 0.00 and handles amounts ending in 's'
    
    Input: precipitation amount in str
    Output: precipitation amount in float
    """

    amount = str(amount)  # some amounts are floats while most are strings
    
    if amount[-2:] == 'Vs':
        amount = float(amount[:-2])
    elif amount[-1] == 's' or amount[-1] == 'V':
        amount = float(amount[:-1])
    elif amount == 'T':
        amount = 0.00
    else:
        amount = float(amount)
    
    return amount


def WindDirection(direction):
    """
    Transforms compass direction into category based on intervals.
        e.g. True south = 180; new south encompasses 135-285
    
    Inputs: wind compass direction (str)
    Outputs: direction category (str)
    """
    
    if direction == 'VRB':
        newdir = 'Variable'
    else:
        direction = int(direction)
        if direction == 0:
            newdir = 'Calm'
        elif (direction >= 1 and direction < 45) or (direction > 315 and direction <= 360):
            newdir = 'North'
        elif direction >= 45 and direction < 135:
            newdir = 'East'
        elif direction >= 135 and direction < 225:
            newdir = 'South'
        else:
            newdir = 'West'
    return newdir


def degree_days(df):
	'''
	This function adds hourly heating and cooling degree days to the weather DataFrame.'''
	df['HourlyCoolingDegrees'] = df['Temperature'].apply(lambda x: x - 65. if x >= 65. else 0.)
	df['HourlyHeatingDegrees'] = df['Temperature'].apply(lambda x: 65. - x if x <= 65. else 0.)

	return df