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
		if self.args.commit:
			self.resposta = self.commit(self.args.firewall)
		elif self.args.job:
			self.resposta = self.get_job(self.args.firewall,self.args.job)		 			
		print(self.resposta)

	def help(self,FW,OBJETO):
		checkexiste=self.listar(FW)
		if OBJETO not in checkexiste:
			return 'Esse objeto '+OBJETO+' não existe.\nUse -f [Endereço IP do Firewall] -o [Nome do Agendamento]'
		else:
			return 'Use -f [Endereço IP do Firewall] -o [Nome do Agendamento]'

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

		xml=dom.findall('result/')
		for i in xml:
			ids = i.find('id').text
			user = i.find('user').text
			result = i.find('result').text
		print('Tarefa =',ids,'\nUsuário = ',user,'\nResultado = ',result)

		xml=dom.findall('result/job/details/line')
		for i in xml:
			resposta = i.text
		return resposta

	def lendo_args_cli(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-f', '--firewall', type=str, help="Endereço IP do firewall Palo Alto")
		parser.add_argument('-c', '--commit', type=str, help="Aplicar configurações do Firewall", choices=['commit'])
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


