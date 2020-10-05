from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import sys
import threading
from urllib import *

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

def get_sise_usa(stock_name):
    url = "https://finance.yahoo.com/quote/"+stock_name+"?p="+stock_name
    spans = BeautifulSoup(urlopen(url).read(),features="lxml").findAll("span")
    data_list = dict()
    for span in spans:
        if 'Trsdu(0.3s) Fw(b)' in str(span):
            data_list.update(price = span.text)
        if 'Trsdu(0.3s)' in str(span) and '103' in str(span).replace(span.text,''):
            data_list.update(open = span.text)
    return data_list

end_program = False
show_all = False

def check_end():
    global end_program
    global show_all
    while(True):
        print('')
        s = input('Press \'q\' to exit, \'s\' to change show all option')
        if( s == 'q'):
            end_program = True
            break
        if( s == 's'):
            show_all = ~show_all

def get_data_and_show(stock_list_korea, stock_list_usa, duration):
    global end_program
    global show_all
    while(True):
        if(end_program == True):
            print('Exit Program...')
            break
        print('')
        print('============================================<'+time.strftime('%c', time.localtime(time.time()))+'>============================================')
        #  HangulAndComputer     	18900     	+400      	18810     	+90 
        print('Name                    Current         From Open       BoughtAt        Earned')
        for industry, code in stock_list_korea.items():
            if(end_program == True):
                print('Exit Program...')
                break
            print(industry, end = '')
            data = get_sise(code[0],1)
            delta = int(data['Debi'][0])
            int_value = int(data['CurJuka'][0])
            if( show_all == False):
                print('\t'+'\033[95m'+"{0:<10d}".format(int_value)+'\033[0m', end = '')
                if( delta == 0 ):
                    print('\t'+"{0:<10d}".format(0), end = '')
                elif( delta > 0 ):
                    print('\t'+'\033[31m'+'+'+"{0:<9d}".format(delta)+'\033[0m', end ='')
                elif( delta < 0 ):
                    print('\t'+'\033[32m'+"{0:<9d}".format(delta)+'\033[0m', end ='')
                print('\t'+'\033[95m'+"{0:<10d}".format(code[2])+'\033[0m', end = '')
                buy_delta = int_value - code[2]
                if( buy_delta == 0 ):
                    print('\t'+"{0:<10d}".format(0), end = '')
                elif( buy_delta > 0 ):
                    print('\t'+'\033[31m'+'+'+"{0:<9d}".format(buy_delta)+'\033[0m', end ='')
                elif( buy_delta < 0 ):
                    print('\t'+'\033[32m'+"{0:<9d}".format(buy_delta)+'\033[0m', end ='')
            else:
                print(data)
            if( int_value > code[1] ):
                print('\t'+'\033[31m'+'You Have to consider it!!!'+'\033[0m', end = '')
            print('')
        for industry, code in stock_list_usa.items():
            if(end_program == True):
                print('Exit Program...')
                break
            print(industry, end = '')
            data_list = get_sise_usa(code[0])
            float_value = float(data_list['price'])
            delta = float(data_list['price']) - float(data_list['open'])
            buy_delta = float(data_list['price']) - code[2]
            delta_str = str(delta)
            if( show_all == False):
                print('\t'+'\033[95m'+"{0:<10f}".format(float_value)+'\033[0m', end = '')
                if( delta == 0 ):
                    print('\t'+"{0:<10f}".format(0), end = '')
                elif( delta > 0 ):
                    print('\t'+'\033[31m'+'+'+"{0:<9f}".format(delta)+'\033[0m', end ='')
                elif( delta < 0 ):
                    print('\t'+'\033[32m'+"{0:<10f}".format(delta)+'\033[0m', end ='')
                print('\t'+'\033[95m'+"{0:<10f}".format(code[2])+'\033[0m', end = '')
                if( buy_delta == 0 ):
                    print('\t'+"{0:<10f}".format(0), end = '')
                elif( buy_delta > 0 ):
                    print('\t'+'\033[31m'+'+'+"{0:<9f}".format(buy_delta)+'\033[0m', end ='')
                elif( buy_delta < 0 ):
                    print('\t'+'\033[32m'+"{0:<10f}".format(buy_delta)+'\033[0m', end ='')
                else:
                    print(data_list)
                    print('')
            print('')
        for i in range(duration):
            if(end_program == True):
                print('Exit Program...')
                break
            time.sleep(1)

if __name__ == '__main__':
				#name			 code	    price to buy  price you buy
    stock_list_korea = {
				'Samsung               ':['005930', 59000, 58000],\
				'HangulAndComputer     ':['030520', 18800, 18810],\
				'SK Hynix              ':['000660', 83000, 84000],\
                                'Hyundai Car           ':['005380', 200000, 176500],\
                                'Kakao                 ':['035720', 379500, 369500]
                        }
    stock_list_usa = {
				'TESLA                 ':['TSLA',   500,   417],\
				'Nvdia                 ':['NVDA',   550,   495],\
				'Apple                 ':['AAPL',   104,   112.89],\
                                'Intel                 ':['INTC',   45,   50],\
                                'Microsoft             ':['MSFT',   250,  205]
			}
    thread = threading.Thread(target = check_end)
    thread.daemon = True
    thread.start()
    time.sleep(2)
    duration = 10
    get_data_and_show(stock_list_korea, stock_list_usa, duration)
