import requests
import facebook
import json
import sqlite3
from datetime import date
import calendar
import datetime 
import plotly.plotly as py
import plotly.graph_objs as go
from IPython.display import Image


#asking for access token since it expires after 2 hrs
access_token = None
if access_token is None:
	access_token = input("\n Copy and paste token from explorer: \n ")

graph = facebook.GraphAPI(access_token)
likes = graph.get_connections('me','likes', limit=100) 
profile = graph.get_object('me', fields = 'name,likes')

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
#function to get day of the week from created time taken from fb request
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

#function to return what time of day the like was created based on fb request data
def getTime(jsonlist):
	time = []
	timesList = []
	timesL = []
	for like in jsonlist:
		time.append(like["created_time"])
	for t in time:
		l = t.split('T')
		l.pop(0)
		new = str(l)
		new= new.replace("'","").replace("[","").replace("]","")
		timesList.append(new)
	for time in timesList:
		time = time.split(":")
		hour = int(time[0])
		minute = int(time[1])
		if hour in range(0,6) and minute in range(0,60):
			timesL.append("Late Night (12:00am-5:59am)")
		elif hour in range(6,12) and minute in range (0,60):
			timesL.append("Morning (6:00am-11:59am)")
		elif hour in range(12,18) and minute in range(0,60):
			timesL.append("Afternoon (12:00pm-5:59pm)")
		elif hour in range(18,25) and minute in range(0,60):
			timesL.append("Evening (6:00pm-11:59pm)")
	return(timesL)	
	

#creating database 
conn =  sqlite3.connect('Fblikes.sqlite')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Fblikes')
cursor.execute('CREATE TABLE Fblikes (post_name TEXT, created_at TIMESTAMP, weekday TEXT, time_of_day TEXT )')

#calling functions to get list of days, and time of day for each like pulled from data
days = getDays(likesList)
times= getTime(likesList)

#adding data into database
for like in likesList:
	#indexing the return lists from the functions to add the correct data into the correct row 
	day= days[likesList.index(like)]
	time = times[likesList.index(like)]
	#creating tuple to add into database
	tup = like["name"],like["created_time"],day,time
	#adding data into database
	cursor.execute('INSERT INTO FbLikes (post_name,created_at,weekday,time_of_day) VALUES (?,?,?,?)',tup)
	conn.commit()

 

#writing output to file to see how many likes there were per day, and most/least popular days 
output = open("FaceBookLikes.txt","w")
day_dict={}
for day in days:
	day_dict[day] = day_dict.get(day,0) + 1
sorted_dict = sorted(day_dict.items(), key= lambda x: x[1], reverse = True)
output.write("***LIKES PER DAY OF THE WEEK*** \n \n")
for k,v in sorted_dict:
	output.write(k+ ": " + str(v)+ " likes \n")
output.write("The most popular day you liked posts: " + str(sorted_dict[0][0]+ "\n"))
output.write("The least popular day you liked posts: " + str(sorted_dict[-1][0]) + "\n \n")

#writing to file about most and least popular times of day that likes were made
time_dict = {}
for time in times:
	time_dict[time] = time_dict.get(time,0) + 1
sorted_tdict = sorted(time_dict.items(), key = lambda x: x[1], reverse = True)
output.write("***LIKES PER TIME OF DAY*** \n \n")
for k,v in sorted_tdict:
	output.write(k+ ": " + str(v)+ " likes \n")
output.write("The most popular time of day you liked posts: " + str(sorted_tdict[0][0] + "\n"))
output.write("The least popular time of day you liked posts: " + str(sorted_tdict[-1][0]) + "\n \n")
output.close()

#creating list of values that shows count of likes per day
num=[]
for v in day_dict.values():
	num.append(v)

#creating visualization for facebook data
#API sign in for plotly tool 
py.sign_in('jsickles5', 'WPW3aurMkoTglr7zmK37')
#adding data that will appear in graph 
trace = go.Bar(x = ['Monday','Tuesday','Wednesday','Thursday','Friday', 'Saturday', 'Sunday'],
			  y= [a for a in num])
data=[trace]
#creating format of the image 
layout = go.Layout(title='Facebook Likes Per Weekday', width =800, height = 640)
fig = go.Figure(data=data, layout=layout)
#saving image as file in directory
py.image.save_as(fig, filename= "FBLikeGraph.png")
Image('FBLikeGraph.png')






	







