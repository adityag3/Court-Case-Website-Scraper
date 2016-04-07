# This script is written by : Aditya Govil
# Github username : adityag3
# Website : http://adityagovil.co


#======================================================================================
#  PROGRAMMING CHALLANGE SOLUTION IN PYTHON
#======================================================================================


# HEADER FILES USED IN THIS PROGRAM
#import urllib 
import requests  #Used for get request 
from bs4 import BeautifulSoup as BS  #Used to scrape data from the sourcecode
from selenium import webdriver  #Mainly used for automated testing
from selenium.webdriver.support.ui import Select  #Used to select dropdown menus
from bs4 import BeautifulSoup   #used to scrape static webpages


#function to scrape page with details of a case
def get_case_status(case_type, case_num, year):

	#url with the form
	url = "http://courtnic.nic.in/supremecourt/casestatus_new/caseno_new.asp"

	browser = webdriver.Firefox()
	# browser = webdriver.PhantomJS()
	# About commented is used to test without opening actual browser

	#opens the url in the firefox browser
	browser.get(url)


	unique_css = "#seltype > option:nth-child(" + str(case_type) + ")"


	browser.find_element_by_css_selector(unique_css).click()
	inp_field = browser.find_element_by_css_selector('body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)')
	inp_field.send_keys(case_num)
	Select(browser.find_element_by_css_selector('#selcyear')).select_by_value(str(year))
	browser.find_element_by_css_selector("body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > form:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > input:nth-child(1)").click()


	#Dictionary with random data
	#It will have the real data after we scrape the webpage using BeautifulSoup4
	info_dict = {
			"Is_disposed" : True,
			"petitioner" : "",
			"respondent" : "",
			"pet_advocate" : "",
			"res_advocate" : "",

			#This sub-dictionary will be EMPTY if the field is not present
			"converted_case" : {
					"case_num" : 000,
					"year" : 0000,
			}
	}


	current_url = browser.current_url
	#print current_url
	
	#print(soup.get_text)

	status_ele =  browser.find_elements_by_xpath("//*[contains(text(), 'DISPOSED')]")
	status_ele = str(status_ele)


	if status_ele == []:
		info_dict['Is_disposed'] = False

	# browser.page_source gets the source code of the current page
	html_source = browser.page_source

	soup = BS(html_source)
	# Selects all the font tags present in that page
	ele = soup.find_all('font')


	# To get the data of the petitioner
	temp = str(ele[10].contents)
	l = len(temp)
	petitioner_str = str(temp[2:l-1])

	info_dict['petitioner'] = petitioner_str



	# To get the data of the respondent
	temp = str(ele[12].contents)
	l = len(temp)
	respondent_str = str(temp[2:l-1])

	info_dict['respondent'] = respondent_str


	# To get the data of the pet_advocate
	temp = str(ele[15].contents)
	l = len(temp)
	pet_advocate_str = str(temp[2:l-1])

	info_dict['pet_advocate'] = pet_advocate_str


	# To get the data of the res_advocate
	temp = str(ele[17].contents)
	l = len(temp)
	res_advocate_str = str(temp[2:l-1])
	info_dict['res_advocate'] = res_advocate_str


	# Checks if the converted case details are there or not
	# If no then deletes it's attribute in the dictionary
	if str(ele[5]) == "u' '":
		del info_dict['converted_case']

	# If there are present then it puts data in the dictionary
	else:
		temp = str(ele[5]).split('/')
		temp_2 = str(temp[0])
		info_dict['converted_case']['case_num'] = temp_2[3:]
		temp_2 = str(temp[1])
		L = len(temp_2)
		info_dict['converted_case']['year'] = temp_2[:l-1]

	return info_dict




#=================================================================================================
#		END OF FUNCTION
#=================================================================================================


#FUNCTION CALL

#test case used
get_case_status(5 ,15 ,2007)
#
	
	
# ----------- END ------------- END -------------- END --------------------
