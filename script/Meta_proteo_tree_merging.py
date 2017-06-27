#!/usr/local/bin/python

from optparse import OptionParser
import sys
import json


#A recursive parser to construct my own data structure and easier count the peptides
def recursparser(data,dico):
    for i in data["children"]:        
        if i["id"] not in dico.keys(): 
            dico[i["id"]]={}             
            listseq=list(i["data"]["sequences"])            
            dico[i["id"]]["name"]=i["name"]
            dico[i["id"]]["data"]=i["data"]
            dico[i["id"]]["data"]["sequences"]=set()
#set structure here is to have only non duplicate peptides when I run another data parsing
            for seq in listseq:
                dico[i["id"]]["data"]["sequences"].add(seq)
            dico[i["id"]]["kids"]=set(i["kids"])
#set structure here is to have only non duplicate kids when I run another data parsing
            dico[i["id"]]["data"]["self_count"]=len(dico[i["id"]]["data"]["sequences"])            
            dico[i["id"]]["data"]["count"]=dico[i["id"]]["data"]["self_count"]
#initialize count with only self_count peptide
        else:                 
            listseq=list(i["data"]["sequences"])            
            for seq in listseq:
                dico[i["id"]]["data"]["sequences"].add(seq)
            for kid in i["kids"]:
                dico[i["id"]]["kids"].add(kid)            
            dico[i["id"]]["data"]["self_count"]=len(dico[i["id"]]["data"]["sequences"])            
            dico[i["id"]]["data"]["count"]=dico[i["id"]]["data"]["self_count"]
        if len(dico[i["id"]]["kids"]):
#recursive method which allows to search all child of each parents                
            dico=recursparser(i,dico)
            tot=0
        
        for k in dico[i["id"]]["kids"]:
            dico[i["id"]]["data"]["count"]+=dico[k]["data"]["count"]
#incremente peptides count with the count of all kids , for non parents count is self_count and for parent is the sum of first generation child count            
                     
    return dico

#the function that allow to generate a d3_hierarchy format string with a recursive method
def jsoncreator(dico,dicopos,jsonout):
    
    dico[dicopos]["data"]["sequences"]=list(dico[dicopos]["data"]["sequences"])
    jsonout+='{"data": '+str(dico[dicopos]["data"]).replace("'",'"')
    jsonout+=',"kids": '+str(list(dico[dicopos]["kids"]))
    jsonout+=', "children": ['
    
    for k in dico[dicopos]["kids"]:
        if k==list(dico[dicopos]["kids"])[len(dico[dicopos]["kids"])-1]:
            jsonout=jsoncreator(dico,k,jsonout)
        else:
            jsonout=jsoncreator(dico,k,jsonout)+","
    jsonout+='], "id": '+str(dicopos)+', "name" : "'+dico[dicopos]["name"]+'"}'

    return jsonout    


if len(sys.argv) >2:
    with open(sys.argv[1]) as data_file:    
        data = json.load(data_file)
    
    dico={}
    dico[data["id"]]={}
    dico[data["id"]]["name"]=data["name"]
    dico[data["id"]]["data"]=data["data"]
    dico[data["id"]]["kids"]=set(data["kids"])
    dico=recursparser(data,dico)

    
    for arg in sys.argv[2:]:
        with open(arg) as data_file:    
            data2 = json.load(data_file)
        
        for kid in data2["kids"]:
            dico[1]["kids"].add(kid)
        dico=recursparser(data2,dico)
        dico[1]["data"]["count"]=dico[1]["data"]["self_count"]
        for k in dico[1]["kids"]:
            dico[1]["data"]["count"]+=dico[k]["data"]["count"]
    
    jsonstr=""
    print(jsoncreator(dico,1,jsonstr))

        
else :
    print ("Argument is needed")
