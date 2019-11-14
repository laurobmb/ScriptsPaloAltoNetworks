#!/usr/bin/python3

from xml.etree import ElementTree
import urllib.request
import ssl,os,sys

def paloalto_url(LINK,RULE):
	context = ssl._create_unverified_context()
	try:
		pagina=urllib.request.urlopen(LINK,context=context)
	except:
		print ("error 1")
		exit(1)
	e=30
	dom=ElementTree.parse(pagina)
	xml=dom.findall('result/entries/entry')
	for i in xml:
		name=i.find('name').text
		nh_state=i.find('nh_state').text
		if name == RULE:
			if 'UP' == nh_state:
				e=10
			elif 'DOWN' == nh_state:
				e=20
			else:
				e=30
	return e


def main(FW,PBF_RULE):
	firewall=FW
	rule=PBF_RULE
	key=[chave]
	api='<show><pbf><rule><name>'+rule+'</name></rule></pbf></show>'
	url='https://'+firewall+'/api/?type=op&cmd='+api+'&key='+key
	valor = paloalto_url(url,rule)
	print(valor)

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2])
