from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import sqlite3
import schedule
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import discord_webhook


opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })



URL = "https://www.cowin.gov.in/home"
selector = "body > app-root > div > app-home > div.maplocationblock.bs-section > div > appointment-table > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > form > div > div > div.col-padding.matlistingblock > div > div > div > div:nth-child"

#put your teams credentials here
CREDS = {'pincode' : '281001', 'age': 50}

CREDS2 = {
	'State' : "Uttar Pradesh",
	'Dis' : "Mathura"
}

age = -1


def start_browser():

	global driver
	
	driver = webdriver.Chrome(r"chromedriver")
	driver.get(URL)

	WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
	find_slot()

	
def find_slot():
	srch = driver.find_elements_by_class_name("mat-input-element")[0]
	srch.click()
	srch.send_keys(CREDS["pincode"])
	time.sleep(1)
	
	if(age<18):
		'''discord_webhook'''
	elif(age<=44):
		srch = driver.find_elements_by_id("flexRadioDefault1")[0]
		srch.click()
	else:
		srch = driver.find_elements_by_id("flexRadioDefault3")[0]
		srch.click()

	srch = driver.find_elements_by_class_name("pin-search-btn")[0]
	srch.click()
	time.sleep(5)
	y=[]
	srch = driver.find_elements_by_class_name("available-para")
	if(len(srch)!=0):
		temp = srch[0].get_attribute("innerText")
		print(temp)
		discord_webhook.send_msg(temp,y)
	else:
		print("vaccines available")
		time.sleep(5)
		vavail=1
		while(vavail):
			path=selector
			path += "("+ str(vavail) + ")"
			
			try:
				xx=driver.find_element_by_css_selector(path)
				temp = list(xx.get_attribute("innerText").split("\n"))
				y.append((temp[0],temp[2]))
				vavail+=1
			except:
				break
		
		print(y)
		discord_webhook.send_msg("Available",y)
		print("Total vaccinantion centres available",len(y))







if __name__=="__main__":

	op = int(input())

	if(op==3):
		age = CREDS['age']

		start_browser()
	
	
	
	



'''
body > app-root > div > app-home > div.maplocationblock.bs-section > div > appointment-table > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > form > div > div > div.col-padding.matlistingblock > div > div > div > div:nth-child(1)

body > app-root > div > app-home > div.maplocationblock.bs-section > div > appointment-table > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > form > div > div > div.col-padding.matlistingblock > div > div > div > div:nth-child(2)
body > app-root > div > app-home > div.maplocationblock.bs-section > div > appointment-table > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > form > div > div > div.col-padding.matlistingblock > div > div > div > div:nth-child(3)
'''
