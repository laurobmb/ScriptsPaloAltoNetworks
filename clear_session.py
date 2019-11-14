#!/usr/bin/python3

from xml.etree import ElementTree
import urllib.request
import ssl,os,sys

def paloalto_url(LINK):
	context = ssl._create_unverified_context()
	try:
		pagina=urllib.request.urlopen(LINK,context=context)
	except:
		print ("Não foi possivel a conexão")
		exit(1)
	dom=ElementTree.parse(pagina)
	xml=dom.findall('result')
	for i in xml:
		member=i.find('member').text
	return member

def source(IP_FW,IP_SRC):
	api='<clear><session><all><filter><source>'+IP_SRC+'</source></filter></all></session></clear>'
	url='https://'+IP_FW+'/api/?type=op&cmd='+api+'&key='+PrivateKey
	resposta = paloalto_url(url)
	return resposta

def destination(IP_FW,IP_DEST):
	api='<clear><session><all><filter><destination>'+IP_DEST+'</destination></filter></all></session></clear>'
	url='https://'+IP_FW+'/api/?type=op&cmd='+api+'&key='+PrivateKey
	resposta = paloalto_url(url)
	return resposta

def main(FW_ipv4,destination_address):
	print(source(FW_ipv4,destination_address))
	print(destination(FW_ipv4,destination_address))

if __name__ == '__main__':
	FW_ipv4='10.1.0.210'
	destination_address='10.2.106.3'
	PrivateKey = [chave]	
	main(FW_ipv4,destination_address)
