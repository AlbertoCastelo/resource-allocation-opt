#!/usr/bin/python
#from mipcl_py.models.schedule import Schedule
from models import ResourceAllocation
import numpy as np
import csv
import json
import _pickle as pk

# time horizon for the scheduling problem (days)
T = 5
# number of resources
N = 200
# number of resource needs of resources
RN = 1000

def generate_data(filename='parameters', printParam=True):
    '''
    Generates random data to be used in the optimization
    :param printParam: boolean to whether print or not the parameters generated
           filename: name of the file where data is saved
    :return: parameters to be used in the optimization problem
    '''
    filename = 'inputData/' + filename
    parameters = dict()

    parameters['RN'] = RN
    parameters['N'] = N
    parameters['T'] = T

    # random choosing whether resource i meets hard constraints
    # to be assigned to task j
    feasibleInd = []
    for i in range(N):
        feasibleRes = []
        for j in range(RN):
            feasibleRes.append(np.random.choice([1, 0]))
        feasibleInd.append(feasibleRes)


    parameters['feasibleInd'] = feasibleInd

    parameters['weights'] = {"type": 0.5,
                             "role" : 0.5,
                             "location" : 0.5,
                             "utilization" : 10}

    # cost asset type
    costType = []
    for i in range(N):
        costRes = []
        for j in range(RN):
            costRes.append(np.random.choice([0, 1]))
        costType.append(costRes)

    # cost role
    costRole = []
    for i in range(N):
        costRes = []
        for j in range(RN):
            costRes.append(np.random.choice([0, 1, 2, 3]))
        costRole.append(costRes)

    # cost location
    costLocation = []
    for i in range(N):
        costRes = []
        for j in range(RN):
            costRes.append(np.random.choice([1, 0]))
        costLocation.append(costRes)


    parameters['cost'] = {"type": costType, "role" : costRole, "location" : costLocation}

    print("\nParameters")
    print(parameters)

    with open(filename+'.p', 'wb') as fp:
        pk.dump(parameters, fp)

    if printParam:
        printParameters(parameters)

    return parameters

def printParameters(parameters):
    '''
    Prints the parameters
    :param parameters:
    :return:
    '''
    print("\n\n\n**********************PARAMETERS*****************************")
    print("# of Resources: %d" %(parameters['N']))
    print("# of Requirements: %d" %(parameters['RN']))
    print("# of Scheduled days: %d" %(parameters['T']))

    print("\nFeasible combinations for Resources (rows) and Resource Needs (columns)")
    a = "  "
    for j in range((parameters['RN'])):
        a += " "+str(j)
    print(a)
    feasibleInd = parameters['feasibleInd']
    for i in range((parameters['N'])):
        a = str(i)+": "
        for j in range((parameters['RN'])):
            #print(feasibleInd[i][j])
            a += str(feasibleInd[i][j])+" "
        print(a)


    print("\nResource Type Parameters")
    print("Resource Type weighting factor: %0.2f" % (parameters["weights"]["type"]))
    print("Resource Type cost for Resources (rows) and Resource Needs (columns)")
    a = "  "
    for j in range((parameters['RN'])):
        a += " " + str(j)
    print(a)
    cost = parameters['cost']['type']
    for i in range((parameters['N'])):
        a = str(i) + ": "
        for j in range((parameters['RN'])):
            # print(feasibleInd[i][j])
            a += str(cost[i][j]) + " "
        print(a)

    print("\nResource Role Parameters")
    print("Resource Role weighting factor: %0.2f" % (parameters["weights"]["type"]))
    print("Resource Role cost for Resources (rows) and Resource Needs (columns)")
    a = "  "
    for j in range((parameters['RN'])):
        a += " " + str(j)
    print(a)
    cost = parameters['cost']['role']
    for i in range((parameters['N'])):
        a = str(i) + ": "
        for j in range((parameters['RN'])):
            # print(feasibleInd[i][j])
            a += str(cost[i][j]) + " "
        print(a)

    print("\nLocation Parameters")
    print("Location weighting factor: %0.2f" %(parameters["weights"]["location"]))
    print("Location cost of Resources (rows) and Resource Needs (columns)")
    a = "  "
    for j in range((parameters['RN'])):
        a += " " + str(j)
    print(a)
    cost = parameters['cost']['location']
    for i in range((parameters['N'])):
        a = str(i) + ": "
        for j in range((parameters['RN'])):
            # print(feasibleInd[i][j])
            a += str(cost[i][j]) + " "
        print(a)

def loadParameters(filename='parameters', printParam=True):
    '''
    :param printParam: whether to print or not the loaded parameters
           filename: name of the file
    :return: parameteres
    '''
    filename = 'inputData/' + filename
    with open(filename+'.p', 'rb') as fp:
        parameters = pk.load(fp)

    if printParam:
        printParameters(parameters)

    return parameters

def main():

    # generate simulation parameters
    # parameters = generate_data('example1', printParam=True)
    parameters = generate_data('example2', printParam=True)

    # load simulation parameters
    # parameters = loadParameters('example1', printParam=True)
    # parameters = loadParameters('example2', printParam=True)

    prob = ResourceAllocation(parameters)
    prob.model()
    
    # try to solve for 1 hour
    prob.optimize(True, 3600)
    
    # get the solution
    solution = prob.getSolution()

    # print the solution
    prob.printSolution()
    
    
    






main()

'''
resources = {
  # Type| Role | availability| continuity| colocated| proefficiency| ind_experience| retention_prospects
  0: [1, 2, ],
  1: [],
  2: [],
}

jobs = {
  0: [0,  4, 2, {0: 2, 1: 3}, ()],
  1: [0,  6, 1, {0: 1, 1: 4}, ()],
  2: [0,  5, 3, {0: 2, 1: 2}, ()],
  3: [3,  7, 1, {0: 2, 1: 1}, ()],
  4: [2,  8, 3, {0: 4, 1: 3}, ()],
  5: [6, 12, 2, {0: 3, 1: 4}, ()],
  6: [1, 10, 4, {0: 5, 1: 4}, ()],
  7: [2,  8, 2, {0: 4, 1: 2}, ()],
  8: [0,  9, 1, {0: 1, 1: 3}, ()],
  9: [5, 12, 3, {0: 5, 1: 5}, ()]
}

prob = Schedule("test1")
prob.model(jobs)
prob.optimize()
prob.printSolution()
'''