from DecisionTree import DecisionTree, DisplayTree, Testing
import pandas as pd
from sklearn.model_selection import train_test_split
import random

def most_frequent(List): 
    counter = 0
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num 
  

random.randint(0,9)
Features=[]

TargetClass=input("Enter Name of Dataset File: ") 
Dataset = input("Enter Name of Dataset File: ") 

fulldata = pd.read_csv(Dataset)
fulldata.drop('animal_name', inplace=True, axis=1)
TrainingData,Test=train_test_split(fulldata, test_size=0.2, random_state=42)
fulldata=TrainingData
        
Columns=fulldata.columns

n=int(input('Please Enter Number of Decision Trees in Forest: '))
TreeRoots=[]
#for index, row in TestData.iterrows():
    
for i in range(n):
        DatatoUse=fulldata
        TrainingData,Test=train_test_split(DatatoUse, test_size=0.05, random_state=42)
        NumberOfFeatures=random.randint(0,len(Columns)-10)
        for selectingFeatures in range(NumberOfFeatures):
            column=Columns[random.randint(1,len(Columns)-2)]
            if column not in Features: 
                Features.append(Columns[random.randint(1,len(Columns)-2)])
        IrreleventClasses=set(Features)   
        
        print(IrreleventClasses)
        TreeRoots.append(DecisionTree(TrainingData, TargetClass, IrreleventClasses))
        Features.clear()
        IrreleventClasses.clear()
        
Result=[]
votingForEachRow=[]
Accurate_Prediction=0
False_Prediction=0

for index, row in Test.iterrows():
    for TempRoot in TreeRoots:
        
        while TempRoot.Isleafnode==False:
            value=row[TempRoot.label]    
            #print(value, TempRoot.label)
            for edgeToWhichNode in TempRoot.EdgeToWhichNode:
                print(edgeToWhichNode[0], value)
                if edgeToWhichNode[0]==value:
                    TempRoot=edgeToWhichNode[1]
        votingForEachRow.append(TempRoot)            
    if most_frequent(votingForEachRow)==row[TargetClass]:
               Accurate_Prediction=Accurate_Prediction+1
    else:   
               False_Prediction=False_Prediction+1
        
    votingForEachRow.clear()        
print(Accurate_Prediction, 'Accurate Predictions')
print(False_Prediction, 'False Predictions')
       
print((Accurate_Prediction/len(Test))*100, 'Percent Accuracy')        
        



    
