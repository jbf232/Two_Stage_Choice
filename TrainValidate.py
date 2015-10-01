from LikelihoodFunctions import *
import matplotlib.pyplot as plt
import numpy as np
from AssortmentOpt import *

numProds=5
lengthPrefLists=2
T=250
T_trainList=[20,30,40,50,60,70,80,90,100, 110,120,130,140,150]
numTrials=50

nonParamTestList=[]
twoStageTestList=[]

nonParamRevList=[]
twoStageRevList=[]

for T_train in T_trainList:

	nonParamTest=[]
	twoStageTest=[]

	nonParamRev=0.0
	twoStageRev=0.0

	np.random.seed(500)
	for trial in range(numTrials):
		prefLists=GenerateTypes(numProds, lengthPrefLists)
		offerMatrix, purchaseMatrix = GenerateData(prefLists, numProds,T,trial)
		potentialArrivalList=GetPotentialArrivalList(T, offerMatrix, purchaseMatrix, prefLists, numProds)
		offerList, purchaseList = GetListSalesData(offerMatrix,purchaseMatrix,T, numProds)
		revList=[0]+[np.random.uniform(0,100) for i in range(numProds)]

		NonNegNonParam=[lambda x, j=i: x[j] for i in range(len(prefLists))]
		lamNonParam=fmin_cobyla(NonParametricLikelihood, [1.0/len(prefLists)]*len(prefLists), [constrSumLam] + NonNegNonParam,\
		args = (potentialArrivalList,0, T_train), consargs=(), rhoend=1e-7, iprint =1 , maxfun=10000, disp= None)


		NonNegTwoStage=[lambda x, j=i: x[j] for i in range(2*(numProds+1))]
		lamTwoStage=fmin_cobyla(TwoStageLikelihood, ([1.0/(numProds+1)]*(numProds+1))*2, [constrArrivalProbs, constrTransitionProbs]\
		 + NonNegTwoStage, args = (numProds, offerList, purchaseList, 0, T_train), consargs=(), rhoend=1e-7, iprint =1 ,\
		  maxfun=10000, disp= None)



		twoStageArrival=lamTwoStage[:numProds+1]
		twoStageTransition=lamTwoStage[numProds+1:]
		lamTwoStageConvert=convertNonParam(prefLists, twoStageArrival, twoStageTransition)

		


		nonParamOptAssort=NonParamIP(prefLists,lamNonParam, numProds, revList)
		twoStageOptAssort=NonParamIP(prefLists,lamTwoStageConvert, numProds, revList)


		nonParamRev+= NonParamRev(prefLists,revList,nonParamOptAssort)
		twoStageRev+= NonParamRev(prefLists,revList,twoStageOptAssort)



		nonParamTest+=[NonParametricLikelihood(lamNonParam, potentialArrivalList,T_trainList[-1],T)]

		twoStageTest+=[TwoStageLikelihood(lamTwoStage, numProds, offerList, purchaseList, T_trainList[-1],T)]

	nonParamTestList+=[np.mean(nonParamTest)]
	twoStageTestList+=[np.mean(twoStageTest)]

	nonParamRevList+=[nonParamRev/numTrials]
	twoStageRevList+=[twoStageRev/numTrials]


plt.plot(T_trainList,nonParamTestList, 'r-', T_trainList, twoStageTestList, 'b-')
plt.show()
plt.plot(T_trainList,nonParamRevList, 'r-', T_trainList, twoStageRevList, 'b-')
plt.show()


