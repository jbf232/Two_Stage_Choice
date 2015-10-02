from LikelihoodFunctions import *
import matplotlib.pyplot as plt
import numpy as np
from AssortmentOpt import *
from TwoStageModel import CalcPurchaseProbsTwoStage, CalcPurchaseProbsNonParam
from GenerateNonparametric import *
from scipy.optimize import fmin_cobyla
from GenerateData import *

numProds=5
lengthPrefLists=2
T=500
T_trainList=[30,60, 60, 120, 250]
numTrials=50
numRevTrials=50
numGridPoints=200

nonParamTestList=[]
twoStageTestList=[]

nonParamRevList=[]
twoStageRevList=[]
optRevList=[]


for T_train in T_trainList:

	nonParamTest=[]
	twoStageTest=[]

	nonParamRev=0.0
	twoStageRev=0.0
	optRev=0.0

	#np.random.seed(1)
	for trial in range(numTrials):
		prefLists=GenerateTypes(numProds, lengthPrefLists)
		offerMatrix, purchaseMatrix = GenerateData(prefLists, numProds,T,trial)
		potentialArrivalList=GetPotentialArrivalList(T, offerMatrix, purchaseMatrix, prefLists, numProds)
		offerList, purchaseList = GetListSalesData(offerMatrix,purchaseMatrix,T, numProds)
		


		
		NonNegNonParam=[lambda x, j=i: x[j] for i in range(len(prefLists))]
		lamNonParam=fmin_cobyla(NonParametricLikelihood, [1.0/len(prefLists)]*len(prefLists), [constrSumLam] + NonNegNonParam,\
		args = (potentialArrivalList,0, T_train), consargs=(), rhoend=1e-7, iprint =1 , maxfun=10000, disp= None)


		NonNegTwoStage=[lambda x, j=i: x[j] for i in range(2*(numProds+1))]
		lamTwoStage=fmin_cobyla(TwoStageLikelihood, ([1.0/(numProds+1)]*(numProds+1))*2, [constrArrivalProbs, constrTransitionProbs]\
		 + NonNegTwoStage, args = (numProds, offerList, purchaseList, 0, T_train), consargs=(), rhoend=1e-7, iprint =1 ,\
		  maxfun=10000, disp= None)



		twoStageArrival=[] 
		for j in range(numProds+1): 
			if lamTwoStage[j]>0.00001:
				twoStageArrival+=[lamTwoStage[j]]
			else:
				twoStageArrival+=[0]


		twoStageTransition=[]
		for j in range(numProds+1):
			if lamTwoStage[numProds +1 +j]>0.00001:
				twoStageTransition+=[lamTwoStage[numProds +1 +j]]
			else:
				twoStageTransition+=[0]
		lamTwoStageConvert=convertNonParam(prefLists, twoStageArrival, twoStageTransition)





		for r in range(numRevTrials):

			revList=[0]+list(np.random.uniform(0,100,numProds))
			nonParamOptAssort=NonParamIP(prefLists,lamNonParam, numProds, revList)
			twoStageOptAssort=NonParamIP(prefLists,lamTwoStageConvert, numProds, revList)
			optAssort=NonParamIP(prefLists,[1.0/len(prefLists)]*len(prefLists), numProds, revList)
			#twoStageOptAssort=FindOptU(twoStageArrival,twoStageTransition, numProds, revList,numGridPoints)
		


			nonParamRev+= NonParamRev(prefLists,revList,nonParamOptAssort)/numRevTrials
			twoStageRev+= NonParamRev(prefLists,revList,twoStageOptAssort)/numRevTrials
			optRev+=NonParamRev(prefLists,revList,optAssort)/numRevTrials


		nonParamTest+=[NonParametricLikelihood(lamNonParam, potentialArrivalList,T_trainList[-1],T)]

		twoStageTest+=[TwoStageLikelihood(lamTwoStage, numProds, offerList, purchaseList, T_trainList[-1],T)]

	nonParamTestList+=[np.mean(nonParamTest)]
	twoStageTestList+=[np.mean(twoStageTest)]


	nonParamRevList+=[nonParamRev/numTrials]
	twoStageRevList+=[twoStageRev/numTrials]
	optRevList+=[optRev/numTrials]


plt.plot(T_trainList,nonParamTestList, 'r-', T_trainList, twoStageTestList, 'b-')
plt.title('Likelihoods')
plt.savefig('Likelihoods') 
plt.show()

plt.plot(T_trainList,nonParamRevList, 'r-', T_trainList, twoStageRevList, 'b-',T_trainList, optRevList, 'g-')
plt.title('Revenues')
plt.savefig('Revenues')
plt.show()


