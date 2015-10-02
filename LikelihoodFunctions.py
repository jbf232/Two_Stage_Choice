# from GenerateData import *
from GenerateNonparametric import FindPurchaseNonparametric, GenerateTypes
# from scipy.optimize import fmin_cobyla
import math

#Get the set of customer classes that could have potentially arrived
def GetPotentialArrivalList(T, offerMatrix, purchaseMatrix, prefLists, numProds):

	potentialArrivalList=[]

	for t in range(T):

		potentialArrival=[]

		prefListNum=0
		for prefList in prefLists:

			offerList=[i for i in range(1,numProds+1) if offerMatrix[t,i]==1]
			truePurchase=[i for i in range(numProds+1) if purchaseMatrix[t,i]==1]
			purchase=FindPurchaseNonparametric(prefList, offerList)


			
			if truePurchase[0]==purchase:

				potentialArrival+=[prefListNum]

			prefListNum+=1

		
		potentialArrivalList+=[potentialArrival]


	return potentialArrivalList

def GetListSalesData(offerMatrix,purchaseMatrix,T, numProds):

	offerList=[]
	purchaseList=[]

	for t in range(T):

		offer=[i for i in range(1,numProds+1) if offerMatrix[t,i]==1]
		truePurchase=[i for i in range(numProds+1) if purchaseMatrix[t,i]==1]

		offerList+=[[0]+ offer]
		purchaseList+=[truePurchase[0]]

	return offerList, purchaseList

#lams sum to 1 for nonparam model
def constrSumLam(x):

	return 1-sum(x)

#Nonparametric likelihood
def NonParametricLikelihood(lam, potentialArrivalList,T_start,T_end):

	
	return -sum([math.log(max(sum([lam[i] for i in potentialArrivalList[t]]),0.0001)) for t in range(T_start,T_end)])

#Arrival Probs sum to 1 for nonparam model
def constrArrivalProbs(x):

	return 1-sum(x[:5+1])

#Tranitions sum to 1
def constrTransitionProbs(x):

	return 1-sum(x[5+1:])


def TwoStageLikelihood(x, numProds, offerList, purchaseList, T_start,T_end):

	
	return -sum([ math.log(max(0.00001,x[purchaseList[t]] + (1-sum([x[j] for j in offerList[t]]))*x[numProds + 1 + purchaseList[t]] )) for t in range(T_start,T_end)])

if __name__ == '__main__':

	numProds=5
	lengthPrefLists=2
	T=50

	prefLists=GenerateTypes(numProds, lengthPrefLists)
	
	offerMatrix, purchaseMatrix = GenerateData(prefLists, numProds,T)
	potentialArrivalList=GetPotentialArrivalList(T, offerMatrix, purchaseMatrix, prefLists, numProds)


	
	NonNegNonParam=[lambda x, j=i: x[j] for i in range(len(prefLists))]
	lamNonParam=fmin_cobyla(NonParametricLikelihood, [1.0/len(prefLists)]*len(prefLists), [constrSumLam] + NonNegNonParam,\
	args = (potentialArrivalList,T), consargs=(), rhoend=1e-7, iprint =1 , maxfun=10000, disp= None)

	offerList, purchaseList = GetListSalesData(offerMatrix,purchaseMatrix)



	NonNegTwoStage=[lambda x, j=i: x[j] for i in range(2*(numProds+1))]
	lamTwoStage=fmin_cobyla(TwoStageLikelihood, ([1.0/(numProds+1)]*(numProds+1))*2, [constrArrivalProbs, constrTransitionProbs]\
	 + NonNegTwoStage, args = (numProds, offerList, purchaseList, T), consargs=(), rhoend=1e-7, iprint =1 ,\
	  maxfun=10000, disp= None)

	print sum(lamTwoStage[:numProds+1]), sum(lamTwoStage[numProds+1:])

