from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

URL = "https://www.linkedin.com/jobs/search/?currentJobId=3687871543&f_LF=f_AL&geoId=105072130&keywords=python" \
      "%20developer&location=Poland&refresh=true "
chrome_driver_path = "C:/chromedriver.exe"

USERNAME = "boukhedenna.nedjm@gmail.com"
PASSWORD = "Nedjm@2021!"


def save_job():
        try:
            save_button = driver.find_element(By.CSS_SELECTOR, value=".jobs-save-button")
            # save_button = driver.find_element(By.LINK_TEXT, value="Save")
            # saved = save_button.find_element(By.TAG_NAME, value="span")
            try:
                saved = save_button.find_element(By.LINK_TEXT, value="Save")
            except NoSuchElementException or StaleElementReferenceException:
                print("Saved already!")
            else:
                save_button.click()
        except NoSuchElementException:
            # pass
            print("No Save Button!")
        else:
            save_button.click()

            # if(saved.text == "Save"):
            #     save_button.click()
            # else:
            #     pass  

def follow_company():
    company_link = driver.find_element(By.CSS_SELECTOR, value=".app-aware-link")
    try:
        pass
    except NoSuchElementException:
        pass
    else:
        pass


# open LinkedIn
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get(URL)
driver.maximize_window()

# click sign in button
time.sleep(2)
sign_in_button = driver.find_element(By.LINK_TEXT, value="Sign in")
sign_in_button.click()

# sign in
time.sleep(2)
username = driver.find_element(By.ID, value="username")
username.send_keys(USERNAME)
password = driver.find_element(by="id", value="password")
password.send_keys(PASSWORD)
password.send_keys(Keys.RETURN)

# CAPTCHA
time.sleep(2)
input("Click enter after CAPTCHA")

# get list of jobs
jobs_list = driver.find_element(by="xpath", value="//*[@id='main']/div/div[1]/div/ul")
jobs = jobs_list.find_elements(by="tag name", value="a")

# save job and follow company
for job in jobs:
    time.sleep(2)
    job.click()
    time.sleep(2)
    save_job()
    # time.sleep(2)
    # follow_company()

# close browser after 5 sec from ENTER key press
input()
time.sleep(5)
driver.quit()
