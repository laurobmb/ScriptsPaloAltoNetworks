#!/usr/bin/python3

import xml.etree.ElementTree as ET
import urllib.request
import ssl,os,sys
import argparse
from datetime import datetime
import time

class PALO_ALTO(object):
	def __init__(self):
		self.lendo_args_cli()
		if self.args.list:
			self.resposta = self.listar(self.args.firewall)

		elif self.args.commit:
			self.resposta = self.commit(self.args.firewall)

		elif self.args.job:
			self.resposta = self.get_job(self.args.firewall,self.args.job)		 			

		elif self.args.set:
			if self.args.firewall or self.args.objeto is None:
				self.resposta = self.set(self.args.firewall,self.args.objeto)
			else:
				self.resposta = self.help(self.args.firewall,self.args.objeto)				

		print(self.resposta)

	def help(self,FW,OBJETO):
		checkexiste=self.listar(FW)
		if OBJETO not in checkexiste:
			return 'Esse objeto '+OBJETO+' não existe.\nUse -f [Endereço IP do Firewall] -o [Nome do Agendamento]'
		else:
			return 'Use -f [Endereço IP do Firewall] -o [Nome do Agendamento]'

	def set_schedule(self,LINK):
		context = ssl._create_unverified_context()
		try:
			pagina=urllib.request.urlopen(LINK,context=context)
		except:
			print ("error 1")
			exit(1)
		dom=ET.parse(pagina)
		xml=dom.findall('msg')
		for i in xml:
			name=i.text
		return name

	def listar(self,FW):
		lista=[]
		context = ssl._create_unverified_context()
		key = '&key='+PrivateKey
		xpath ='&xpath=/config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/schedule'
		url = 'https://'+FW+'/api/?type=config&action=get'+xpath+key
		pagina=urllib.request.urlopen(url,context=context)
		dom=ET.parse(pagina)
		root = dom.getroot()
		for elem in root.iter():
			try:
				e=elem.attrib['name']
				lista.append(e)
			except:
				error='Error'
		return lista

	def commit(self,FW):
		context = ssl._create_unverified_context()
		key = '&key='+PrivateKey
		url = 'https://'+FW+'/api/?type=commit&cmd=<commit></commit>'+key
		if DebugLevel == 1:
			print(url)		
		print('Tentando aplicar alterações no firewall ...')
		pagina=urllib.request.urlopen(url,context=context)
		dom=ET.parse(pagina)
		xml=dom.findall('msg')
		
		for i in xml:
			name=i.text

		if 'name' in locals():
			return name
		else:
			xml=dom.findall('result/job')
			for i in xml:
				jobid=i.text
				time.sleep(80)
				resultado = self.get_job(FW,jobid)
				return resultado

	def get_job(self,FW,JOBID):
		context = ssl._create_unverified_context()
		key = '&key='+PrivateKey
		url = 'https://'+FW+'/api/?type=op&cmd=<show><jobs><id>'+JOBID+'</id></jobs></show>'+key
		if DebugLevel == 1:
			print(url)
		pagina=urllib.request.urlopen(url,context=context)
		dom=ET.parse(pagina)
		xml=dom.findall('result/job/details/line')
		for i in xml:
			if 'successfully' in i.text:
				return i.text

	def set(self,FW,OBJETO):
		checkexiste=self.listar(FW)
		if OBJETO in checkexiste:
			HORARIO=self.get_hora()
			key = '&key='+PrivateKey
			xpath='&xpath=/config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/schedule/entry[@name=\''+OBJETO+'\']&element=<schedule-type><non-recurring><member>'+HORARIO+'</member></non-recurring></schedule-type>'
			url='https://'+FW+'/api/?type=config&action=set'+xpath+key
			if DebugLevel == 1:
				print(url)
			return self.set_schedule(url)
		else:
			return self.help(FW,OBJETO)

	def get_hora(self):
		diaria = datetime.now().strftime('%Y/%m/%d')
		diaria = diaria+'@08:00-'+diaria+'@23:59'
		return diaria

	def lendo_args_cli(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-l', '--list', help="listar schedules do firewall Palo Alto",action="store_true")
		parser.add_argument('-c', '--commit', help="Aplicar configurações do Firewall",action="store_true")
		parser.add_argument('-s', '--set', help="Setar schedule  do firewall Palo Alto com a data do dia anterior até às 29:59 do mesmo dia",action="store_true")
		parser.add_argument('-o', '--objeto', type=str, help="Shedule ja configurada no firewall")
		parser.add_argument('-f', '--firewall', type=str, help="Endereço IP do firewall Palo Alto")
		parser.add_argument('-j', '--job', type=str, help="Verificar Jobs dos commits do PaloAlto")		
		self.args = parser.parse_args()
    
if __name__ == '__main__':
    
    ''' DebugLevel 
    	0 = Não tem DEEBUG
    	1 = Mostra as URLs de acesso 
    '''
    DebugLevel=0
    global PrivateKey
    PrivateKey = [chave]
    PALO_ALTO()


