
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class rea():

    def __init__(self,driver,url):
        driver.get(url)

        element_present = EC.presence_of_element_located((By.ID, 'listing_info'))

        delay = 10  # seconds
        try:
            WebDriverWait(driver, delay).until(element_present)
        except:
            print("Panic loudly")

        self.beds = driver.find_element_by_xpath('//*[@id="listing_info"]/ul/li[2]/dl/dd[1]').text
        self.bath = driver.find_element_by_xpath('//*[@id="listing_info"]/ul/li[2]/dl/dd[2]').text
        self.cars = driver.find_element_by_xpath('//*[@id="listing_info"]/ul/li[2]/dl/dd[3]').text
        self.rent = dict()
        self.rent["week"] = driver.find_element_by_xpath('//*[@id="listing_info"]/ul/li[1]/p').text.replace("$","").split(" ")[0]
        self.rent["month"] = driver.find_element_by_xpath('//*[@id="features"]/div[1]/div/ul/li[5]/span').text.replace("$","")
        self.streetAddress = driver.find_element_by_xpath('//*[@id="listing_header"]/h1/span[1]').text
        self.locality = driver.find_element_by_xpath('//*[@id="listing_header"]/h1/span[2]').text
        self.state = driver.find_element_by_xpath('//*[@id="listing_header"]/h1/span[3]').text
        self.postcode = driver.find_element_by_xpath('//*[@id="listing_header"]/h1/span[4]').text
        self.bond = driver.find_element_by_xpath('//*[@id="features"]/div[1]/div/ul/li[6]/span').text.replace("$","")
        self.fullAddress =  self.streetAddress + ", " + self.locality + " " + self.state + " " + self.postcode

    def content(self):
        content = dict()
        content["beds"] = self.beds
        content["bath"] = self.bath
        content["cars"] = self.cars
        content["rent"] = self.rent
        content["bond"] = self.bond
        content["streetAddress"] = self.streetAddress
        content["locality"] = self.locality
        content["state"] = self.state
        content["postcode"] = self.postcode
        return content