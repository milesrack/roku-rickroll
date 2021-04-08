#!/usr/bin/python3
from roku import Roku
import argparse
import sys
import time
import requests
from bs4 import BeautifulSoup
import socket

roku = Roku('0.0.0.0') #You don't need to change this, discovery will still work
myip = [(s.connect(('1.1.1.1', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1] #Local IP
parser = argparse.ArgumentParser()
parser.add_argument('-d','--discover',action='store_true',help='Discover Roku devices on the local network')
parser.add_argument('-t','--target',dest='target',help='Target to Rickroll')
parser.add_argument('-a','--target-all',dest='target_all',action='store_true',help='Target all Roku devices on the local network')
parser.add_argument('-r','--replay',dest='replay',type=int,nargs='?',const=0,default=0,help='Number of times to replay the video (default 0)')
args = parser.parse_args()

#Class to store the id attribute of YouTube
class YouTube:
	id = '837'

#Gets device name and serial number so it is easier to identify
def DeviceInfo(ip):
	url = 'http://%s:8060/query/device-info' % ip
	r = requests.get(url)
	content = BeautifulSoup(r.content, 'lxml')
	device_name = content.find('default-device-name')
	return device_name.text

#Looks for Roku devices on the local network and returns them in a list
def DiscoverRokus():
	try:
		print('Discovering Roku devices...')
		netid = '.'.join(myip.split('.')[:-1]) + '.' #Gets the first 3 octets of the local IP (eg. 10.0.0.5 -> 10.0.0.)
		rokus = []
		start = time.time()
		for i in range(1,256):
			try: #Appends IP to the 'rokus' list if a connection can be made on port 8060 (web server)
				rokuip = netid+str(i)
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(0.5)
				s.connect((rokuip,8060))
				s.close()
				name = DeviceInfo(rokuip)
				print('Discovered Roku device at %s [%s]' % (rokuip, name))
				rokus.append(rokuip)
			except (OSError,TimeoutError):
				pass
		end = time.time()
		#print('Scan took {:.2f}s'.format(end-start)) #Scan time will always be the same (socket timeout is constant), this line is only useful for testing
		return rokus
	except KeyboardInterrupt:
		print('Exiting...')
		sys.exit()

#Exits the program and leaves a message :)	
def Goodbye(ip):
	roku = Roku(ip)
	print('Exiting...')
	roku.search()
	time.sleep(5)
	roku.literal('haha :)')
	sys.exit()

def RickrollRoku(ip,replay_limit=0):
	try:
		print('Rickrolling %s...' % ip)
		roku = Roku(ip)
		#active_app = vars(roku.active_app)['name']
		roku.poweron()
		time.sleep(0.5)
		roku.home()
		time.sleep(0.5)
		if roku['YouTube'] == None:
			print('Installing YouTube...')
			roku.store(YouTube)
			time.sleep(1)
			roku.select()
			while vars(roku.active_app)['name'] == 'Roku':
				roku.select() #Presses select while YouTube isn't open (still installing), last select will close the installation dialogue
				time.sleep(1)
			print('Installed YouTube successfully!')
			[(roku.select(), time.sleep(0.2)) for i in range(2)] #Opens YouTube once it has been installed
			print('Launching YouTube...')
			fresh_install = True
		else:
			print('Launching YouTube...')
			roku.store(YouTube)
			time.sleep(1)
			roku.select()
			fresh_install = False
		if fresh_install:
			time.sleep(20) #Needs extra time to load after a fresh install
		else:
			time.sleep(15) #Waits for YouTube to open and load buttons
		#Navigates to the search section of YouTube
		roku.left()
		time.sleep(0.5)
		roku.up()
		time.sleep(0.5)
		roku.right()
		time.sleep(0.5)
		roku.literal('Rick Astley Never Gonna Give You Up') #Types out the name of the video
		time.sleep(1)
		roku.right() #Skips over suggested search terms so we can navigate to the video
		time.sleep(0.5)
		[(roku.down(), time.sleep(0.2)) for i in range(5)] #Skip over on-screen keypad
		roku.select()
		print('Increasing volume to 50...')
		#[(roku.volume_up(), time.sleep(0.2)) for i in range(50)] #Comment this out when testing (very loud)
		print('Playing \'Never Gonna Give You Up\' by Rick Astley...')
		time.sleep(9) # In case of ads
		roku.select() # Skips ad
		time.sleep(200) #Sleeps for almost the duration of the video, takes into account delay from ads		
		replay_count = 0
		while replay_count < replay_limit:
			replay_count += 1
			print('Replaying \'Never Gonna Give You Up\' by Rick Astley [%s]...' % replay_count)
			[(roku.reverse(), time.sleep(0.2)) for i in range(22)] #Rewinds to the beginning of the video
			roku.select()
			time.sleep(200)
		Goodbye(ip)
	except KeyboardInterrupt: 
		Goodbye(ip)

def main():
	if args.discover:
		DiscoverRokus()
	elif args.target:
		RickrollRoku(args.target,args.replay)
	elif args.target_all:
		discovered = DiscoverRokus()
		for ip in discovered:
			RickrollRoku(ip,args.replay)
	else:
		parser.print_help()

if __name__ == '__main__':
	main()