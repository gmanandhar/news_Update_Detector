''' Importing Area'''
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
from . import helper
from . import  logger
from datetime import datetime
from app.db import connection , module



# Global Declaration
CACHE = 3 #Minutes
url = 'https://thenewdaily.com.au/news/coronavirus/'
html = 'app/templates/news.html'
opt_html = 'app/templates/filterNews.html'

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

    # Method to write filter data into output file
    def write_webPage(self, filepath= html, data=''):
         if data is '':
          data = self._data
         helper.write_website(filepath,data)

    # Method  to read from the website
    def read_webPage(self,filePath=html):
        self._data = helper.get_website(filePath)

    # Method to change URL of Scrap class
    def change_url(self):
        self._url = url
    # Method to Print all extract data from website
    def print_data(self):
        print(self._data)

    # Method to parse data into HTML format
    def convertDataBs(self):
        self._soup = BeautifulSoup(self._data,"html.parser")

        # def check_update(self):
        #     con = connection.connection()
        #     date = datetime.date()
        #     res = con.query('READ', "SELECT website_name, URl, content FROM news WHERE date=" + date)
        #     if len(self._data) == len(res):

    # Method to map output with HTML tags
    def htmlParser(self):
        con = connection.connection()
        mod = module.module()
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
        current_date = datetime.now().strftime('%Y/%m/%d')
        res = con.query('READ', "SELECT date, URl, content FROM news WHERE date='" + current_date+"'")
        length_res = len(res)
        db_date = []
        db_url = []
        db_content = []
        if length_res > 0:
            for x in res:
                db_date += x[0]
                db_url += x[1]
                db_content +=[2]

        for tag in news_list:
            if tag.find('a').get('href') and tag.find('h1').string != None: # Find out all link from the main body og website
                link = tag.find('a').get('href')
                date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', link)[0]
                title= tag.find('h1').string # Return String inside the heading tag
                if length_res == 0:
                    mod.insert(date,datetime.now().time(),'thenewdaily.com.au',link,title)
                else:
                    for i in db_date:
                        if i == current_date and date == current_date:
                            if db_url[i] != link and db_content == title:
                                print("URL has been changed of " + title)
                                print ("New URL is" + link)
                                con.query('UPDATE',"UPDATE news SET `url`= {} where `content`={}".format(link,title))
                                con.__del__()
                            elif db_url == link and db_content != title:
                                print("Title has been changed for following URL" + link)
                                print("New Title for the above link is "+ title)
                                con.query('UPDATE', "UPDATE news SET `content`= {} where `url`={}".format(title, url))
                                con.__del__()


                news_links += "<li>{} <a href='{}' target='_blank'>{}</a></li>\n".format(date,link,title)
        news_links += '</ol>'

        htmltext =htmltext.format(NEWS_LINKS=news_links)

        self.write_webPage(filepath=opt_html,data=htmltext.encode())

