from LikelihoodFunctions import *
import matplotlib.pyplot as plt

numProds=5
lengthPrefLists=2
T=250
T_trainList=[20,30,40,50,60,70,80,90,100, 110,120,130,140,150]
numTrials=50

nonParamTestList=[]
twoStageTestList=[]

for T_train in T_trainList:

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



		nonParamTest+=[NonParametricLikelihood(lamNonParam, potentialArrivalList,T_trainList[-1],T)]

		twoStageTest+=[TwoStageLikelihood(lamTwoStage, numProds, offerList, purchaseList, T_trainList[-1],T)]

	nonParamTestList+=[np.mean(nonParamTest)]
	twoStageTestList+=[np.mean(twoStageTest)]


plt.plot(T_trainList,nonParamTestList, 'r-', T_trainList, twoStageTestList, 'b-')
plt.show()


