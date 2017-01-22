from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class domain():

    def __init__(self,driver,url):

        driver.save_screenshot('/home/priorax/screenshot1.png')
        driver.get(url)
        driver.save_screenshot('/home/priorax/screenshot2.png')
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/header/ul/li[2]/em'))
        delay = 10  # seconds
        try:
            WebDriverWait(driver, delay).until(element_present)
        except:
            print("Panic loudly")
        self.beds = driver.find_element_by_xpath('//*[@id="main"]/div/header/div/div[2]/span[1]/span[2]/em').text
        self.bath = driver.find_element_by_xpath('//*[@id="main"]/div/header/div/div[2]/span[2]/span[2]/em').text
        self.cars = driver.find_element_by_xpath('//*[@id="main"]/div/header/div/div[2]/span[3]/span[2]/em').text
        self.rent = dict()
        self.rent["week"] = driver.find_element_by_xpath('//*[@id="main"]/div/header/div/div[1]/span').text.replace("$","")
        self.rent["month"] = float(self.rent['week'].replace("$","")) * 4.3
        self.bond = driver.find_element_by_xpath('//*[@id="main"]/div/header/ul/li[2]/em').text.replace("$","")
        self.fullAddress = driver.find_element_by_xpath('//*[@id="main"]/div/header/div/div[1]/h1').text
        self.streetAddress = self.fullAddress.split(",")[0]
        self.locality = self.fullAddress.split(",")[1].split("VIC")[0].strip()
        self.state = "VIC"
        self.postcode = self.fullAddress.split("VIC ")[1]
        self.bond = driver.find_element_by_xpath('//*[@id="main"]/div/header/ul/li[2]/em').text


    def content(self):
        content = dict()
        content["bond"] = self.bond
        content["beds"] = self.beds
        content["bath"] = self.bath
        content["cars"] = self.cars
        content["rent"] = self.rent
        content["streetAddress"] = self.streetAddress
        content["locality"] = self.locality
        content["state"] = self.state
        content["postcode"] = self.postcode
        content["fullAddress"] = self.fullAddress
        return content
