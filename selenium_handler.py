from rea import rea
from selenium import webdriver
from domain import domain
import pprint

class handler():
    def __init__(self,url):
        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        driver.set_window_size(1366, 768)
        # let's not worry about reactive pages.
        self.generate_data(driver,url)


    def generate_data(self,driver,url):
        URL = url.replace("http://","").replace("www.","").replace("https://","")
        baseSite = URL.split(".")[0]
        try:
            if ("realestate" == baseSite):
                self.rental = rea(driver,"http://" + URL)
            elif (baseSite == "domain"):
                self.rental = domain(driver,"http://" + URL)
            else:
                raise("Panic loudly")
        except:
            print(driver.current_url)
            driver.save_screenshot('/home/priorax/screenshot.png')
            print(URL)
        driver.close()

    def json(self):
        return self.rental.content()

    def prettify_xml(self,elem):
        from xml.etree import ElementTree
        from xml.dom import minidom
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def internet(self):
        from internet import cable,nbn,adsl
        internet = dict()
        adsl = adsl(self.rental.fullAddress)
        internet["adsl"] = adsl.get_speed()
        nbn = nbn(self.rental.fullAddress)
        internet["nbn"] = nbn.performRequest()
        cable = cable(self.rental.fullAddress)
        internet["cable"] = cable.performRequest()
        return internet

    def xml(self,gmaps_config):
        import transport_gmaps
        from xml.etree.ElementTree import Element, SubElement, Comment, tostring
        top = Element('top')

        child = SubElement(top, 'Property')

        transport_options = transport_gmaps.transport(self.rental.fullAddress,gmaps_config)
        transport = SubElement(top,"Transport")
        pt = SubElement(transport,"Public_Transport")
        driving = SubElement(transport, "Driving")

        try:
            pt_details = transport_options.public_transport()
            time_taken_for_pt = str(round(pt_details["legs"][0]["duration"]["value"] / 60, 2))
            pt.text = time_taken_for_pt
        except:
            pt.text = "Unable to access Google Maps"
        try:
            driving_details = transport_options.driving()
            driving_str = str(round(driving_details["legs"][0]["duration"]["value"] / 60, 2))
            driving.text = driving_str
        except:
            driving.text = "Unable to access Google Maps"
        address = SubElement(child, 'Address')
        address.text = self.rental.fullAddress

        money = SubElement(child,'Money')
        rent = SubElement(money,"Rent")
        month = SubElement(rent,"Month")
        month.text = str(self.rental.rent["month"])
        week = SubElement(rent,"Week")
        week.text = str(self.rental.rent["week"])
        bond = SubElement(money,"Bond")
        bond.text = str(self.rental.bond).replace("$","")
        amenities = SubElement(child,"Amenities")
        car = SubElement(amenities,"Car")
        car.text = str(self.rental.cars)
        beds = SubElement(amenities, "Beds")
        beds.text = str(self.rental.beds)
        baths = SubElement(amenities, "Baths")
        baths.text = str(self.rental.bath)

        internet = SubElement(child,"Internet")
        adsl = SubElement(internet,"ADSL")
        cable = SubElement(internet, "Optus_Cable")
        nbn = SubElement(internet,"NBN")
        internet_details = self.internet()
        adsl.text = internet_details["adsl"]

        cable.text = "To_Implement_Later"
        nbnDetails = internet_details["nbn"]
        nbnAvaliable = SubElement(nbn,"Avalaiable")
        nbnDate = SubElement(nbn,"Date")
        if nbnDetails["serviceAvailableAddress"]:
            nbnAvaliable.text = "Available"
            nbnDate.text = "Now"
        else:
            nbnAvaliable.text = nbnDetails["servingArea"]["serviceStatus"]
            nbnDate.text = nbnDetails["servingArea"]["rfsMessage"]

        return self.prettify_xml(top)