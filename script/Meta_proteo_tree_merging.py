#!/usr/local/bin/python

from optparse import OptionParser

import json


with open('../test_data/Bering_Strait.d3_hierarchy') as data_file:    
    data = json.load(data_file)

#for i in data:
#    if i=="children":
#        for d in data[i]:
#            print (d["id"])
#

dico={}
dico[data["id"]]={}
dico[data["id"]]["name"]=data["name"]
dico[data["id"]]["data"]=data["data"]
dico[data["id"]]["kids"]=data["kids"]
dico[data["id"]]["children"]=data["children"]


def recursparser(data,dico):
	for i in data["children"]:
#		for t in i["data"]["sequences"]:
#			print (t)
		if i not in dico.keys(): 
			dico[i["id"]]={}
			dico[i["id"]]["name"]=i["name"]
			dico[i["id"]]["data"]=i["data"]
			dico[i["id"]]["data"]["sequences"]=set(dico[i["id"]]["data"]["sequences"])
			dico[i["id"]]["kids"]=set(i["kids"])
			dico[i["id"]]["children"]=i["children"]
			if len(i["children"]):
				recursparser(i,dico)
		return dico
dico2=recursparser(data,dico)

def dicoreader(dico,childlist):
	for i in childlist:
		print (dico[i]["name"])
		if len(dico[i]["kids"]):
			dicoreader(dico,dico[i]["kids"])


dicoreader(dico2,dico2[1]["kids"])

#print (len(dico))
#print (len(dico2))

