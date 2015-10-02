from GenerateNonparametric import FindPurchaseNonparametric


def CalcPurchaseProbsTwoStage(S, numProds, arrival, transition):

	purchaseProbsDict={}

	probNotOffered=sum([arrival[j] for j in range(1,numProds+1) if j not in S])
	

	for prod in S:

		purchaseProbsDict[prod]= arrival[prod] + probNotOffered*transition[prod]

	return purchaseProbsDict

def CalcPurchaseProbsNonParam(S, numProds, prefLists, lam):

	purchaseProbsDict={}
	

	for prod in S:

		custCount=0
		purchaseProb=0
		for cust in prefLists:

			purchase=FindPurchaseNonparametric(cust, S)

			if purchase==prod:
					 

				purchaseProb+=lam[custCount]

			custCount+=1
			
		purchaseProbsDict[prod]=purchaseProb

	return purchaseProbsDict
