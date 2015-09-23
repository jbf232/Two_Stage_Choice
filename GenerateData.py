from GenerateNonparametric import *
import numpy as np
import random


def GenerateData(numProds, lengthPrefLists,T):
	seed=1000
	random.seed(seed)
	np.random.seed(seed)

	#Get the set of customer types aka their preference lists (assume uniform arrival probs)
	prefLists=GenerateTypes(numProds, lengthPrefLists)

	#Generate the Sales Data
	offerMatrix=np.zeros((T, numProds+1))
	purchaseMatrix=np.zeros((T, numProds+1))

	for t in range(T):

		arrivingType=random.sample(prefLists,1)[0]
		
		offerMatrix[t,0]=1
		offerList=[]
		for i in range(1, numProds+1):

			if np.random.uniform() > 0.5:

				offerMatrix[t,i]=1
				offerList+=[i]

		
		purchase=FindPurchaseNonparametric(arrivingType, offerList)
		
		
		purchaseMatrix[t, purchase]=1

	return offerMatrix, purchaseMatrix









if __name__ == '__main__':

	numProds=5
	lengthPrefLists=2
	T=10
	


	offerMatrix, purchaseMatrix = GenerateData(numProds, lengthPrefLists,T)
	print offerMatrix

