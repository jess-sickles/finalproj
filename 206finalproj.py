import requests
import facebook
import json

access_token = None
if access_token is None:
	access_token = input("\n Copy and paste token from explorer: \n ")

graph = facebook.GraphAPI(access_token)
likes = graph.get_connections('me','likes') 
profile = graph.get_object('me', fields = 'name,likes')
print(json.dumps(profile, indent = 4))

#caching 
i = 0
while i<=100:
	try:
		with open('myLikes.json','a') as f:
			for like in likes['data']:
				f.write(json.dumps(like)+"\n")
			likez = requests.get(likes['paging']['next']).json()
			i+=1
	except KeyError:
		#ran out of likes
		break





