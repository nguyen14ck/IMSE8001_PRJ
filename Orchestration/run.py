
import configparser #parse configruation file
import platform

import sqlite3 as sql #work with SQLite database
import os
import random #generate data

import pyutilib.workflow #for workflow
import subprocess #run Rscript.exe
from gurobipy import * #run Gurobi solver
import timeit #record running time



from Optimization_model import *
from Database_tasks import *


# @:class#######################################################################
class TaskA(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('file_name')
        self.outputs.declare('database_name')

    def execute(self):
        #CREATE OR OPEN DATABASE
        print self.file_name
        self.database_name = generate_db(self.file_name)

        #READ CONFIGURATION FILE
        config = configparser.ConfigParser()
        config.read('config\config.ini')
        program = config['Orchestration']['R']
        argument = config['Orchestration']['Script']



# @class:

# @:class#######################################################################
class TaskD(pyutilib.workflow.Task):

    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('B_completed')
        self.outputs.declare('result_D')

    def execute(self):
        if (self.B_completed == True):
            config = configparser.ConfigParser()
            config.read('config\config.ini')

            program = config['Orchestration']['R']
            argument = config['Orchestration']['Script']

            subprocess.call([program, argument])
            print "\n***********************************"
            print('############# FINISH RUN R ################')
            print "***********************************"

            self.result_D = "R Scripts Succeeded"
        else:
            self.result_D = "Cannot receive result from B to continue"



# @:class


# @:class#######################################################################
class TaskB(pyutilib.workflow.Task):

    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self, *args, **kwds)
        self.inputs.declare('database_name')
        self.outputs.declare('B_completed')

    def execute(self):
        config = configparser.ConfigParser()
        config.read('config\config.ini')
        k = config['Orchestration']['iterations']
        k = int(k)

        for i in range(1,k+1):
            n,c,e,l = read_db(refresh_db(self.database_name))
            model_1 = mtztw(n,c,e,l)
            model_2 = mtz2tw(n,c,e,l)
            model_3 = tsptw2(n,c,e,l)
            print "\n***************mtztw Method********************",i,"/",k
            print('############# TRAVELING SALESMAN PROBLEM PROBLEM WITH TIME WINDOWS ################')
            print "***************mtztw Method********************"

            start_time = timeit.default_timer()
            model_1.optimize()
            stop_time = timeit.default_timer()
            print "START TIME = ", start_time
            print "STOP TIME = ", stop_time
            #run_time = (stop_time - start_time) #in second
            #run_time = model_1.params.timeLimit
            run_time = model_1.Runtime
            print "SOLVING TIME = ", run_time
            print "OPTIMAL VALUE =", model_1.ObjVal

            if(i==1):
                update_db(self.database_name,1,model_1.ObjVal,run_time,start_time,stop_time,new_table=True)
            else:
                update_db(self.database_name,1,model_1.ObjVal,run_time,start_time,stop_time,new_table=False)

            print "\n***************mtz2tw Method********************",i,"/",k
            print('############# TRAVELING SALESMAN PROBLEM PROBLEM WITH TIME WINDOWS ################')
            print "***************mtz2tw Method********************"


            start_time = timeit.default_timer()
            model_2.optimize()
            stop_time = timeit.default_timer()
            print "START TIME = ", start_time
            print "STOP TIME = ", stop_time
            #run_time = (stop_time - start_time) #in second
            #run_time = model_2.params.timeLimit
            run_time = model_2.Runtime
            print "SOLVING TIME = ", run_time
            print "OPTIMAL VALUE =", model_2.ObjVal


            update_db(self.database_name,2,model_2.ObjVal,run_time,start_time,stop_time,new_table=False)

            print "\n***************tsp2tw Method********************",i,"/",k
            print('############# TRAVELING SALESMAN PROBLEM PROBLEM WITH TIME WINDOWS ################')
            print "***************tsptw2 Method********************"


            start_time = timeit.default_timer()
            model_3.optimize()
            stop_time = timeit.default_timer()
            print "START TIME = ", start_time
            print "STOP TIME = ", stop_time
            #run_time = (stop_time - start_time) #mili second
            #run_time = model_3.params.timeLimit
            run_time = model_3.Runtime
            print "SOLVING TIME = ", run_time
            print "OPTIMAL VALUE =", model_3.ObjVal



            update_db(self.database_name,3,model_3.ObjVal,run_time,start_time,stop_time,new_table=False)

        self.B_completed = True



# @:class
#####################################################

def main():

    # @usage:

    A = TaskA()
    B = TaskB()
    D = TaskD()
    B.inputs.database_name = A.outputs.database_name
    D.inputs.B_completed = B.outputs.B_completed

    w = pyutilib.workflow.Workflow()
    w.add(A)
    w.add(B)
    w.add(D)


    config = configparser.ConfigParser()
    config.read('config\config.ini')
    data_file = config['Orchestration']['database']
    print(w(file_name=data_file))

if __name__ == '__main__':
    main()

# @:usage