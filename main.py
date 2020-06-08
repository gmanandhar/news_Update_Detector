from app.db import connection

from app.lib import logger
from app.lib import scrap
from app.lib import helper
import sys
from app.db import connection

if __name__ == '__main__':
   #Define Log location
   #logger.set_log('app/templates/error.log')

   #SSL and HTTP issue for MAC
   if str(sys.platform) == 'darwin':
      helper.http_issue()

   #Creating Scraping object
   scp_obj = scrap.Scrap(scrap.url,logger)

   #Checking time interval to redownload content
   if helper.check_cache(scrap.html,scrap.CACHE):
      scp_obj.retrive_webpage()
      scp_obj.convertDataBs()
      scp_obj.htmlParser()




