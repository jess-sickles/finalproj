import requests
import facebook
import json
import sqlite3

access_token = None
if access_token is None:
	access_token = input("\n Copy and paste token from explorer: \n ")

graph = facebook.GraphAPI(access_token)
likes = graph.get_connections('me','likes') 
profile = graph.get_object('me', fields = 'name,likes')
#print(json.dumps(profile, indent = 4))
#caching content into json file 

i = 0
while i < 4:
		with open('206_FinalFB_cache.json','a') as f:
				for like in likes['data']:
					f.write(json.dumps(like)+"\n")	
				likes = requests.get(likes['paging']['next']).json()
				i+=1
				
				
				

#creating database 
# conn =  sqlite3.connect('Fblikes.sqlite')
# cursor = conn.cursor()
# cursor.execute('DROP TABLE IF EXISTS Fblikes')
# cursor.execute('CREATE TABLE Fblikes (post_name TEXT, post_ID TEXT, created_at TIMESTAMP )')

# cache_file = open('206_FinalFB_cache.json','r')
# cache_contents = cache_file.read()
# cache_file.close()
# CACHE_DICTION = json.loads(cache_contents)
# for like in CACHE_DICTION:
# 	tup = like["name"], like ["id"], like["created_at"]
# 	cursor.execute('INSERT INTO FbLikes (post_name,post_ID,created_at) VALUES (?,?,?)',tup)







	







