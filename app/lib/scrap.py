''' Importing Area'''
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re, os, hashlib
from . import helper
from . import  logger
from datetime import datetime
from app.db import connection , module



# Global Declaration
CACHE = 3 #Minutes
url = 'https://thenewdaily.com.au/news/coronavirus/'
html = 'app/templates/news.html'
opt_html = 'app/templates/filterNews.html'
current_date = datetime.now().strftime('%Y/%m/%d')

class Scrap:
    _url =''
    _data =''
    _log = None
    _soup = None

    #Constructor
    def __init__(self,url,log):
        self._url =url
        self._log = log

    # Method to request web page
    def retrive_webpage(self):
        try:
            req = Request(self._url,headers={'User-Agent': 'Mozilla/5.0'}) # Act as browser
            inp_html = urlopen(req)
        except Exception as e:
            print(e)
            logger.log(str(e))
        else:
            self._data = inp_html.read()
            if len(self._data)>0:
                print("Data Retrive Sucessfully")

    #Method that check Change

    # Method to write filter data into output file
    def write_webPage(self, filepath= html, data=''):
         if data is '':
          data = self._data
         helper.write_website(filepath,data)

    # Method  to read from the website
    def read_webPage(self,filePath=html):
        self._data = helper.get_website(filePath)

    # Method to Print all extract data from website
    def print_data(self):
        print(self._data)

    # Method to parse data into HTML format
    def convertDataBs(self):
        self._soup = BeautifulSoup(self._data,"html.parser")

    def check_update(self):
        chunkSize = 10000
        i=0

        if helper.check_file(opt_html):
            #File Handeling and HTML parsing
            self._url = "file://" + os.getcwd() +"/app/templates/filterNews.html"
            self.retrive_webpage()
            self.convertDataBs()
            data_parse = self._soup.find_all(['li']) # finds all <ol> from the html

            # Querying data from html and tally with database
            for tag in data_parse:
                link = tag.find('a').get('href')
                date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', link)[0]  # Get New Publish date from URL
                title = tag.find('a').string  # Return String inside the heading tag
                print(title)
                if date == current_date:
                    self.check_db(date,link,title,len(data_parse))

    #Method to encode from long text to MD5
    def encode(self, txt):
         res = hashlib.md5(txt.encode())
         return res.digest()

    """Method to check from database
    where
    x[0] is date
    x[1] = URL
    x[1] = content
    """

    def check_db(self, date, url, content,counter):
        #Creating objects
        count=0  # Counter for total data record after SQL query
        con = connection.connection()
        mod = module.module()
        #Initial varaible
        en_content = self.encode(content)
        en_url = self.encode(url)
        #Query to get current current date content from database
        res = con.query('READ', "SELECT date, URl, content FROM news WHERE date='" + current_date + "'")
        length_res = len(res)
        if length_res > 0:
            for x in res:
                if x[0] == date:
                    en_db_url = self.encode(x[1])
                    en_db_content = self.encode(x[2])
                    if en_url != en_db_url and en_content== en_db_content:
                        # Same Content with change in URL
                        print("URL has been changed of " + x[1])
                        print("New URL is" + url)
                        con.query('UPDATE', "UPDATE news SET `url`= {} where `content`={}".format(url, content))
                        con.__del__()
                    elif en_url == en_db_url and en_content != en_db_content:
                        # Same URl with change in content
                        print("Title has been changed for following URL" + url)
                        print("New Title for the above link is " + content)
                        con.query('UPDATE', "UPDATE news SET `content`= {} where `url`={}".format(content, url))
                        con.__del__()
                    elif en_url != en_db_url and en_content != en_db_content and count == length_res:
                        #Check URL and Content if its not equal and count reach to length of select query
                        print("New Content has been added to website")
                        print("Details")
                        print("Website URL: " + url)
                        print("Heading: " + content)
                        mod.insert(date, datetime.now().time(), 'thenewdaily.com.au', url, content)
                    count +=1
        else:
            print("New news has been added to website on "+ current_date)
            print("Website URL: " + url)
            print("Heading: " + content)
            mod.insert(date, datetime.now().time(), 'thenewdaily.com.au', url, content)


    # Method to map output with HTML tags
    def htmlParser(self):
        counter=0
        news_list = self._soup.find_all(['article'])
        htmltext= '''
        <html>
        <head><title>News Update Detector</title></head>
        <body>
        {NEWS_LINKS}
        </body>
        </html>
        '''
        news_links ='<ol>'
        for tag in news_list:
            if tag.find('a').get('href') and tag.find('h1').string != None: # Find out all link from the main body of website
                link = tag.find('a').get('href')
                date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', link)[0] # Get New Publish date from URL
                title= tag.find('h1').string # Return String inside the heading tag
                if date == current_date:
                    counter +=1
                    # self.check_db(current_date,link,title,counter)
                    news_links += "<li><a href='{}' target='_blank'>{}</a></li>\n".format(link,title)
        news_links += '</ol>'

        htmltext =htmltext.format(NEWS_LINKS=news_links)

        self.write_webPage(filepath=opt_html,data=htmltext.encode())

