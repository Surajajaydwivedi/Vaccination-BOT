import time
import discord_webhook
import datetime
from datetime import date
import requests

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="
age = -1
'''# Importing necessary modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import ast

# WebDriver Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Target URL
driver.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=281001&date=08/05/2021")

# print(driver.title)

# Printing the whole body text
s=(driver.find_element_by_xpath("/html/body").text)
driver.close()
s=s[12:-1]
s=ast.literal_eval(s)
print("Vaccines Available!!")
print("details : ")
for i in s:
    print(i["name"],"(",i["min_age_limit"],"+) : ",i["available_capacity"])
# Closing the driver'''
def check_inf(pincode):
	starttime = time.time()
	while True:
		check_ones(pincode)
		time.sleep(1800.0 - ((time.time() - starttime) % 1800.0)) #checks availablily every 5 Hr


def check_ones(pincode):
	today = date.today()
	today = today.strftime("%d/%m/%Y")
	temp_url= URL +pincode+"&date="+str(today)
	result = requests.get(temp_url)

	
	if(result.status_code!=200):
		print("Sorry due to some techical reasons we cant access Vaccination Availability Info right now")
		discord_webhook.send_msg(-1,[])
		return
	dict = result.json()
	if len(dict["sessions"])==0:
		discord_webhook.send_msg(0,[])
	else:
		print("Vaccines Available!!")
		print("Details are also sent to your Discord")
		discord_webhook.send_msg(-1,dict["sessions"])





if __name__=="__main__":
	op = 0
	while(op<1 or op>3):
		op = int(input(("1. Check Availability \n2. Set Availability Reminder\nEnter option : ")))
		if(op<1 or op>2):
			print("Error, Wrong Input Try Again\n")
	
	
	if(op==1):
		pincode = input("Enter Your Area Pincode :")
		check_ones(pincode)
	elif(op==2):
		pincode = input("Enter Your Area Pincode :")
		check_inf(pincode)
