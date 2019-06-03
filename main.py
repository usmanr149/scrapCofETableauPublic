from selenium import webdriver
import re, os
import pandas as pd
import numpy as np

from selenium.webdriver.chrome.options import Options

import time

import datetime
import pygsheets

url = 'https://public.tableau.com/profile/city.of.edmonton#!/'

options = Options()
options.headless = True

current_dirs_parent = os.getcwd()


driver = webdriver.Chrome(current_dirs_parent + '/chromedriver', options=options)

driver.get(url)

time.sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(5)

titles = driver.find_elements_by_class_name('workbook-title')

viz_names = []

for i in titles:
    viz_names.append(i.text)

views = driver.find_elements_by_class_name('workbook-view-count')

viz_views = []

for v in views:
    try:
        viz_views.append(int(v.text.split(' ')[0]))
    except:
        viz_views.append('')

ex_dic = {
    'Viz Title': viz_names,
    'Views': viz_views
}

df = pd.DataFrame.from_records(ex_dic, columns=['Viz Title', 'Views'])

df['Date'] = datetime.datetime.today().strftime('%Y-%m-%d')
df['Viz Title'].replace('', np.nan, inplace=True)

df.dropna(subset=['Viz Title'], inplace=True)

gc = pygsheets.authorize('protect/credentials.json')

sh = gc.open_by_key('1cInMp8VOFmWuVhePuVxwVC60MH6nrDkkBv0S6XUiLkU')

#select the first sheet
wks = sh[0]

for index,row in df.iterrows():
    wks.append_table(values=[row['Viz Title'], row['Views'], str(row['Date'])])

wks_1 = sh[1]

wks_1.append_table(values=[len(df), sum(df['Views']), str(datetime.datetime.today().strftime('%Y-%m-%d'))])

driver.close()


