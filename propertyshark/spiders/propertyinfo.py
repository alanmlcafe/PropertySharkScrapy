# -*- coding: utf-8 -*-
from collections import OrderedDict
import scrapy

from ..items import PropertysharkItem

class PropertyinfoSpider(scrapy.Spider):
    name = 'propertyinfo' #Spider name
    allowed_domains = ['propertyshark.com']
    start_urls = [] #Urls where scrapy will begin the crawl
    url_base = "https://www.propertyshark.com/mason/Property/"
    num_starting_page = 900001 #Starting page, we will parse from
    num_pages_to_read = 49999 #Number of pages we want

    #Customized settings to Optimized broad scrapy crawls
    custom_settings = { 
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': .05,
        'REDIRECT_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': False, #Turn to true to lessen load on website
        'AUTOTHROTTLE_START_DELAY': .05,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 100,
        'FEED_URI': "tmp/property" + str(num_starting_page) + "-" + str(num_pages_to_read + num_starting_page) +".csv"
    }
    
    def __init__(self):
        #===Tables of the property shark website===
        #Contains, building address, zip code, borough, lot size, building class, and year built
        self.table1_col21_prefix = "//div[@id = 'ny/nyc/summary_property_overview_content']/div/div[@class = 'cols21']/table/tr[" 
        self.table1_col22_prefix = "//div[@id = 'ny/nyc/summary_property_overview_content']/div/div[@class = 'cols22']/table/tr[" 
        #Contains neighborhood name, nearest school district, and distance of closest police and fire stations
        self.table2_col21_prefix = "//div[@id = 'ny/nyc/summary_other_charac_content']/div/div[@class = 'cols21']/table/tr["
        self.table2_col22_prefix = "//div[@id = 'ny/nyc/summary_other_charac_content']/div/div[@class = 'cols22']/table/tr["

        #===Suffix of xpath, used to make xpath shorter===
        #The suffix of the thing we are looking for
        self.xpath_suffix_name = "]/td/table/tr/th/text()"
        #The suffix of the result
        self.xpath_suffix_result = "]/td/table/tr/td/text()"

        #Dictionary of property information, the website has them in order of the list
        self.table1_col21_dict = {'Property address':'building_addr', 'Zip code':'zipcode', 
        'Borough':'borough'} 
        self.table1_col22_dict = {'Lot sqft':'lot_size', 'Building class':'building_class',
        'Year built':'year_built'}

        #Populate the start urls
        for i in range(self.num_pages_to_read + 1):
            url = self.url_base + str(i + self.num_starting_page)
            self.start_urls.append(url) 

    #TODO: Delete line below
    #response.xpath("//div[@id = 'ny/nyc/summary_property_overview_content']/div/div[@class = 'cols21']/table/tr[1]/td/table/tr/td/text()").extract_first()

    #Parse function
    def parse(self, response):
            
        print(response) #Prints out the url of the website

        item = PropertysharkItem() #Scrapy item container, acts sort of like a dictionary
        item['building_addr'] = '' #Initialize it so we can check if it is empty later

        ##This for loop finds the address, zipcode, and borough
        #Read all the columns of a table and stops when it reaches end of table or runs 6 times (Maximum number of entries for this column)
        for index in range(6):
            index_as_str = str(index + 1)
            if response.xpath(self.table1_col21_prefix + index_as_str + self.xpath_suffix_name).extract_first() == None:
                break
            if response.xpath(self.table1_col21_prefix + index_as_str + self.xpath_suffix_name).extract_first() in self.table1_col21_dict:
                item_arg_name = self.table1_col21_dict[response.xpath(self.table1_col21_prefix + index_as_str + self.xpath_suffix_name).extract_first()]
                item[item_arg_name] = response.xpath(self.table1_col21_prefix + index_as_str + self.xpath_suffix_result).extract_first()

        #If we did not get a building address, the site redirected us to a page that is useless, so skip 
        if item['building_addr'] is None or len(item['building_addr']) == 0:
            return

        ##This for loop finds the lot size, building class, and year built
        #Read all the columns of a table and stops when it reaches end of table or runs 6 times (Maximum number of entries for this column)
        for index in range(6):
            index_as_str = str(index + 1)
            if response.xpath(self.table1_col22_prefix + index_as_str + self.xpath_suffix_name).extract_first() == None:
                break
            if response.xpath(self.table1_col22_prefix + index_as_str + self.xpath_suffix_name).extract_first() in self.table1_col22_dict:
                item_arg_name = self.table1_col22_dict[response.xpath(self.table1_col22_prefix + index_as_str + self.xpath_suffix_name).extract_first()]
                item[item_arg_name] = response.xpath(self.table1_col22_prefix + index_as_str + self.xpath_suffix_result).extract_first().rstrip('\n')

        #==========================================================================
        #The rest of the statements have a constant path, therefore no loop needed
        #==========================================================================

        #Getting name of property neighborhood
        item['neighborhood'] = response.xpath(self.table2_col21_prefix + "1" + self.xpath_suffix_result).extract_first() 

        #Getting school district of property
        item['school_district'] = response.xpath(self.table2_col21_prefix + "2" + self.xpath_suffix_result).extract_first() 

        #Add if statements to check if there are any residential/commerical
        property_type = response.xpath(self.table2_col21_prefix + "3" + self.xpath_suffix_name).extract_first() 
        property_type2 = response.xpath(self.table2_col21_prefix + "4" + self.xpath_suffix_name).extract_first() 
        
        if property_type == 'Residential Units':
            #Getting amount of residential units within property(If any)
            item['residential_units'] = response.xpath(self.table2_col21_prefix + "3" + self.xpath_suffix_result).extract_first() 
            if property_type2 == 'Commercial Units':
                #Getting amount of commerical units within property(If any)
                item['commerical_units'] = response.xpath(self.table2_col21_prefix + "4" + self.xpath_suffix_result).extract_first() 
        elif property_type == 'Commerical Units':
            #Getting amount of commerical units within property(If any)
            item['commerical_units'] = response.xpath(self.table2_col21_prefix + "3" + self.xpath_suffix_result).extract_first() 

        temp = response.xpath(self.table2_col22_prefix + "1" + self.xpath_suffix_result).extract_first()
        if temp:
        #Getting closest police station, property shark has a '\n' string terminator at the beginning of it
            item['closest_police_station'] = response.xpath(self.table2_col22_prefix + "1" + self.xpath_suffix_result).extract_first().strip('\n')

        #Getting closest fire station, property shark has a '\n' string terminator at the beginning of it
        temp = response.xpath(self.table2_col22_prefix + "2" + self.xpath_suffix_result).extract_first()
        if temp:
            item['closest_fire_station'] = response.xpath(self.table2_col22_prefix + "2" + self.xpath_suffix_result).extract_first().strip('\n')

        #Item will be stored in a csv, csv settings in settings.py
        yield item
    