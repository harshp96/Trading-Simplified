import logging
import sys
# sys.path.append('../')
from pmClient import PMClient
import pandas as pd
import json
from datetime import date, timedelta
from time import sleep

logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
    filename="debug.log",  # Specify the log file name
    filemode="a"  # 'w' mode will overwrite the log file on each run, 'a' will append
)

with open('API_Keys.json', "r") as file:
    api_keys = json.load(file)

pm = PMClient(api_key=api_keys['api_key'], api_secret=api_keys['api_secret'])

pm.set_access_token(api_keys['access_token'])
pm.set_public_access_token(api_keys['public_access_token'])
pm.set_read_access_token(api_keys['read_access_token'])

try:
    holdQuantity=1000
    symbol='NIFTY'
    strick_price=None
    expiry_date=None

    if expiry_date == None:
        today = date.today()
        if today.weekday() > 3:
            expiry_date = today + timedelta(days=10-today.weekday())    # next week's thursday
        else:
            expiry_date = today + timedelta(days=3-today.weekday())     # this week's thursday
        expiry_date = expiry_date.strftime('%d-%m-%Y')
        logging.info('Taking expiry_date: {}'.format(expiry_date))
        print('Taking expiry_date: {}'.format(expiry_date))
    
    ce_holdPrice = 0
    pe_holdPrice = 0
    havePosition = False
    while True:
        try:
            data = pm.get_option_chain("CALL", symbol, expiry_date)
            df = pd.json_normalize(data['data']['results'])
            if strick_price == None:
                strick_price = round(float(df['spot_price'].unique()[0])/50)*50
                logging.info('Taking strick_price: {}'.format(strick_price))
                print('Taking strick_price: {}'.format(strick_price))
            cedf = df[(df.stk_price == (strick_price+50))]

            data = pm.get_option_chain("PUT", symbol, expiry_date)
            df = pd.json_normalize(data['data']['results'])
            pedf = df[(df.stk_price == (strick_price))]

            pe_price = float(pedf.iloc[0]['price'])
            ce_price = float(cedf.iloc[0]['price'])

            if not havePosition:
                ce_holdPrice = ce_price
                pe_holdPrice = pe_price
                havePosition = True
                logging.info('=====================================/n Making entry position /n=====================================')
                logging.info('[CALL] Buy Price: {0}, Buy Quntity: {1}, For Strick Price: {2}'.format(ce_holdPrice, holdQuantity, strick_price+50))
                logging.info('[PUT] Buy Price: {0}, Buy Quntity: {1}, For Strick Price: {2}'.format(pe_holdPrice, holdQuantity, strick_price))

                print('=====================================/n Making entry position /n=====================================')
                print('[CALL] Buy Price: {0}, Buy Quntity: {1}, For Strick Price: {2}'.format(ce_holdPrice, holdQuantity, strick_price+50))
                print('[PUT] Buy Price: {0}, Buy Quntity: {1}, For Strick Price: {2}'.format(pe_holdPrice, holdQuantity, strick_price))

            logging.info('Call [{0}->{1}], PUT [{2}->{3}], Current Position: {4}'.format(ce_holdPrice, ce_price, pe_holdPrice, pe_price, 
                round((ce_price-ce_holdPrice)*holdQuantity+(pe_price-pe_holdPrice)*holdQuantity)
            ))
            print('Call [{0}->{1}], PUT [{2}->{3}], Current Position: {4}'.format(ce_holdPrice, ce_price, pe_holdPrice, pe_price, 
                round((ce_price-ce_holdPrice)*holdQuantity+(pe_price-pe_holdPrice)*holdQuantity)
            ))

        except Exception as e:
            logging.error("Error: {}".format(e))
            print("Error: {}".format(e))

        sleep(5)
except Exception as e:
    logging.error("Error: {}".format(e))
    print("Error: {}".format(e))
