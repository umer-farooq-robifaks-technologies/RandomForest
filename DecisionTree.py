import scipy.stats
from math import log2
import pandas as pd

fulldata = None
data=None

TargetClass=None
root=None
Alledges=[]
Test=None
WholeEntropy=None

class node:
    def __init__(self):
        self.label= None
        self.edges=[]
        self.edgeOperated=[]
        self.EdgeToWhichNode=[]
        self.nextnode=[]
        self.previouseNode=None
        self.Isleafnode=False
        
def AllExampleSame(datasChecksame):
   targetLabel=datasChecksame[TargetClass]
   myset = set(targetLabel)   
   
   if len(myset)==1:
       return myset.pop()
   else:
       return False
 
def AllAttributeEmpty():
   
   a=data.isnull().sum()
   a=a.tolist()    
   if sum(a)==(len(data)*(len(data.columns)-1)):
       return True

def MostCommonTargetValue():
    targetLabel=data[TargetClass]
    return targetLabel.value_counts()[:1].index.tolist()

def get_Entropy(filterddata, classtype, attributeType):
    
    if attributeType!=None:
        selection =  filterddata[classtype]==attributeType
        selection=filterddata[selection]
        
        selection_class=selection[TargetClass]
        selection_class=selection_class.value_counts().sort_index(ascending=True).tolist()
        entropy=0        
        total=sum(selection_class)
        
        
        
        li=[]
        for classes in selection_class:
            li.append(classes/total)
        
        #entropysa = scipy.stats.entropy(li, base=2)  # get entropy from counts
        
        for entropytemp in selection_class:
            entropy=entropy+(entropytemp/total)*log2(entropytemp/total)
    else:
        filterddata=filterddata[TargetClass]
        filterddata=filterddata.value_counts().sort_index(ascending=True).tolist()
        
        entropy=0
        total=sum(filterddata)
        
        for entropytemp in filterddata:
            entropy=entropy+(entropytemp/total)*log2(entropytemp/total)
    return -entropy    









import time

Allinfogains=[]
eachcolumn=[]
Allinfonamegain=[]
def Get_Max_Info_Gain(dataforGain):
    WholeEntropy=get_Entropy(dataforGain, TargetClass, None) 
    global eachcolumn
    infogain=0
    Allinfogains.clear()
    eachcolumn=''
    lenofWholeData=len(dataforGain)
    columns=dataforGain.columns
    for eachcolumn in columns:
      if eachcolumn!=TargetClass:
        eachcolumndata=dataforGain[eachcolumn].unique()
        for ecd in eachcolumndata:   
            selectionofspecificattributes =  dataforGain[eachcolumn]==ecd
            selectionofspecificattributes=dataforGain[selectionofspecificattributes]
            length=len(selectionofspecificattributes)
            
            infogain=infogain+(length/lenofWholeData)*get_Entropy(dataforGain, eachcolumn, ecd) #here could be dataforgain because we need to filter 
              
              
            
        infogain=WholeEntropy-infogain
        
        Allinfogains.append(infogain)
        Allinfonamegain.append([eachcolumn,infogain])
        infogain=0
      else:
          continue
    return columns[Allinfogains.index(max(Allinfogains))]


        




TrackNodeEdge=[]
temp=None
nodeedge=None
leafNodeLabel=None

def FilterDataset(node, edge):
    TrackNodeEdge.clear()
    global nodeedge
    tempData=data
    temp=node
    nodeedge=edge    
    
    if node.previouseNode!=None:
            
            while True:
                TrackNodeEdge.append([temp,nodeedge])
                
                if temp.previouseNode==None:
                    for darray in temp.EdgeToWhichNode:
                        if darray[1]==TrackNodeEdge[len(TrackNodeEdge)-1][0]:
                            nodeedge=darray[0]
                    TrackNodeEdge.append([temp,nodeedge])
                    TrackNodeEdge.reverse()
                    
                    for nodeedgeStructure in TrackNodeEdge:
                        dataselection =  tempData[nodeedgeStructure[0].label]==nodeedgeStructure[1]
                        dataselection=tempData[dataselection]
                        tempData=dataselection
                    if AllExampleSame(tempData)!=False:
                        leafNodeLabel=AllExampleSame(tempData)
                        
                        CreateNode(tempData,node, edge, leafNodeLabel)
                        break
                    else:
                        CreateNode(tempData,node, edge, None)
                        break
                        
                        
                        
                
                                
                for darray in temp.previouseNode.EdgeToWhichNode:
                    if darray[1]==TrackNodeEdge[len(TrackNodeEdge)-1][0]:
                        nodeedge=darray[0]

                temp=temp.previouseNode
                
    elif node.previouseNode==None:
            dataselection =  data[node.label]==edge
            dataselection=data[dataselection]
            if AllExampleSame(dataselection)!=False:
                        leafNodeLabel=AllExampleSame(dataselection)
                        CreateNode(dataselection,node, edge, leafNodeLabel)
            else:
                        CreateNode(dataselection,node, edge, None)
                    
            
            
    TrackNodeEdge.clear()


    

    


def CreateNode(tailoreddata,previouseNode,LeadingEdge, leafNodeLabel):
    tempnode=node()   #the column having highest info gain is placed on the node.
    
    if leafNodeLabel==None:    
        tempnode.label=Get_Max_Info_Gain(tailoreddata)
        tempnode.edges=tailoreddata[tempnode.label].unique()
        for nodeedge in tempnode.edges:     
            Alledges.append([tempnode,nodeedge])    
            
    else:
        
        tempnode.label=leafNodeLabel
        tempnode.Isleafnode=True
        
        
    previouseNode.nextnode.append(tempnode)
    tempnode.previouseNode=previouseNode
    previouseNode.EdgeToWhichNode.append([LeadingEdge,tempnode])




            
        
def Operate(data):
    global root
    while True:
        if root==None:   #clear
            root=node()   #the column having highest info gain is placed on the node.
            root.label=Get_Max_Info_Gain(data)
            
            root.edges=data[root.label].unique()
            root.previouseNode=None
            for nodeedge in root.edges:     
                Alledges.append([root,nodeedge])    
        else:   
              if Alledges !=[]:  
                edgeNode=Alledges.pop()
                FilterDataset(edgeNode[0],edgeNode[1])
                
                edgeNode=None
              elif Alledges==[]:
                  print('Tree Ready')
                  break
                
def Testing(TestData, root):
    TempRoot=root
    Accurate_Prediction=0
    False_Prediction=0
    NumberOfTestCases=len(TestData)
    
    for index, row in TestData.iterrows():
        while TempRoot.Isleafnode==False:
            value=row[TempRoot.label]        
            for edgeToWhichNode in TempRoot.EdgeToWhichNode:
                if edgeToWhichNode[0]==value:                
                    TempRoot=edgeToWhichNode[1]
        if TempRoot.label==row[TargetClass]:
               Accurate_Prediction=Accurate_Prediction+1
        else:   
               False_Prediction=False_Prediction+1
        
        TempRoot=root    
    print(Accurate_Prediction, 'Accurate Predictions')
    print(False_Prediction, 'False Predictions')
       
    print((Accurate_Prediction/NumberOfTestCases)*100, 'Percent Accuracy')        
        

displayList=[]
displayParentNode=[]
def DisplayTree(root):
    TempNode=root
    displayList.append(TempNode.EdgeToWhichNode)
    displayParentNode.append(TempNode)    
    while displayList!=[] and displayParentNode!=[]:
        
        nodesAndEdge=displayList.pop()
        TempNode=displayParentNode.pop()
        print('Parent ',TempNode.label)
        for nte in nodesAndEdge:
            edge=nte[0]
            node=nte[1]
            
            print(edge, node.label)
            displayParentNode.append(node)
            displayList.append(node.EdgeToWhichNode)



def DecisionTree(Dataset, Targetclass, IrreleventClasses):
    global Train, Test, root, data, WholeEntropy, TargetClass
    data=Dataset
    
    for irreleventClass in IrreleventClasses:
        print(irreleventClass,' filtering ')
        
        try:
            data.drop(irreleventClass, inplace=True, axis=1)
        except:
            print('couldnt')    
    TargetClass=Targetclass
    WholeEntropy=get_Entropy(data,TargetClass, None)

    if AllExampleSame(data):
        root=node()
        root.label=AllExampleSame(data)
    elif AllAttributeEmpty():
        root=node()
        MostFrequent=MostCommonTargetValue()
        root.label=MostFrequent[0]  
    else:
        
        Operate(data)
    return root    
    

