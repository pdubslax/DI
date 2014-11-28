import re
import numpy as np
import operator

f2 = open('rpi.txt', 'rw')
listOfRPI = {}
for line in f2:
	wordList = re.sub("[^\S]", " ",  line).split()
	listOfRPI[wordList[0]]=wordList[1]

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

mech = Browser()
mech2 = Browser()

url = "http://www.masseyratings.com/scores.php?s=267615&sub=11590&all=1&mode=2&format=0"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)
table = soup.find("pre")


url2 = "http://realtimerpi.com/rpi_Men.html"
page2 = mech2.open(url2)
html2 = page2.read()
soup2 = BeautifulSoup(html2)
table2 = soup2.findChildren("table")
dataTable = table2[4]
rows = dataTable.findChildren(['th', 'tr'])
firstTime = True

test=open('rpi2.txt','w')

for row in rows:
	cells = row.findChildren('a')
	start = 0
	for cell in cells:
		if len(cells) != 4:
			break
		value = cell.string
		if (start==0):
			#this is the teamname
			newName = value.replace(" ", "")+';'
			test.write(newName)

		elif (start==1):
			#the good rpi
			newRPI = value+';'
			test.write(newRPI)

		elif (start==3):
			newConference = value+';'+'\n'
			test.write(newConference)
		start += 1 

test.close()

f3 = open('rpi2.txt', 'rw')
listOfRPI2 = {}
for line in f3:
	wordList = re.sub(";", " ",  line).split()
	listOfRPI2[wordList[0]]= {}
	listOfRPI2[wordList[0]]["RPI"]=float(wordList[1])
	listOfRPI2[wordList[0]]["Conf"]=(wordList[2])
	



def dominanceScore(opposingTeam, MOV, status):
	rpi = listOfRPI2[listOfRPI[opposingTeam]]["RPI"]
	if (status==0):
		mult = 1
	elif ((status==1 and MOV>0) or (status==2 and MOV<0) ):
		mult = .7
	else :
		mult = 1.3

	if (MOV<0):
		finalResult = MOV*(1 - (rpi**3))*mult
	else:
		finalResult = MOV*(rpi**3)*mult
	return finalResult



test=open('test.txt','w')
test.write(table.string)
test.close()


with open("test.txt") as infile, open("test2.txt", "w") as outfile:
    for line in infile:
        outfile.write(line.replace(";", ""))
outfile.close()

f = open('test2.txt', 'rw')


teamDic = {}

for line in f:	
	wordList = re.sub("[^\S]", " ",  line).split()
	if len(wordList)==0:
		break
	homeTeam = ""
	awayTeam = ""
	foundHomeTeam = False
	neutralSite = False
	if (wordList[1][0]=='@'):
		foundHomeTeam = True
		homeTeam = wordList[1][1:]
		i = 2
		while (wordList[i][0].isdigit()==False):
			homeTeam += wordList[i]
			i+=1
		homeScore = int(wordList[i])
	else:
		awayTeam = wordList[1]
		i = 2
		while (wordList[i][0].isdigit()==False):
			awayTeam += wordList[i]
			i+=1
		awayScore = int(wordList[i])
	i+=1
	if (wordList[i][0]=='@'):
		homeTeam = wordList[i][1:]
		i += 1
		while (wordList[i][0].isdigit()==False):
			homeTeam += wordList[i]
			i+=1
		homeScore = int(wordList[i])
	elif (foundHomeTeam == False):
		homeTeam = wordList[i]
		i += 1
		while (wordList[i][0].isdigit()==False):
			homeTeam += wordList[i]
			i+=1
		homeScore = int(wordList[i])
		neutralSite = True
	else:
		awayTeam = wordList[i]
		i += 1
		while (wordList[i][0].isdigit()==False):
			awayTeam += wordList[i]
			i+=1
		awayScore = int(wordList[i])
#status 1=home 2 =away 0= neutral	
	if (homeTeam in teamDic):
		if (neutralSite):
			status = 0
		else:
			status = 1
		teamDic[homeTeam]["schedule"].append(dominanceScore(awayTeam,homeScore-awayScore,status))
	else:
		if (neutralSite):
			status = 0
		else:
			status = 1
		teamDic[homeTeam] = {}
		teamDic[homeTeam]["schedule"]=[]
		teamDic[homeTeam]["schedule"].append(dominanceScore(awayTeam,homeScore-awayScore,status))

	if (awayTeam in teamDic):
		if (neutralSite):
			status = 0
		else:
			status = 2
		teamDic[awayTeam]["schedule"].append(dominanceScore(homeTeam,awayScore-homeScore,status))
	else:
		if (neutralSite):
			status = 0
		else:
			status = 2
		teamDic[awayTeam] = {}
		teamDic[awayTeam]["schedule"] = []
		teamDic[awayTeam]["schedule"].append(dominanceScore(homeTeam,awayScore-homeScore,status))


# o = open('rpi.txt', 'w')
# for key in teamDic:
# 	o.write(key+' '+ key+ '\n')

avg = {}
for key in teamDic:
	avg[key] = {}
	avg[key]["meanDI"]=np.mean(teamDic[key]["schedule"])
	avg[key]["conference"]= listOfRPI2[listOfRPI[key]]["Conf"]

straightRank = {}
for key in teamDic:
	straightRank[key]=avg[key]["meanDI"]

sorted_x = sorted(straightRank.items(), key=operator.itemgetter(1),reverse=True)
sorted_y = sorted(avg.items(), key=operator.itemgetter(1),reverse=True)

import csv
with open('finalDI.csv', 'w') as fp:
	a = csv.writer(fp, delimiter=',')
	for i in range(len(sorted_x)):
		a.writerow([str(sorted_x[i][0]),str(sorted_x[i][1])])
	a.writerow('')
	for i in range(len(sorted_y)):
		a.writerow([str(sorted_y[i][0]),str(sorted_y[i][1]["meanDI"]),str(sorted_y[i][1]["conference"])])


print '\n'
name = raw_input('Enter your name: ')
print '\n'+"Hello " + name +'! Welcome to the Dominance Index' + '\n'
while (True):
	command = raw_input('Enter your command: ')
	if (command == 'help' or command == 'h'):
		print "Try the following commands:"
		print "     'h' or 'help' for documentation"
		print "     'q' or 'quit' to exit the program"
		print "     'p' or 'print' to print the top X in the index"
		print "     'c' or 'conf' to print the DI for a conference"
		print "     'l' or 'list' to list the different conferences"
	if (command == 'p' or command == 'print'):
		print '\n'
		command = raw_input('How many teams do you want to see? ')
		top = int(command)
		print '\n'
		for i in range(top):
			print '#'+str(i+1)+': '+sorted_x[i][0]+' '+str(sorted_x[i][1])
		print '\n'
	if (command == 'q' or command == 'quit'):
		print '\n'+"Good Bye. Come again soon." + '\n'
		break
	if (command == 'c' or command == 'conf'):
		print '\n'
		command = raw_input('What conference do you want to see? ')
		print '\n'
		for i in range (len(sorted_y)):
			if sorted_y[i][1]["conference"]==command:
				print sorted_y[i][0] + ' ' + str(sorted_y[i][1]["meanDI"])
		print '\n'
	if (command == 'l' or command == 'list'):
		print '\n'
		confDic = {}
		for i in range (len(sorted_y)):
			if sorted_y[i][1]["conference"] not in confDic:
				confDic[sorted_y[i][1]["conference"]] = 1
				print sorted_y[i][1]["conference"]
		print '\n' 
# o.close()
f3.close()
f2.close()
f.close()