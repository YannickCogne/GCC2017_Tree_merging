#!/usr/local/bin/python

from optparse import OptionParser

import json


with open('../test_data/Chukchi_Sea.d3_hierarchy') as data_file2:    
    data = json.load(data_file2)


with open('../test_data/Bering_Strait.d3_hierarchy') as data_file:    
    data2 = json.load(data_file)

    
dico={}
dico[data["id"]]={}
dico[data["id"]]["name"]=data["name"]
dico[data["id"]]["data"]=data["data"]
dico[data["id"]]["kids"]=data["kids"]


def recursparser(data,dico):
    for i in data["children"]:
        
        if i["id"] not in dico.keys(): 
            dico[i["id"]]={}
             
            listseq=list(i["data"]["sequences"])
            dico[i["id"]]["name"]=i["name"]
            dico[i["id"]]["data"]=i["data"]
            dico[i["id"]]["data"]["sequences"]=set()
            for seq in listseq:
                
                dico[i["id"]]["data"]["sequences"].add(seq)
            dico[i["id"]]["kids"]=set(i["kids"])
            dico[i["id"]]["data"]["self_count"]=len(dico[i["id"]]["data"]["sequences"])            
            dico[i["id"]]["data"]["count"]=dico[i["id"]]["data"]["self_count"]


        else:
    
             
            listseq=list(i["data"]["sequences"])
            
            for seq in listseq:
                
                dico[i["id"]]["data"]["sequences"].add(seq)
            for kid in i["kids"]:
                dico[i["id"]]["kids"].add(kid)
            
            dico[i["id"]]["data"]["self_count"]=len(dico[i["id"]]["data"]["sequences"])            
            dico[i["id"]]["data"]["count"]=dico[i["id"]]["data"]["self_count"]



        if len(i["kids"]):
                
            dico=recursparser(i,dico)
            for k in i["kids"]:
                    
                dico[i["id"]]["data"]["count"]+=dico[k]["data"]["count"]
                    
                
                    
            
                     
    return dico
dico2=recursparser(data,dico)
print(dico2[1236])
dico3=recursparser(data2,dico2)
print (dico2[1236])
print (dico3 [33090])
print (dico3[4751])
def dicoreader(dico,childlist):
	for i in childlist:
            print (dico[i]["name"])
            print (dico[i]["data"]["count"])
            if len(dico[i]["kids"]):
                dicoreader(dico,dico[i]["kids"])

#def jsoncreator(dico):

print( '{"data": {"count": '+str(list(dico3[1236]["data"]["sequences"])).replace("'",'"'))

    


#str+=', "rank": "'++'", "valid_taxon": 1}, "kids":'++', "children": ['
#dicoreader(dico2,dico2[1]["kids"])

#print (len(dico))
#print (len(dico2))

