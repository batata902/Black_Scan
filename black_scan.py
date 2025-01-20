import requests
from bs4 import BeautifulSoup
import sys
from os import system


def limpa(url):
	separado = url.split('=')
	final = separado[0] + '='
	return final


def get_links(url):
	response = requests.get(url)
	parser = BeautifulSoup(response.text, 'html.parser')
	links = parser.find_all('a')
	for link in links:
		if link['href'].startswith('http://') or link['href'].startswith('https://'):
			if link['href'] in lista_url:
				pass
			else:
				lista_url.append(link['href'])
		elif 'php?' in link['href']:
			if link['href'] in lista_url:
				pass
			else:
				lista_url.append(url + link['href'])


def sqli_scan(list, listaver=True):
	if listaver is False:
		verific = requests.get(list + "'")
		if 'Fatal error' in verific.text or 'SQL syntax' in verific.text:
			print (f'\033[32mFalha SQLi encontrada -->\033[m {list}')
		else:
			print ('A url fornecida parece não ser vulnerável.')
	if listaver:
		session = requests.Session()
		for link in list:
			try:
				verific = session.get(link + "'")
				if 'Fatal error' in verific.text or 'SQL syntax' in verific.text:
					print (f'\033[32mFalha SQLi em -->\033[m {link}')
				else:
					pass
			except requests.exceptions.ConnectionError:
				pass
			except KeyboardInterrupt:
				print ('O usuário escolheu sair')
				sys.exit()



def xss_scan(list, listaver=True):
	if listaver is False:
		url = limpa(list)
		response = requests.get(url + '<script> alert("pirocadesabao") </script>')
		if 'pirocadesabao' in response.text:
			print (f'\033[32mPossivel falha XSS em -->\033[m {list}')
		else:
			pass
	if listaver:
		session = requests.Session()
		for link in list:
			try:
				url = limpa(link)
				response = session.get(url + '<script> alert("pirocadesabao") </script>')
				if 'pirocadesabao' in response.text:
					print (f'\033[32mFalha XSS em -->\033[m {link}')
				else:
					pass
			except requests.exceptions.ConnectionError:
				pass
			except KeyboardInterrupt:
				print ('O usuário escolheu sair')
				sys.exit()



lista_url = list()

try:
	url = sys.argv[1]
	crawl = sys.argv[2]
	modo = sys.argv[3] # 3 modos: SQLi Scan, XSS Scann, Show Links, SQLi and XSS Scan

	if crawl == '--one-link' and modo == '--sqli':
		sqli_scan(url, listaver=False)
	elif crawl == '--get-all' and modo == '--sqli':
		get_links(url)
		sqli_scan(lista_url)

	if crawl == '--one-link' and modo == '--xss':
		xss_scan(url, listaver=False)
	elif crawl == '--get-all' and modo == '--xss':
		get_links(url)
		xss_scan(lista_url)

	if crawl == '--one-link' and modo == '--sqli-xss':
		sqli_scan(url, listaver=False)
		xss_scan(url, listaver=False)
	elif crawl == '--get-all' and modo == '--sqli-xss':
		get_links(url)
		sqli_scan(lista_url)
		print ()
		print ('=' * 60)
		print ()
		xss_scan(lista_url)
except IndexError:
	print ('''\033[32mUso: python3 black_scan.py [url] [--one-link/--get-all] [--sqli/--xss/--sqli-xss] 
			Etapas:
			{Especificando quantos alvos}
			--one-link : Diz ao programa para escanear apenas o link fornecido
			--get-all : Diz ao programa para escanear o link dado e todos os que estiverem dentro dele
			
			{Modo}
			--sqli : Busca apenas por vulnerabilidade de SQL Injection na/nas url(s) alvo
			--xss : Busca apenas por vulnerabilidade de XSS (Cross-Site-Scripting) na/nas url(s) alvo
			--sqli-xss : Busca por SQL Injection e por XSS na/nas url alvo\033[m''')
