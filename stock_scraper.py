import requests
from bs4 import BeautifulSoup
from socket import *
import time
import csv
import sys

def get_stock_prices(list_of_tickers):

	with open('stock_prices.csv', 'a', newline='\n', encoding='utf-8') as csvFile:
		fieldNames = ['Ticker Name', 'Company Name', 'Stock price']
		writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
		writer.writeheader()

		for ticker in list_of_tickers:
			stock_price_url = 'http://www.marketwatch.com/investing/stock/%s' %ticker
			try:
				webpage2 = requests.get(stock_price_url, timeout=10)
			except Exception as e:
				print(e)
				print('Request timed out for ' + ticker + '!!')

			soup = BeautifulSoup(webpage2.text, 'html.parser')

			for company in soup.find_all('a'):
				if company.text == ticker:
					req =  soup.find('p' , class_='data bgLast')
					price = req.text
					'''
					with open('stock_prices.txt', 'a') as f:
						f.write('Stock price of ' + company['title'] + '(' + ticker + ')' + ' is ' + price + '\n')
					print('Stock price of ' + ticker + ' is ' + price)
					'''
					writer.writerow({'Ticker Name': ticker, 'Company Name': company['title'], 'Stock price': price})

def get_stock_tickers():

	num_of_companies = 500
	url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
	webpage = requests.get(url)
	soup = BeautifulSoup(webpage.text, 'html.parser')
	table = soup.find('table', {'class': 'wikitable sortable'})
	tickers = []

	for row in table.findAll('tr'):	
		column = row.findAll('td')
		if len(column) > 0:
			if len(tickers) <= num_of_companies:
				tickers.append(str(column[0].string.strip()))
			else:
				break
	tickers.sort()

	return tickers

def main():

	print('This may take a few minutes ...')
	sys.stdout.flush()
	tickers_collection = get_stock_tickers()
	get_stock_prices(tickers_collection)

if __name__ == '__main__':

	start_time = time.time()
	main()
	print('Execution finished in ' + str(round(time.time() - start_time, 2)) + 's')
