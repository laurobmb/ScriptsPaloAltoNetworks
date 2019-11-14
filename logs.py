#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from xml.etree import ElementTree
import sys, requests, argparse
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import urllib3


class PA_Invetory(object):

	def __init__(self):
		self.lendo_argumentos()
		if self.args.ipv4 != None or self.args.destination_zone != None or self.args.destination_address != None:
			if self.args.ipv4 and self.args.destination_address and self.args.destination_zone:
				self.iniciando(self.args.ipv4, self.args.destination_address, self.args.destination_zone)
				print('Arquivo numeros.png salvo na pasta')
				exit(0)
		else:
			print('erro: falta argumento')
			exit(0)

	def get_job_www(self,fw_ipv4,destination_address,destination_zone):
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		last_hour_date_time = datetime.now() - timedelta(hours = 1)
		last_hour_date_time = last_hour_date_time.strftime('%Y/%m/%d %H:%M:%S')
		URL = 'https://paloalto/api/?type=log&log-type=traffic&query='
		KEY = '&key='+PrivateKey
		QUERY = '( zone.src eq '+destination_zone+') and ( addr.dst in '+destination_address+' ) and (( port.dst eq 80 ) or ( port.dst eq 443 )) and (receive_time geq '+'\''+last_hour_date_time+'\''+')'
		NLOG = '&nlogs=15'
		url_completa = URL+QUERY+NLOG+KEY
		url_completa = url_completa.replace("paloalto", fw_ipv4)
		response = requests.get(url_completa, verify=False)
		response = response.text
		arquivo = open("paloalto.xml", "w")
		arquivo.write(response)
		arquivo.close()
		file_name='paloalto.xml'
		dom=ElementTree.parse(file_name)
		xml=dom.findall('result')
		for i in xml:
			trabalho = i.find('job').text
		return trabalho
	
	def get_log(self,fw_ipv4,job):
		URL = 'https://paloalto/api/?type=log&action=get&job-id=xxxxx'
		KEY = '&key='+PrivateKey
		url_completa = URL+KEY
		url_completa = url_completa.replace("paloalto", fw_ipv4)
		url_completa = url_completa.replace("xxxxx", job)
		lista_ip =[]
		response = requests.get(url_completa, verify=False)
		response = response.text
		arquivo = open("ips.xml", "w")
		arquivo.write(response)
		arquivo.close()
		file_name='ips.xml'
		dom=ElementTree.parse(file_name)
		xml=dom.findall('result/log/logs/entry')
		for i in xml:
			lista_ip.append(i.find('src').text)
		return lista_ip

	def lendo_argumentos(self):
		parser = argparse.ArgumentParser()
		#group = parser.add_mutually_exclusive_group()
		parser.add_argument('-z', '--destination_zone')		
		parser.add_argument('-d', '--destination_address')		
		parser.add_argument('-4', '--ipv4', type=str, help='Endereço ipv4 do firewall paloalto')
		self.args = parser.parse_args()

	def iniciando(self,fw_ipv4,destination_address,destination_zone):	
		numero_job = self.get_job_www(fw_ipv4,destination_address,destination_zone)
		ips = self.get_log(fw_ipv4,numero_job)
		dicionario = Counter(ips)
		fig, ax = plt.subplots()
		lista_valores = dicionario.values()
		lista_nomes = dicionario.keys()
		
		def make_autopct(values):
			def my_autopct(pct):
				total = sum(values)
				val = int(round(pct*total/100.0))
				return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
			return my_autopct

		ax.pie(dicionario.values(), labels=dicionario.keys(), autopct=make_autopct(lista_valores),shadow=True)
		ax.axis('equal')
		ax.set(title='Log de acesso IPv4 Address')
		fig.savefig('pie.png', dpi=100, figsize=(100, 100))
		plt.show()
		fig, ax = plt.subplots()
		plt.bar(dicionario.keys(), dicionario.values())
		fig.savefig('barras.png', dpi=100, figsize=(100, 100))

		plt.show()		


if __name__ == '__main__':
	PrivateKey = [chave]
	PA_Invetory()
