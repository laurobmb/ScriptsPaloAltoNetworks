from xml.etree import ElementTree
import urllib.request
import ssl,os,sys
import time as time
import datetime
from time import strptime
import pyautogui

os.system('clear')

def barra( nome ):  
    barra="======================================================================================"    
    titulo=nome
    print(barra)
    print(barra)
    print(titulo.center(len(barra)))
    print(barra)
    print(barra)
    return;

def paloalto_url(link):
	context = ssl._create_unverified_context()
	url = link
	url = url.replace("paloalto", sys.argv[1])
	try:
		pagina=urllib.request.urlopen(url,context=context)
	except:
		print ("error 1")
		exit(1)
	dom=ElementTree.parse(pagina)
	xml=dom.findall('result/content-updates/entry')
	for i in xml:
		filename=i.find('filename').text
		version=i.find('version').text
		releasedon=i.find('released-on').text
		print ("Nome:", filename, " versão:", version, "Released:", releasedon)
	return;


def data_atual():
  now = datetime.datetime.today()
  d = now.strftime("%d")
  m = now.strftime("%m")
  data=d+m
  return data

def main():

	if len(sys.argv) != 2:
		print('use: {} <ip do firewall>'.format(sys.argv[0]))
		sys.exit()

	PrivateKey = [chave]

	url='https://paloalto/api/?type=op&cmd=<request><anti-virus><upgrade><check></check></upgrade></anti-virus></request>&key='+PrivateKey
	barra("Atualização de Vacinas do PaloAlto - Antivírus")
	paloalto_url(url)
	url = 'https://paloalto/api/?type=op&cmd=<request><content><upgrade><check></check></upgrade></content></request>&key='+PrivateKey
	barra("Atualização de Vacinas do PaloAlto - Conteúdo de segurança")
	paloalto_url(url)
	url = 'https://paloalto/api/?type=op&cmd=<request><wildfire><upgrade><check></check></upgrade></wildfire></request>&key='+PrivateKey
	barra("Atualização de Vacinas do PaloAlto - Wildfire")
	paloalto_url(url)

	time.sleep(2)

	foto = pyautogui.screenshot()
	foto.save('/home/lpgomes/Imagens/'+data_atual()+' - firewall.png') 

if __name__ == '__main__':
	main()
