import requests
import facebook
import json
import sqlite3
from datetime import date
import calendar

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

#creating database 
conn =  sqlite3.connect('Fblikes.sqlite')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Fblikes')
cursor.execute('CREATE TABLE Fblikes (post_name TEXT, created_at TIMESTAMP, weekday TEXT )')

for like in likesList:
	tup = like["name"],like["created_time"]
	cursor.execute('INSERT INTO FbLikes (post_name,created_at) VALUES (?,?)',tup)
	conn.commit()



def getDay():
	time=[]
	dateslist=[]
	weekday=[]
	for like in likesList:
		time.append(like["created_time"])
	for t in time:
		dateslist.append(time.replace('-', ' ').replace('T', ' ').split())
	for time in dateslist:
		








	







