from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium_stealth import stealth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import lxml
import sys


# time.sleep(20)
# Create webdriver

debug = 0

if debug == 1:
    time.sleep(0)
else:
    time.sleep(20)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option(
    'prefs',
    {
        # 'profile.managed_default_content_settings.javascript': 2,
        'profile.managed_default_content_settings.images': 2,
        'profile.managed_default_content_settings.mixed_script': 2,
        'profile.managed_default_content_settings.media_stream': 2,
        'profile.managed_default_content_settings.stylesheets':2
    }
)
driver = webdriver.Remote(command_executor="http://172.18.0.2:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME, options=options)


link_mass = []
if debug == 1:
    df_read = pd.read_csv('/home/fedor12/Project/Parser/Parser-main/resources/Table/Places_Match(table-tennis)All.csv', delimiter=';')
else:
    df_read = pd.read_csv('/app/resources/Table/Places_Match(table-tennis)All.csv', delimiter=';')

df_inf = pd.DataFrame({
        'Name': pd.Series(link_mass, dtype='object'),
        'Address': pd.Series(link_mass, dtype='object'),
        'Lat': pd.Series(link_mass, dtype='object'),
        'Lon': pd.Series(link_mass, dtype='object'),
        'Height': pd.Series(link_mass, dtype='object'),
        'Timezone': pd.Series(link_mass, dtype='object'),

        'Error': pd.Series(link_mass, dtype='object'),
        'Link_match': pd.Series(link_mass, dtype='object'),
})

Namber = df_read.values.shape[0]
Ostring = ""
text1 = 0
text2 = 0
number = 0

if debug == 1:
    Ostring = "/home/fedor12/Project/Parser/Parser-main/resources/parser11/range"
else:
    Ostring = "/app/resources/parser/range"

with open(Ostring, "r") as file:  # Изменяется
    text1 = int(file.readline())
    text2 = int(file.readline())
    number = int(file.readline())


if debug == 1:
    text1 = 1
    text2 = 15

for i in range(text1, text2):
    # print(i)
    address = df_read["Address"].iloc[i]
    # print(address)
    city = re.sub(r",\s.{1,1000}", "", address, 1)
    city = re.sub(r".{1,1000}\s", "", city, 1)
    name = 0
    link = 0
    coordinates = 0
    error = 0
    lat = 0
    lon = 0
    height = 0
    timezone = 0

    try:
        name = df_read["Name"].iloc[i]
        link = df_read["Link"].iloc[i]
        driver.get(f"https://yandex.ru/maps/2/saint-petersburg/?ll=30.315635%2C59.938951&z=11")
        time.sleep(5)
        input = driver.find_element(by=By.CLASS_NAME, value='input__control').send_keys(address)
        buttons = driver.find_element(by=By.CLASS_NAME, value='small-search-form-view__icon').click()
        time.sleep(5)
        coordinates = driver.find_element(by=By.CLASS_NAME, value='toponym-card-title-view__coords-badge').text
        lat = re.sub(r",\s.{1,100}", "", coordinates, 1)
        lon = re.sub(r".{1,100},\s", "", coordinates, 1)
        print(link)
    except:
        error = 1
        pass


    time.sleep(3)
    driver.get(f"https://ru.wikipedia.org/wiki/{city}_(город)")
    time.sleep(3)
    tr = ''
    try:
        tr = driver.find_element(by=By.CLASS_NAME, value='infobox').find_elements(by=By.TAG_NAME, value='tr')
    except:
        pass
    for tag in tr:
        # print(tag.text)
        if re.sub(r"\s.{1,100}", "", tag.text, 1) == "Высота":
            height = re.sub(r"Высота центра\s", "", tag.text, 1)
        if re.sub(r"\s.{1,1000}", "", tag.text, 1) == "Часовой":
            timezone = re.sub(r"Часовой пояс\s", "", tag.text, 1)

    df_inf.loc[len(df_inf.index)] = [name, address, lat, lon, height, timezone, error, link]


if debug == 1:
    df_inf.to_csv(f'/home/fedor12/Project/Parser/Parser-main/resources/Match_Coordinates(table-tennis){number}.csv', index=False, sep=';',
                  encoding='utf-8-sig')
else:
    df_inf.to_csv(f'/app/resources/parser/Match_Coordinates(table-tennis){number}.csv', index=False, sep=';',
                  encoding='utf-8-sig')

driver.close()
driver.quit()


