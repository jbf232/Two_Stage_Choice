from GenerateData import *
from GenerateNonparametric import *
from scipy.optimize import fmin_cobyla
import math

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

def constr1(x):

	return 1-sum(x)


def NonParametricLikelihood(x, potentialArrivalList,T):

	
	return -sum([math.log(sum([max(x[i],0.001) for i in potentialArrivalList[t]])) for t in range(T)])

if __name__ == '__main__':

	numProds=20
	lengthPrefLists=2
	T=1000
	
	offerMatrix, purchaseMatrix = GenerateData(numProds, lengthPrefLists,T)

	prefLists=GenerateTypes(numProds, lengthPrefLists)

	potentialArrivalList=GetPotentialArrivalList(T, offerMatrix, purchaseMatrix, prefLists, numProds)

	#print NonParametricLikelihood([1.0/len(prefLists)]*len(prefLists), potentialArrivalList,T)
	
	NonNeg=[lambda x, j=i: x[j] for i in range(len(prefLists))]
	lam=fmin_cobyla(NonParametricLikelihood, [1.0/len(prefLists)]*len(prefLists), [constr1] + NonNeg,\
	args = (potentialArrivalList,T), consargs=(), rhoend=1e-7, iprint =1 , maxfun=10000, disp= None)

	print sum(lam)

