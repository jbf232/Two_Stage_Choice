# from LikelihoodFunctions import GetPotentialArrivalList

def GenerateTypes(numProds, lengthPrefLists):

	"""Generates the full set of types
		numProds does not include the no purchase option
	"""

	if lengthPrefLists==1:

		return [[i] for i in range(1, numProds+1)]

	else:

		previousList=GenerateTypes(numProds, lengthPrefLists-1)
		newTypes=[]
		for prefList in previousList:
			for i in range(1,numProds+1):

				if i not in prefList:
					newType=prefList+[i]

					if newType not in previousList:
					
						newTypes+=[newType]
				
		return previousList + newTypes

def FindPurchaseNonparametric(arrivingType, offerList):

	

	for prod in arrivingType:

		if prod in offerList:

			return prod

	return 0







if __name__ == '__main__':

	print GenerateTypes(3, 3)
