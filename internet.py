#!/usr/bin/python3
import requests
from io import BytesIO
import pycurl
import json
from requests import Session, Request

class httpReuest():
    def __init__(self, url, headers = [], postdata = "", referrer = ""):
        self.buffer = BytesIO()
        self.c = pycurl.Curl()
        self.c.setopt(self.c.URL, url)
        if headers != "":
            self.c.setopt(self.c.HTTPHEADER, headers)
        if postdata != "":
            self.c.setopt(self.c.POSTFIELDS, postdata)
        if referrer != "":
            self.c.setopt(self.c.REFERER, referrer)
        self.c.setopt(self.c.WRITEDATA, self.buffer)
        self.c.setopt(self.c.FOLLOWLOCATION, True)

    def performRequest(self):
        try:
            self.c.perform()
            f = json.loads((self.buffer.getvalue()).decode("utf-8"))
            return f
        except Exception as e:
            return "Address validation failed."

class cable():
    def __init__(self,address):
        if "/" in address and "Unit" not in address:
            self.Address = address.replace(" ", "+").replace(",", "%2C")
        else:
            self.Address = address
        url = "http://www.optus.com.au/portal/site/shop/template.BINARYPORTLET/menuitem.d8ade77814f20d81da238c7e189f01ca/resource.process/?javax.portlet.tpst=be4a23840fd90027ddd62db6f02000a0&javax.portlet.rst_be4a23840fd90027ddd62db6f02000a0=isRelocation%3Dfalse%26marketSegment%3DRES&javax.portlet.rid_be4a23840fd90027ddd62db6f02000a0=sqResultPage&javax.portlet.rcl_be4a23840fd90027ddd62db6f02000a0=cacheLevelPage&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken&vgnextoid=23dc201ef9fd3510VgnVCM1000001f80ff0aRCRD"
        headers = ['Content-Type: application/x-www-form-urlencoded; charset=UTF-8',
                   'Accept: */*',
                   'Referer: http://www.optus.com.au/shop/broadband/home-broadband/plans']
        query = 'address=' + self.Address + '&country=Australia&marketSegment=RES&queryType=token&site=consumer&token=0FOAUGHwXgBwAAAAAIAwEAAAAAWUQKwAAAAAAAADE5MgBkAAAAAP....8AAAAAAAAAAAAxOTIgaGlsdG9uAA--&attempt=1&planType=&campaign=BBPlansTest'
        self.http = httpReuest(url=url,headers=headers,postdata=query)

    def performRequest(self):
        try:
            pr = self.http.performRequest()
            print(pr)
            return pr
        except:
            return False

class nbn():
    def __init__(self,Address):
        self.address = Address
        location = json.loads(requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + Address).text)
        lat = location['results'][0]['geometry']['location']['lat']
        lng = location['results'][0]['geometry']['location']['lng']
        Address = Address.replace("Unit ","").replace(",","").split(" ")
        streetNumber = Address[0]
        streetName = Address[1] + "%20" + Address[2]
        if len(Address) == 7:
            suburb = Address[3] + "%20" + Address[4]
            postCode = Address[6]
        elif len(Address) == 5:
            suburb = Address[2] + "%20" + Address[3]
            postCode = Address[4]
        else:
            suburb = Address[2] + "%20" + Address[3]
            postCode = Address[5]
        self.url = "http://www.nbnco.com.au/api/map/search.html?lat=" + str(lat) + '&lng=' + str(lng) + '&streetNumber=' + str(streetNumber) + '&street=' + streetName + '&suburb=' + suburb + '&postCode=' + postCode + "&state=vic"
        self.referrer = "http://www.nbnco.com.au/connect-home-or-business/check-your-address.html"

    def performRequest(self):
        request = httpReuest(self.url,referrer=self.referrer)
        try:
            pr = request.performRequest()
            print(pr)
            return pr
        except:
            return "Not active"

class adsl():

    def __init__(self,Address):
        payload = {'Address' : Address }
        baseURI = 'http://www.adsl2exchanges.com.au/addresslookupstart.php'
        self.s = Session()
        req = Request('POST', baseURI, data=payload)
        self.prepped_request = req.prepare()

    def get_speed(self):
        resp = self.s.send(self.prepped_request,timeout=10)
        x = resp.text.split('\n')
        for line in x:
            if "Estimated speed" in line:
                speed = line.split("<br>")[2].split(' ')[3]
        return speed
