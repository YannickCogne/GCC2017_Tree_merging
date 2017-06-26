#!/usr/local/bin/python

from optparse import OptionParser

import json


with open('../test_data/Bering_Strait.d3_hierarchy') as data_file:    
    data = json.load(data_file)

for i in data:
    if i=="children":
        for d in data[i]:
            print (d["id"])

dico[data["id"]]={}
dico[data["id"]["data"]=data["data"]
dico[data["id"]["kids"]=data["kids"]
dico[data["id"][""]=data["data"]
dico[data["id"]["data"]=data["data"]
dico[data["id"]["data"]=data["data"]
