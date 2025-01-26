#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:45:00 2021

@author: samira
"""
from helper.util import column1s,column
from helper.parse_network import get_nodes
import numpy as np

ETB = {} # {"A": {"A1": [2,3], "A3" = [3]}, "B" {"B1:[1,3]} ....}
placementTreeDict = {} # {("D", "A1"): (5,[2,3,4], steinerTree(5234)} show steiner tree to connect all D's with A1 -> problem: what about multiple recipient event types? what about single sink placements=
eventNodeDict =  {} # {0: ["B1", "A3", "E0"], 1: ["A1B2", "A1B3", "B1"]} which instances of events/projections are generated or sent to/via node x -> maybe reuse network dict, but atm used for other stuff


def initEventNodes(nodes,network):  #matrice: comlumn indices are node ids, row indices correspond to etbs, for a given etb use IndexEventNodes to get row ID for given ETB
    #Storign all nodes producing a given event type with a 1 in the corresponding list
    # Node generating event type A would have: [1,0,0,0,...]
    myEventNodes = []
    #Storing a dictionary with the event type and node id as key and the index in the myEventNodes type for the list.
    myIndexEventNodes = {}
    offset = 0
    index = 0 
    #For each primitve event
    for etype in nodes.keys():
        myetbs = []
        #each node producting the event type
        for node in nodes[etype]:

            #creating a list of zeros with the length of the network
            mylist = [0 for x in range(len(network.keys()))]
            #Adding a 1 at the position of the node producing the event
            mylist[node] = 1
            myEventNodes.append(mylist)
            myIndexEventNodes[etype+str(node)] = index
            index += 1
            myetbs.append(etype+str(node))
        myIndexEventNodes[etype] = myetbs
        #offset = index
    return(myEventNodes, myIndexEventNodes)

def getETBs(node,EventNodes,IndexEventNodes):


    mylist = column1s(column(EventNodes, node))       
    return [list(IndexEventNodes.keys())[list(IndexEventNodes.values()).index(x)] for x in mylist] # index from row id <-> etb

def getNodes(etb,EventNodes,IndexEventNodes):
    return column1s(EventNodes[IndexEventNodes[etb]])

def setEventNodes(node, etb,EventNodes,IndexEventNodes):
    EventNodes[IndexEventNodes[etb]][node] = 1
 
def unsetEventNodes(node, etb,EventNodes,IndexEventNodes):
    EventNodes[IndexEventNodes[etb]][node] = 0    
    
def addETB(etb, etype,EventNodes,IndexEventNodes,network):
    mylist = [0 for x in range(len(network.keys()))]
    EventNodes.append(mylist)
    index = len(EventNodes)-1
    IndexEventNodes[etb] = index
    if not etype in IndexEventNodes:
        IndexEventNodes[etype] = [etb]
    else:
        IndexEventNodes[etype].append(etb)
    
def SiSManageETBs(projection, node,IndexEventNodes,EventNodes,network):
    etbID = genericETB("", projection,node)[0]
    addETB(etbID, projection,EventNodes,IndexEventNodes,network)           
    setEventNodes(node, etbID,EventNodes,IndexEventNodes)       

def MSManageETBs(projection, parttype,nodes):
    etbIDs = genericETB(parttype, projection)
    for projectionETB in etbIDs:
             addETB(projectionETB, projection)             
    for i in range(len(nodes[parttype])):
        setEventNodes(nodes[parttype][i], etbIDs[i])          


def genericETB(partType, projection,node):
    ETBs = []   
    if len(partType) == 0 or partType not in projection.leafs():
        myID = ""
        for etype in projection.leafs():
            myID += etype
        ETBs.append(myID)
    else:
        for node in nodes[partType]:   
            myID = ""
            for etype in projection.leafs():
                myID += etype
                if etype == partType:
                    myID += str(node)
            ETBs.append(myID)
    return ETBs

def getNumETBs(projection,IndexEventNodes):
    num = 1
    for etype in projection.leafs():
        num *= len(IndexEventNodes[etype])
    return num

def NumETBsByKey(etb, projection,IndexEventNodes):
    instancedEvents = []
    index = 0
    if len(projection) == 1:
        return 1
    for i in range(1, len(etb)):       
        if not etb[i] in projection.leafs() and etb[index] in projection.leafs() and not etb[index] in instancedEvents:
            instancedEvents.append(etb[index])
        elif etb[i] in projection.leafs():
            index = i
    
    num = getNumETBs(projection)
    for etype in instancedEvents:
        num = num / len(IndexEventNodes[etype])
    return num

def getLongest(allPairs):
    avs  = []
    for i in allPairs:
        avs.append(np.average(i))
    return np.median(avs)
   
