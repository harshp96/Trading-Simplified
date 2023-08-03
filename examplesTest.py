import logging
from pmClient import PMClient
import pandas as pd
import json
from datetime import date, timedelta
from time import sleep
from tabulate import tabulate
from utils import PMService

logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
    filename="debug.log",  # Specify the log file name
    filemode="a"  # 'w' mode will overwrite the log file on each run, 'a' will append
)

def logInfo(debug, console=True):
    if console:
        logging.info(debug)
        print(debug)
    else:
        logging.info(debug)

pmObj = PMService()
pm = pmObj.getPmClient()
print(pm.get_live_market_data('LTP', ['NSE', '82880', 'OPTION']))

# try:
#     holdQuantity=1000
#     symbol='NIFTY'
#     strick_price=None
#     expiry_date=None

#     if expiry_date == None:
#         today = date.today()
#         if today.weekday() > 3:
#             expiry_date = today + timedelta(days=10-today.weekday())    # next week's thursday
#         else:
#             expiry_date = today + timedelta(days=3-today.weekday())     # this week's thursday
#         expiry_date = expiry_date.strftime('%d-%m-%Y')
#         logInfo('Taking expiry_date: {}'.format(expiry_date))
    
#     ce_holdPrice = 0
#     pe_holdPrice = 0
#     havePosition = False
#     while True:
#         try:
#             data = pm.get_option_chain("CALL", symbol, expiry_date)
#             df = pd.json_normalize(data['data']['results'])
#             if strick_price == None:
#                 strick_price = round(float(df['spot_price'].unique()[0])/50)*50
#                 logInfo('Taking strick_price: {}'.format(strick_price))
#             cedf = df[(df.stk_price == (strick_price+50))]
#             logInfo(tabulate(cedf, headers='keys', tablefmt='psql'))

#             data = pm.get_option_chain("PUT", symbol, expiry_date)
#             df = pd.json_normalize(data['data']['results'])
#             pedf = df[(df.stk_price == (strick_price))]
#             logInfo(tabulate(pedf, headers='keys', tablefmt='psql'))

#             pe_price = float(pedf.iloc[0]['price'])
#             ce_price = float(cedf.iloc[0]['price'])

#             if not havePosition:
#                 ce_holdPrice = ce_price
#                 pe_holdPrice = pe_price
#                 havePosition = True
#                 logInfo('=====================================/n Making entry position /n=====================================')
#                 logInfo('[CALL] Buy Price: {0}, Buy Quntity: {1}, For Strick Price: {2}'.format(ce_holdPrice, holdQuantity, strick_price+50))
#                 logInfo('[PUT] Buy Price: {0}, Buy Quntity: {1}, For Strick Price: {2}'.format(pe_holdPrice, holdQuantity, strick_price))

#             logInfo('Call [{0}->{1}], PUT [{2}->{3}], Current Position: {4}'.format(ce_holdPrice, ce_price, pe_holdPrice, pe_price, 
#                 round((ce_price-ce_holdPrice)*holdQuantity+(pe_price-pe_holdPrice)*holdQuantity)
#             ))

#         except Exception as e:
#             logging.error("Error: {}".format(e))
#             print("Error: {}".format(e))

#         sleep(5)
# except Exception as e:
#     logging.error("Error: {}".format(e))
#     print("Error: {}".format(e))
