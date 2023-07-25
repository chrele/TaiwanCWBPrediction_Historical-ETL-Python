import json
import numpy as np
import pandas
import requests
import bs4
import lxml.etree as xml
import urllib
import zipfile
from datetime import datetime
import os
import time

pandas.options.mode.chained_assignment = None

URL = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/'
TOKEN = '' #insert your API key

if not os.path.exists('outputs/'):
  os.mkdir('outputs/')

if not os.path.exists('outputs/Taipei'):
  os.mkdir('outputs/Taipei')
  os.mkdir('outputs/Taipei/2days/')
  os.mkdir('outputs/Taipei/7days/')

if not os.path.exists('outputs/Miaoli'):
  os.mkdir('outputs/Miaoli')
  os.mkdir('outputs/Miaoli/2days/')
  os.mkdir('outputs/Miaoli/7days/')

if not os.path.exists('outputs/Kaohsiung'):
  os.mkdir('outputs/Kaohsiung')
  os.mkdir('outputs/Kaohsiung/2days/')
  os.mkdir('outputs/Kaohsiung/7days/')

def insertRows(df, at, val):
  df1 = df[0:at]
  df2 = df[at:]
  df1.loc[at] = val
  df_res = pandas.concat([df1, df2], ignore_index=True)
  df_res.reset_index()
  return df_res

getValue = ['CI', 'WS', 'MinCI', 'MaxCI']
dataSource = ['F-D0047-061','F-D0047-063','F-D0047-065','F-D0047-067','F-D0047-013','F-D0047-015']
cities = ['Taipei','Taipei','Kaohsiung','Kaohsiung','Miaoli','Miaoli']
span = ['2days', '7days', '2days', '7days', '2days', '7days']
verbose = False

if verbose:
  print('Running Service ...')
for x in range(len(dataSource)):
  #Extraction
  if verbose:
    print('Attempting connection to' + dataSource[x])
  API_Response = requests.get(URL + dataSource[x] + '?Authorization=' + TOKEN + '&format=' + "JSON")
  if API_Response.json()['success'] == 'true':
    if verbose:
      print('Connection Successful!')
    data = json.loads(API_Response.text)
    #Transform
    dfs = []
    if verbose:
      print('Retrieving and Transforming Data')
    for i in data['records']['locations'][0]['location']:
      df_time = pandas.DataFrame.from_dict(data['records']['locations'][0]['location'][0]['weatherElement'][1]['time'])
      df_time = df_time.rename(columns={'startTime': 'time'})
      df_time = df_time.drop(['endTime','elementValue'], axis = 1)
      for j in range(len(i['weatherElement'])):
        valueName = i['weatherElement'][j]['elementName']
        if valueName in ['PoP12h', 'PoP6h']:
          continue
        
        df_other3h = pandas.DataFrame.from_dict(i['weatherElement'][j]['time'])
        df_other3h = df_other3h.explode('elementValue')
        
        try:
          df_other3h = pandas.concat([df_other3h.drop(['startTime','endTime','elementValue'], axis=1), df_other3h['elementValue'].apply(pandas.Series)], axis=1)
        except:
          df_other3h = pandas.concat([df_other3h.drop(['dataTime','elementValue'], axis=1), df_other3h['elementValue'].apply(pandas.Series)], axis=1)
        
        df_other3h = df_other3h.rename(columns={'value': valueName})
        df_other3h = df_other3h.drop(['measures'], axis = 1)

        if valueName == 'Wx':
          df_other3h = df_other3h.iloc[1::2]
        elif valueName in getValue:
          df_other3h = df_other3h.iloc[::2]
        elif valueName == 'UVI':
          df_other3h = df_other3h.iloc[::2]
          df_other3h.reset_index()
          for k in range(1, len(df_other3h)*2, 2):
            df_other3h = insertRows(df_other3h, k, 0)
                    
        df_other3h.reset_index()
        df_time = pandas.concat([df_time, df_other3h], axis=1)

      df_time['District'] = i['locationName']
      if verbose:
        print('Data Transformation is Done.')
      dfs.append(df_time)
    
    #Load
    if verbose:
      print('Loading Data to CSV')
    for df in dfs:
      if cities[x] == 'Taipei':
        if span[x] == '2days':
          df.to_csv('outputs/Taipei/2days/result_' + cities[x] + df['District'][0] + span[x] + '.csv')
        else:
          df.to_csv('outputs/Taipei/7days/result_' + cities[x] + df['District'][0] + span[x] + '.csv')
      elif cities[x] == 'Kaohsiung':
        if span[x] == '2days':
          df.to_csv('outputs/Kaohsiung/2days/result_' + cities[x] + df['District'][0] + span[x] + '.csv')
        else:
          df.to_csv('outputs/Kaohsiung/7days/result_' + cities[x] + df['District'][0] + span[x] + '.csv')
      elif cities[x] == 'Miaoli':
        if span[x] == '2days':
          df.to_csv('outputs/Miaoli/2days/result_' + cities[x] + df['District'][0] + span[x] + '.csv')
        else:
          df.to_csv('outputs/Miaoli/7days/result_' + cities[x] + df['District'][0] + span[x] + '.csv')

    if verbose:
      print('Loading Data is Finished')

file = open('data.json', 'a')
file.write(json.dumps(API_Response.json(), indent=2))
file.close()