import numpy as np
from mipcl_py.mipshell.mipshell import *


class ResourceAllocation(Problem):
    """docstring for ResourceAllocation"""

    def __init__(self, parameters):
        Problem.__init__(self,"allocation")
        # self.arg = arg

        self.RN = parameters['RN']
        self.N = parameters['N']
        self.T = parameters['T']
        self.feasibleInd = parameters['feasibleInd']

        self.weights = parameters['weights']
        self.cost = parameters['cost']

    def model(self):
        # define optimization problem
        # VARIABLES
        # decision variables
        self.x = x = VarVector([self.N, self.RN, self.T], 'x', BIN)

        # CONSTRAINTS
        # C1: all requirements must have resources assigned to them
        for j in range(self.RN):
            for t in range(self.T):
                if self.N >= self.RN:
                    sum_(x[s][j][t] for s in range(self.N)) == 1
                else:
                    sum_(x[s][j][t] for s in range(self.N)) <= 1

        # C2: set to zero the variables when the combination i,j is not feasible
        for i in range(self.N):
            for j in range(self.RN):
                for t in range(self.T):
                    if not self.feasibleInd[i][j]:   # if this combination is not feasible
                        x[i][j][t] == 0

        # C3: 1 resource  can only be assigned to a requirement at the same time
        for i in range(self.N):
            for t in range(self.T):
                if self.N > self.RN:
                    sum_(x[i][s][t] for s in range(self.RN)) <= 1
                else:
                    sum_(x[i][s][t] for s in range(self.RN)) == 1

        # Objectives
        # type
        w = self.weights['type']
        c = self.cost['type']
        J_1 = sum_(w * c[i][j]*x[i][j][t] for i in range(self.N) for j in range(self.RN) for t in range(self.T))

        # role
        w = self.weights['role']
        c = self.cost['role']
        J_2 = sum_(w * c[i][j] * x[i][j][t] for i in range(self.N) for j in range(self.RN) for t in
                   range(self.T))

        # sum of all objectives
        #J = J_RES
        J = J_1 + J_2

        # minimize objective
        minimize(J)

    def getSolution(self):
        solution = None
        if self.is_infeasible:
            print("INFEASIBLE")
        if self.is_unbounded:
            print("UNBOUNDED")

        if self.is_solution is not None:
            if self.is_solution:
                print("A solution was obtain")
                if self.is_solutionOptimal:
                    print("     OPTIMAL")

                else:
                    print("     NOT OPTIMAL")
                solution = dict()
                solution['Objective'] = self.getObjVal()

                # value of decision variables
                solution['Variables'] = self.x


                print(solution)
                return solution
    def printSolution(self):

        print("\n\nSOLUTION\nAssignment of Resources (rows) to Resource Needs (columns)")
        a = "  "
        xLabel1 = " "
        xLabel2 = "  "
        for j in range((self.RN)):
            a += " " + str(j)
        for t in range(self.T):
            xLabel1 += a +"|"
            xLabel2 += "  t=" + str(t) + "  | "
        print(xLabel2)
        print("--------------------------------------------------------------")
        print(xLabel1)
        print("--------------------------------------------------------------")
        x = self.x
        for i in range((self.N)):
            a = str(i) + ":  "
            for t in range(self.T):
                for j in range((self.RN)):
                # print(feasibleInd[i][j])
                    a += str(int(self.x[i][j][t].val)) + " "
                a += " | "
            print(a)
            print("--------------------------------------------------------------")

