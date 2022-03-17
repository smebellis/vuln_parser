import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import argparse

def read_filename():
   '''Handles user input of file name'''
   parser = argparse.ArgumentParser()
   parser.add_argument('-f', '--filename',
                       type=argparse.FileType('r'),
                       dest=r'C:\Users\ryane\python_practice\parse_anchore',
                       default= r'C:\Users\ryane\python_practice\parse_anchore',
                       help='Enter file name')
   args = parser.parse_args()
   return args.filename
    
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
#driver = webdriver.Firefox(executable_path=r'C:\Users\ryane\Downloads\geckodriver.exe')

#These four options avoid truncation in DataFrame outputs
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#This is the file that will be parsed
#df = pd.read_csv(read_filename())
df = pd.read_csv('anchore_security_ubi8.csv')

#base_url = 'https://access.redhat.com/security/cve/'
base_url = 'https://nvd.nist.gov/vuln/detail/'

#coverts column to string
df['severity'] = df['severity'].astype('string')

#creates new df with only the rows that have a severity of 'Critical' or 'High'
df2 = df[df['severity'].str.contains('Low')]

#create empty dictionary to store the CVEs and their descriptions
cve_list = {}

#iterate through each row and select
#'cve' column and get the cve number
for ind in df2.index:
    cve = (df2['cve'][ind])
    
    # print(cve)
    try:
        driver.get(f"{base_url}{cve}")
        description = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/table/tbody/tr/td/div/div[1]/p[1]").text
    except NoSuchElementException:
        pass
    # driver.implicitly_wait(5)
    #print(description)
    cve_list[cve] = description

for i, j in cve_list.items():
    print (i, j)
    
df3 = pd.DataFrame.from_dict(cve_list, orient='index')

df3.to_excel('test_anchore3.xlsx')

driver.close()







         