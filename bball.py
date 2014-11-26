import re
import numpy as np
import operator

f2 = open('rpi.txt', 'rw')
listOfRPI = {}
for line in f2:
	wordList = re.sub("[^\S]", " ",  line).split()
	listOfRPI[wordList[0]]=wordList[1]

f3 = open('rpi2.txt', 'rw')
listOfRPI2 = {}
for line in f3:
	wordList = re.sub(";", " ",  line).split()
	listOfRPI2[wordList[0]]=float(wordList[1])


def dominanceScore(opposingTeam, MOV, status):
	rpi = listOfRPI2[listOfRPI[opposingTeam]]
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

f = open('bball.txt', 'rw')

teamDic = {}

for line in f:
	wordList = re.sub("[^\S]", " ",  line).split()
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
	#print homeTeam + ' ' + str(homeScore) + ' ' + awayTeam + ' ' + str(awayScore)
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
	avg[key]=np.mean(teamDic[key]["schedule"])

sorted_x = sorted(avg.items(), key=operator.itemgetter(1),reverse=True)

for i in range(25):
    print '#'+str(i+1)+': '+sorted_x[i][0]+' '+str(sorted_x[i][1])







# o.close()
f3.close()
f2.close()
f.close()