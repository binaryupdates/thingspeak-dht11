import http.client
import urllib.parse
import time
import RPi.GPIO as GPIO
import dht11
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

instance = dht11.DHT11(pin=21)

def doit():
	global temperature, humidity
	#temperature=0
	#humidity=0
	result = instance.read()
	if result.is_valid():
		temperature = result.temperature
		humidity = result.humidity
		print ("Temp:",temperature,"Humid:",humidity)
	params = urllib.parse.urlencode({'field1': temperature,'field2': humidity,'key':'UM85DIA10C5XWMGW'})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = http.client.HTTPConnection("api.thingspeak.com:80")

	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print(response.status, response.reason)
		data = response.read()
		conn.close()
	except:
		print ("connection failed")	

#sleep for 16 seconds (api limit of 15 secs)
if __name__ == "__main__":
	while True:
		doit()
		time.sleep(16) 
