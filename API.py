#Author: Kheshav Sewnundun ( kheshavsewnundun@gmail.com)
#Tag: v1.0.0
#Licence: MIT
from flask import flask, request
from datetime import datetime, date, timedelta
import os, calendar, json, sys, re

app = Flask(__name__)

@app.route("/")
def checkVirus():
	'''Function for checking virus'''
	fileName = request.args.get("fileName")
	timenow = datetime.now()
	relativeTime = datetime.now() - timedelta(minutes=2)
	relativeTimeStamp = calendar.timegm(relativeTime.timetuple())
	f =  os.popen("/opt/NAI/LinuxShield/libexec/sqlite /var/opt/NAI/LinuxShield/etc/nailsd.db 'select * from scanLog where i_tim > %s AND fileName=\"%s\"'" % (relativeTimeStamp,fileName))
	data = f.read().rstrip("\n")
	arr = []
	for line in data.split("\n"):
	        arr.append(tuple(line.split("|")))

	arr=tuple(arr)
	if len(arr[0][0]) is not 0:
		dic = {
		        "file": fileName,
		        "status": "FOUND",
		        "info" : { "timestamp" : [x[4] for x in arr] ,
		                   "path" : [x[6] for x in arr]
		                }
		      }
	else:
		dic = {
		        "file": fileName,
		        "status": "NOTFOUND"
		      }
	return json.dumps(dic)



if __name__ == "__main__":
	app.run()