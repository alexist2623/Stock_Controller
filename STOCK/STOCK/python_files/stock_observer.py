from urllib import *
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import sys

def get_sise(stock_code, try_cnt):
	url="http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng?code={}".format(
stock_code)
	req=urlopen(url)
	result=req.read()
	xmlsoup=BeautifulSoup(result,"lxml-xml")
	stock = xmlsoup.find("TBL_StockInfo")
	stock_df=pd.DataFrame(stock.attrs, index=[0])
	stock_df=stock_df.applymap(lambda x: x.replace(",",""))
	return stock_df

#        except HTTPError as e:
#        logging.warning(e)
#        if try_cnt>=3:
#            return None
#        else:
#            get_sise(stock_code,try_cnt=+1)



def get_data_and_show(stock_list):
	while(True):
		for industry, code in stock_list.items():
			print(industry, end = '')
			data = get_sise(code[0],1)
			int_value = int(data['CurJuka'][0])
			print('\033[95m'+data['CurJuka'][0]+'\033[0m')
			if( int_value > code[1] ):
				print('\033[31m'+'You Have to sell it!!!'+'\033[0m')
		time.sleep(20)

if __name__ == '__main__':
	stock_list = {
				'Samsung':['005930', 89000],\
				'HangulAndComputer':['030520', 18800]
			}
	get_data_and_show(stock_list)
