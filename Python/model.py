#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
v1

Created on Mon Jun 22 09:42:22 2020
@author: Martin van der Schelling
more info: https://github.com/mpvanderschelling/BMC-optimizer
"""

#........... import packages ..................


#pip install -r bmc_requirements.txt

import skopt as sk
import numpy as np
import pandas as pd
from datetime import datetime
import os

import sklearn.utils._cython_blas
import sklearn.neighbors.typedefs
import sklearn.neighbors.quad_tree
import sklearn.tree
import sklearn.tree._utils
    
#.......................................

now = datetime.now()

# fiber_lb = 0.05
# fiber_ub = 0.20

# filler_lb = 0.0
# filler_ub = 1.0

# dry_lb = 0.40
# dry_ub = 0.75

# acq_func = 'EI'
# strategy = 'cl_min'
# max_recipes = 6
# total_mass = 2800.
# author = 'Martin van der Schelling'

def converttype(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return str(value)   

def parentdirpath(file,folder='files'):
    if not os.path.exists(os.path.join(os.getcwd(),os.pardir,folder)):
        os.mkdir(os.path.join(os.getcwd(),os.pardir,folder))
        print("[HOME]\t Created the folder '%s'" %folder)
        
    return os.path.join(os.getcwd(),os.pardir,folder,file)


#..............Startup and import ................


def startup():
    print("***************************************")
    print("****     BMC OPTIMIZATION MODEL    ****")
    print("***************************************")
    print(now.strftime("%B %d, %Y -- %H:%M"))
    print("Made by Martin van der Schelling")
    print("***************************************")
    print("\n")
    


def importconfig():
    global config
    config = []
    with open(parentdirpath('config.txt')) as f:
        for line in f:
            config.append(line)        
            
            if line == '\n':
                continue
            
            if line[0] == '#':
                continue
            
            if len(line.split()) == 1:
                print('[CONFIG] No value found for %s' %line.split())
                continue
            
      
            
            value = ' '.join(line.split()[1:])
              
            # convert value to the correct type      
            value = converttype(value)       
            globals()[line.split()[0]] = value #line.split()[1]
             
            
            print('[CONFIG]\t Load: %s = %s' %(line.split()[0],value))


def importobjective():
    global objective
    objective = []
    with open(parentdirpath('objective.txt')) as g:
        for line in g:
            if line[0] != '#':
                objective.append(line)
                print('[OBJECTIVE]\t Load: %s' %line.replace('\n',''))
            
        
#.............. Main module................

def home():
    
    print("[HOME]\t Type '?' for a list of available commands")
    
    while True:
        print("\n")
        
        query = input("[HOME]\t *** What would you like to do?: ")

        if query == 'exit':
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        
        if query =='?' or query == 'help':
            with open(parentdirpath('help.txt')) as h:
                for line in h:
                    print(line,end='')
                    
            #print('[HOME]\t Available commands: show <parameter>, set <parameter>, ask model, print, exit') 
        
        elif 'show' in query.split()[0]:
            show_query(query)
            
            
        elif 'set' in query.split()[0]:
            set_query(query)
        
        elif query == 'ask model':
            askmodel()
            
        elif query == 'print model':
            printrecipes()
            
        elif query == 'print scores':
            printscores()
            
        elif query == 'print config':
            printconfig()
        else:
            print("[HOME]\t '%s' is not a known command." %query)
            print("")           
            
       


#........... PRINT CONFIG .............

def printconfig():

    print("[PRINT]\t Do you want to overwrite the config file?")
    while True:
        ans = str(input("[PRINT]\t * Answer [y/n]: "))
        if ans not in ['y','n']:
            print("[PRINT]\t Please enter y or n")
        else:
            break
    
    if ans == 'y':
        with open(parentdirpath('config.txt','w+')) as f:
            for line in config:
                if line == '\n':
                    pass
                    
                elif line[0] == '#':
                    f.write(line)
                    continue
                    
                else:
                    f.write('%s %s'%(line.split()[0],str(globals()[line.split()[0]])))
                    
                f.write('\n')
                    
        print('[PRINT]\t Wrote the config.txt file!')
                          
    else:
        return

#........... PRINT SCORES .............

def printscores():
    if 'scores' not in globals():
        chooseoutput()
        if 'scores' not in globals():
            return
        
    print("[PRINT]\t Do you want to save the scores?")
    while True:
       ans = str(input("* Answer [y/n]: "))
       if ans not in ['y','n']:
            print("Please enter y or n")
       else:
           break
    
        
    if ans == 'y':
        while True:
            filename = str(input("[PRINT]\t Enter filename to save to (exclude type): "))
            break
        
        #OUTPUT TO CSV
        filename = filename + '.csv'
        scores.to_csv(parentdirpath(filename,folder='recipes'))
        print("[PRINT]\t Files saved as %s in the recipes folder" %filename) 

 #........... SHOW PARAMETERS .............  
    
def show_query(query):
    if len(query.split()) == 1:
        for line in config:
            if line == '\n':
                continue
            
            if line[0] == '#':
                continue
            
            print("[SHOW]\t %s = %s"%(line.split()[0], str(globals()[line.split()[0]])))
        return

    if query.split()[1] == 'data':
        if 'data' not in globals():
            opendatabase()
            if 'data' not in globals():
                return
        else:
            pass
        
    if query.split()[1] == 'config':
        for line in config:
            if line == '\n':
                continue
            
            if line[0] == '#':
                continue
            
            print("[SHOW]\t %s = %s"%(line.split()[0], str(globals()[line.split()[0]])))
        return
    
    
    
    if query.split()[1] == 'batch' and 'population' in globals():
        print('[SHOW]\t %s = %s' %('batch', str(globals()['population'])))
        return
        
    elif query.split()[1] in globals():
        param = query.split()[1]
        print('[SHOW]\t %s = %s' %(param, str(globals()[param])))
        
    else:
        print('[SHOW]\t %s is not a known parameter' %query.split()[1])

#........... SET PARAMETERS .............
        
def set_query(query):
    if query == 'set config':
        importconfig()
        return
    
    
    if len(query.split()) == 1:
        print('[SET]\t Please specify what you want to set')
        return    
    
    
    #other set functions
    
    if query.split()[1] == 'now':
        print('[SET]\t Changed now to %s !' %now)
        new_now = datetime.now()
        globals()['now'] = new_now
        return
    
    
    if query.split()[1] == 'data':
        opendatabase()
        return
    
    if query.split()[1] == 'materials':
        choosematerials()
        return
    
    if query.split()[1] == 'output':
        chooseoutput()
        return
    
    if query.split()[1] == 'batch':
        setpop()
        return
    
    #set functions for individual parameters
    
    
    if len(query.split()) < 3:
        print('[SET]\t Please specify a parameter and a value you want to set it')
        return
        
    elif query.split()[1] in globals():
        
        param = query.split()[1]
        old_value = globals()[param]
        new_value = ' '.join(query.split()[2:])
           
        #check if same type
        try:
            new_value = type(old_value)(new_value)

            # return   
         
        except ValueError:
            print('[SET]\t Types are not the same: expected %s but got %s' %(type(old_value),type(new_value[0])))
            return
        
        #check if other rules apply
        
        if query.split()[1] == 'max_recipes':
            if new_value < 0:
                print('[SET]\t max_recipes should not be a negative number!')
                return
        
        if query.split()[1] == 'total_mass':
            if new_value < 0:
                print('[SET]\t total_mass should not be a negative number!')
                return        
        
        if query.split()[1] == 'acq_func':
            if new_value not in ['LCB','EI','PI','gp_hedge','EIps','PIps']:
                print('[SET]\t acq_func should be LCB, EI, PI, gp_hedge, EIps or PIps!')
                return             

        if query.split()[1] == 'strategy':
            if new_value not in ['cl_min','cl_mean','cl_max']:
                print('[SET]\t strategy should be cl_min, cl_mean or cl_max!')
                return   
        
        globals()[param] = new_value
        print('[SET]\t Changed %s from %s to %s !' %(param,old_value,new_value))
        
        

        # if not, parameter is not known
    else:
        print('[SET]\t %s is not a known parameter' %query.split()[1])    
        
        
        
#........... SET DATA .............

def opendatabase():
    global data
    global databasename
    
    while True:
        text = str(input("[SET DATA]\t * Enter the name of the database: "))
        
        if text == 'exit':
            return
        
        
        try:
            data = pd.read_excel(parentdirpath(text),index_col=0)    
        except FileNotFoundError:
            print("[SET DATA]\t %s is not found" %text)
        else:
            databasename = text
            break

    print("[SET DATA]\t Found %d entries in database %s" %(len(data),databasename))       
    print("[SET DATA]\t Imported database %s as variable 'data'" %databasename)
 

#........... SET MATERIALS .........


def choosematerials():
    if 'data' not in globals():
        opendatabase()
        if 'data' not in globals():
            return
       
    global fiber_t
    global filler_t
    
    global d
    global x

    
    def materiallist(column):
        return list(set(data[column]))
    
    
    
    #fiber
    
    print("[SET MATERIALS]\t Choose a natural fiber to investigate")
    
    while True:
        fiber_t = str(input("[SET MATERIALS]\t * Enter the name of the natural fiber: "))
        if fiber_t in materiallist('type fiber'):
            break
        else:
            print("[SET MATERIALS]\t %s not present in the database!" %fiber_t)
            print("[SET MATERIALS]\t Fibers in database: %s "%' - '.join(materiallist('type fiber')))
    
    print("[SET MATERIALS]\t Selected %s as natural fiber" %fiber_t)
    
    #filler
    
    print("[SET MATERIALS]\t Choose a natural filler to investigate")
    
    while True:
        filler_t = str(input("[SET MATERIALS]\t * Enter the name of the natural filler: "))
        if filler_t in materiallist('type filler'):
            break
        else:
            print("[SET MATERIALS]\t %s not present in the database!" %filler_t)
            print("[SET MATERIALS]\t Fillers in database: %s" %' - '.join(materiallist('type filler')))
    
    print("[SET MATERIALS]\t Selected %s as filler" %filler_t)
    
    
    #select relevant data
    dd = data.loc[(data["type fiber"] == fiber_t) & (data["type filler"].isin([filler_t,'Calcite']))]
    
    dd =  dd.loc[dd['fiber ratio'].between(fiber_lb,fiber_ub,inclusive=True)]
    dd =  dd.loc[dd['filler ratio'].between(filler_lb,filler_ub,inclusive=True)]
    dd =  dd.loc[dd['dry ratio'].between(dry_lb,dry_ub,inclusive=True)]
    
    xx = np.atleast_2d(dd[["fiber ratio","filler ratio","dry ratio"]].to_numpy()).tolist()
    
    if len(xx) == 0:
        print('[SET MATERIALS]\t No entries found in the database that match your search boundaries!')
        print('[SET MATERIALS]\t Try to widen your search!')
        return
    
    d = dd
    x = xx
    
    #TODO do something if len(x) == 0    
    
    print("[SET MATERIALS]\t Found %d entries in database for %s with %s!" %(len(x),fiber_t,filler_t))

# #........... SET OUTPUT .........

def chooseoutput():
    if 'x' not in globals():
        choosematerials()
        if 'x' not in globals():
            return
    
    # outputcolumns = list(data.columns)[-5:] 
    
    outputcolumns = list(data.columns)
    for i in ['type fiber','type filler','fiber ratio','filler ratio','dry ratio','glycerol']:
        outputcolumns.remove(i)
    
    try:
        outputcolumns.remove('testable?')
    except ValueError:
        pass
    
    global fx
    global output
    global scores
    obj = []
    
    with open(parentdirpath('objective.txt')) as g:
        for line in g:
            if line[0] != '#':
                obj.append(line)
                
    #bias list
    biaslist = [i.split()[-1] for i in obj]
    biaslist = [1.0 if i in ['max','min'] else float(i) for i in biaslist ]
    bias = pd.Series(biaslist,index=outputcolumns)

    mm = pd.DataFrame(np.nan, columns=outputcolumns, index=d.index)
    
    for i in outputcolumns:
        for j in obj:
            if i in j:
                obj_beh = j.replace(i,'').replace('\n','')[1:]
                sign = obj_beh.split()[0]
                
                if sign == 'min':
                    mm[i] = ((d[i]-d[i].min())/(d[i].max()-d[i].min()))*bias[i]

                    
                if sign == 'max':
                    mm[i] = (abs(1-(d[i]-d[i].min())/(d[i].max()-d[i].min())))*bias[i]
                    
    if 'testable?' in list(data.columns):
        for i in list(mm.index):
            if d['testable?'][i] == 'no':
                mm.loc[i] = pd.Series((badplatepenalty*sum(bias))/len(outputcolumns), index=mm.columns) #huge penalty value
        
                    
    cumbias = pd.DataFrame([ [ bias.iloc[i]*mm.notna().iloc[j][i] for i in range(len(mm.iloc[0]))] for j in range(len(mm)) ],index=d.index).sum(axis=1)
    multi_obj = mm.sum(axis=1).divide(cumbias)
    
    
    print('[SET OUTPUT]\t Made single-objective output by rules of objective.txt')
    output = multi_obj
    print('[SET OUTPUT]\t name \t\t score')
    for i in range(len(output)):
        print('[SET OUTPUT]\t %s \t %s' %(output.index[i],output[i]) )

    scores = mm.div(cumbias,axis=0) #fillna()
    scores['testable?'] = d['testable?']
    scores['total scores'] = scores.sum(axis=1)
    fx = multi_obj.to_numpy().tolist()


# #........... SET BATCH ....................

def setpop():

    print("[SET BATCH]\t How many BMC doughs do you want to make?")
    
    global population
    
    while True:
        try:
            text = int(input("[SET BATCH]\t * Enter a number between 1 and 6: "))
        except ValueError:
            print("[SET BATCH]\tPlease enter an integer")
        else:
            if not 0 <= text < max_recipes:
                print("[SET BATCH]\t Please enter a number between 1 and 6")
            else:
                population = text
                break
    
    print("[SET BATCH]\t Setting %d as number of requested recipes from model .." %population)


    
# #........... ASK MODEL ............

def askmodel():

    
    #Ratio Fiber/Filler
    try:
        fiber_w = sk.space.Real(fiber_lb,fiber_ub, name='weightratio fiber')
        fillerA_w = sk.space.Real(filler_lb,filler_ub,name='weightratio natural filler') #if step=5, 21 options
        dry_w = sk.space.Real(dry_lb,dry_ub,name='ratio of dry material') #0.40,0.57
    except ValueError:
        print('[ASK MODEL]\t The boundaries of your model are not correctly set')
        return
    
    dim = [fiber_w, fillerA_w, dry_w]
    
    #........... INITIALIZE MODEL ...........
    
    opt = sk.Optimizer(dim,acq_func=acq_func)
    
    #........... TELL MODEL HISTORY ...........
    
    if 'fx' not in globals():
        chooseoutput()
        if 'fx' not in globals():
            return
        
    if 'population' not in globals():
        setpop()
        if 'population' not in globals():
            return    
                
    global xi
    
    #tell model history
    opt.tell(x,fx)
    
    print("[ASK MODEL]\t Succesfully build model on historical data")
    
    #........... ASK MODEL ....................
    
    
    #ask model
    xi = opt.ask(population,strategy=strategy)
    
    
    for i in range(population):
        print("[ASK MODEL]\t Recipe %d/%d : fiber: %.4f | filler: %.4f | dry: %.4f" %(i+1,population,xi[i][0],xi[i][1],xi[i][2]))




#........... PRINT MODEL ................


def printrecipes():
    
    def printcsv(filename):
        #--- Materials needed ---#
        
        # total_viscose = 0
        total_calcite = 0
        total_resin = 0
        total_fiber = 0
        total_filler = 0
        
        #--- Create batch ---#
        
        batch = []
        result = [] 
        
        for i in range(population):
            samplename = 'Recipe' + str(i+1)
        
         
            fiber_wx, fillerA_wx, dry_wx = xi[i]  
            resin_t = 'Polyester'
            
            #total_mass = _total_mass #3372. #grams
            
            fiber_m = fiber_wx* total_mass
            dry_m = dry_wx*total_mass   
        
            fillerA_m = (dry_wx-fiber_wx)*fillerA_wx * total_mass
            fillerB_m = (dry_wx-fiber_wx)*(1.-fillerA_wx) * total_mass
        
            premix_w = 1.-dry_wx #1.-dry_wx-glycerol_wx
            premix_m = premix_w * total_mass
            
            resin_w = premix_w*0.924099335
            resin_m = resin_w * total_mass
        
            trigonox_w = premix_w*0.013641133
            trigonox_m = trigonox_w * total_mass
            
            zincstearate_w = premix_w - resin_w - trigonox_w #premix_w * 0.062259532
            zincstearate_m = zincstearate_w * total_mass
               
            total_m = resin_m+trigonox_m+zincstearate_m+fiber_m+fillerA_m+fillerB_m #+glycerol_m
            
            result.append([zincstearate_m,trigonox_m, resin_m, fillerA_m, fillerB_m, fiber_m])
        
            #--- Pandas ---#
            
            recipe = pd.DataFrame({'Name':      [np.nan                     ,np.nan                                         ,samplename],
                                # 'units':      ['g'                        ,'%'                                            ,'name'],
                            'PE':               [round(resin_m)             ,round((resin_m/total_mass)*100,2)              ,resin_t],
                            'Trigonox':         [round(trigonox_m)          ,round((trigonox_m/total_mass)*100,2)           ,'Trigonox'],
                            'Zinc':             [round(zincstearate_m)      ,round((zincstearate_m/total_mass)*100,2)       ,'Zinc'],
                            'Nat. Filler':      [round(fillerA_m)           ,round((fillerA_m/total_mass)*100,2)            ,filler_t],
                            'Calcite':          [round(fillerB_m)           ,round((fillerB_m/total_mass)*100,2)            ,'Calcite'],
                            'Fiber':            [round(fiber_m)             ,round((fiber_m/total_mass)*100,2)              ,fiber_t],
                            'Total':            [round(total_m)             ,round((total_m/total_mass)*100,2)              ,np.nan],
                            ' ':                [np.nan                     ,np.nan                                         ,np.nan],
                            'Fiber %':          [np.nan                     ,round(fiber_wx*100,6)                          ,fiber_t],                    
                            'NF %':             [np.nan                     ,round(fillerA_wx*100,6)                        ,filler_t],               
                            'Dry %':            [np.nan                     ,round(dry_wx*100,6)                            ,np.nan]
        
        
                                },index=['g','%','name'])
            
            recipe = recipe.T
            
            #reindex columns
            recipe = recipe.reindex(columns=['%','g','name'])
            recipe = recipe.append(pd.Series(np.nan,name='   ',dtype=float))
            
            total_calcite += round(fillerB_m)
            total_resin += round(resin_m)
            total_fiber += round(fiber_m)
            total_filler += round(fillerA_m)
          
        
            batch.append(recipe)
         
            
        output = batch[0] 
        
        if population != 1:
            for i in range(1,population):
                output = pd.concat([output,batch[i]])
        
             
        #drop empty last column
        output = output.iloc[:,:-1]
        
                                 
        #add general information
        generalinfo = pd.DataFrame({'Stock C':  [np.nan,            str(total_calcite)                 ,'Calcite'],
                            'Stock NF ':        [np.nan,            str(total_filler)                  ,filler_t ],
                            'Stock F':          [np.nan,            str(total_fiber)                   ,fiber_t  ],
                            'Time':             [np.nan,            now.strftime("%B %d, %Y -- %H:%M") ,np.nan   ],
                            'Author':           [np.nan,            author         ,np.nan   ]
                                }).T
        
        generalinfo.columns = output.columns
        output = output.append(generalinfo)
        
        #OUTPUT TO CSV
        filename = filename + '.csv'
        output.to_csv(parentdirpath(filename,folder='recipes'))
        
    if 'xi' not in globals():
        askmodel()
        if 'xi' not in globals():
            return

    print("[PRINT]\t Do you want to save the %d proposed recipes?" %population)
    while True:
        ans = str(input("* Answer [y/n]: "))
        if ans not in ['y','n']:
            print("Please enter y or n")
        else:
            break
    
        
    if ans == 'y':
        while True:
            filename = str(input("[PRINT]\t Enter filename to save to (exclude type): "))
            break
        
        printcsv(filename)
        print("[PRINT]\t Files saved as %s.csv" %filename)




if __name__ == "__main__":
    startup()
    importconfig()
    importobjective()
    home()







