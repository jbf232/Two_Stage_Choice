from LikelihoodFunctions import *

numProds=10
lengthPrefLists=2
T=500
T_train=250
numTrials=10

nonParamTest=[]
twoStageTest=[]

for trial in range(numTrials):
	prefLists=GenerateTypes(numProds, lengthPrefLists)
	offerMatrix, purchaseMatrix = GenerateData(prefLists, numProds,T)
	potentialArrivalList=GetPotentialArrivalList(T, offerMatrix, purchaseMatrix, prefLists, numProds)
	offerList, purchaseList = GetListSalesData(offerMatrix,purchaseMatrix,T, numProds)






	NonNegNonParam=[lambda x, j=i: x[j] for i in range(len(prefLists))]
	lamNonParam=fmin_cobyla(NonParametricLikelihood, [1.0/len(prefLists)]*len(prefLists), [constrSumLam] + NonNegNonParam,\
	args = (potentialArrivalList,0, T_train), consargs=(), rhoend=1e-7, iprint =1 , maxfun=10000, disp= None)


	NonNegTwoStage=[lambda x, j=i: x[j] for i in range(2*(numProds+1))]
	lamTwoStage=fmin_cobyla(TwoStageLikelihood, ([1.0/(numProds+1)]*(numProds+1))*2, [constrArrivalProbs, constrTransitionProbs]\
	 + NonNegTwoStage, args = (numProds, offerList, purchaseList, 0, T_train), consargs=(), rhoend=1e-7, iprint =1 ,\
	  maxfun=10000, disp= None)



	nonParamTest+=[NonParametricLikelihood(lamNonParam, potentialArrivalList,T_train,T)]

	twoStageTest+=[TwoStageLikelihood(lamTwoStage, numProds, offerList, purchaseList, T_train,T)]

print "Non Param", np.mean(nonParamTest)

print "Two-Stage", np.mean(twoStageTest)