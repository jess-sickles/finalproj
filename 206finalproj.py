import requests
import facebook
import json
import sqlite3
from datetime import date
import calendar
import datetime 

access_token = None
if access_token is None:
	access_token = input("\n Copy and paste token from explorer: \n ")

graph = facebook.GraphAPI(access_token)
likes = graph.get_connections('me','likes', limit=100) 
profile = graph.get_object('me', fields = 'name,likes')
#print(json.dumps(profile, indent = 4))
#caching content into json file 
likesList=[]
while True:
	try:
		with open('206_FinalFB_cache.json','a') as f:
				for like in likes['data']:
					f.write(json.dumps(like)+"\n")	
					likesList.append(like)
				likes = requests.get(likes['paging']['next']).json()
	except KeyError:
	
		#ran out of posts
		break	

def getDays(jsonlist):
	time=[]
	dateslist=[]
	weekday=[]
	for like in jsonlist:
		time.append(like["created_time"])
	for t in time:
		l = t.split('T')
		l.pop(1)
		new = str(l)
		new= new.replace("'","").replace("[","").replace("]","")
		format = "%Y-%m-%d"
		datetimeob = datetime.datetime.strptime(new,format)
		dateobj=datetimeob.date()
		dateslist.append(dateobj.weekday())
	finaldays = []
	for day in dateslist:
		if day == 0:
			finaldays.append("Monday")
		if day == 1:
			finaldays.append("Tuesday")
		if day ==2:
			finaldays.append("Wednesday")
		if day ==3:
			finaldays.append("Thursday")
		if day ==4:
			finaldays.append("Friday")
		if day==5:
			finaldays.append("Saturday")
		if day==6:
			finaldays.append("Sunday")
	return(finaldays)		

#creating database 
conn =  sqlite3.connect('Fblikes.sqlite')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Fblikes')
cursor.execute('CREATE TABLE Fblikes (post_name TEXT, created_at TIMESTAMP, weekday TEXT )')

days = getDays(likesList)

for like in likesList:
	day= days[likesList.index(like)]
	tup = like["name"],like["created_time"],day
	cursor.execute('INSERT INTO FbLikes (post_name,created_at,weekday) VALUES (?,?,?)',tup)
	conn.commit()

 


output = open("FaceBookLikes.txt","w")
day_dict={}
for day in days:
	day_dict[day] = day_dict.get(day,0) + 1
sorted_dict = sorted(day_dict.items(), key= lambda x: x[1], reverse = True)
for k,v in sorted_dict:
	output.write(k+ ": " + str(v)+ " likes \n")
output.write("The most popular day you liked posts: " + str(sorted_dict[0][0]+ "\n"))
output.write("The least popular day you liked posts: " + str(sorted_dict[-1][0]))
output.close()















		
#.date['created_time'][0:4]
#.ctime






	







