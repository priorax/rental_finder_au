Rental Finder (AU)

This project came around from me getting sick of looking up the internet avaliable at properties when looking for a new place to rent.

This is only made to work in Australia, if you are not Australian, sorry.

The idea is that you use this to make an XML file that can then be read in via Google Sheets using IMPORTXML

Input:
- http://server:port/?addr=(domain or rea url)
  - eg: http://localhost:9000/?addr=https://www.domain.com.au/49-cardinal-road-glenroy-vic-3046-11122907

Dependancies:
 - Selenium
 - Google Maps API Key
 - Google Maps Python Client
 - PhantomJS


To do:
  - Make the get-variable name more descriptive
  - Add a config file to manage web settings
     - For now, just update web_handler.py

  - Add a setup.py to manage dependancy management

  - Add a config file to manage destination for direction searches
  - Allow multiple destinations to be searched for
  - Allow an json output so that you can write you own tools