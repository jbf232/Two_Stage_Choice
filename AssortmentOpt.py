from gurobipy import *
from GenerateNonparametric import *

def NonParamIP(prefLists,lam, numProds, revList):

	numTypes=len(prefLists)

	#Create the model
	m=Model("NonParamIP")

	x={}
	for i in range(1,numProds+1):
		firstChoiceTotal=sum([revList[i]*lam[g] for g in range(numTypes) if prefLists[g][0]==i])
		x[i]=m.addVar(0.0,1,-firstChoiceTotal,GRB.BINARY,"x_%d" %i)

	y={}
	for g in range(numTypes):
		if len(prefLists[g])>1:
			secondChoice=prefLists[g][1]
			y[g,secondChoice]=m.addVar(0.0,1,-lam[g]*revList[secondChoice],GRB.BINARY,"y_%d" %g)

	m.update()


	for g in range(numTypes):
		if len(prefLists[g])>1:
			first=prefLists[g][0]
			second=prefLists[g][1]
			m.addConstr(LinExpr([1,1],[x[first],y[g,second]]),GRB.LESS_EQUAL,1.0)
			m.addConstr(LinExpr([1,-1],[y[g,second],x[second]]),GRB.LESS_EQUAL,0)

	m.setParam( 'OutputFlag', False)
	m.optimize()

	

	optAssort=[]
	prodCount=1
	for v in m.getVars()[:numProds]:
		#print prodCount,v.X

		if v.X==1.0:
			optAssort+=[prodCount]
		prodCount+=1

	return optAssort

def convertNonParam(prefLists, twoStageArrival, twoStageTransition):

	lam=[]

	for pref in prefLists:
		first=pref[0]
		if len(pref)>1:
			second=pref[1]
			lam+=[twoStageArrival[first]*twoStageTransition[second]]
		else:
			lam+=[twoStageArrival[first]*twoStageTransition[0]]

	return lam

def NonParamRev(prefLists,revList, S):
	#Assume uniform arrival for now
	rev=0

	for pref in prefLists:
		purchase=FindPurchaseNonparametric(pref, S)
		rev+=revList[purchase]

	return rev








if __name__ == '__main__':

	prefLists=[[1],[2,1],[2],[1,2]]
	
	numProds=2


	print NonParamRev(prefLists,[0,10,20], [1])

