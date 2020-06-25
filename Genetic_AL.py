from Solution import Solution
from input import Input
import math
import numpy as np
import numpy.random as numr
from random import shuffle
import time
import pandas as pd





class Chromo(Solution):
    
    Listofsolutions=[]
    pop=[]    
    @classmethod
    def reset(cls):
        cls.pop=[]
        cls.Listofsolutions=[]

    @classmethod    
    def initialpop(cls,Data,nPop,Varsize,crossover_rate,mutation_rate,mu):
        
        cls.nPop=nPop
        cls.Varsize=Varsize
        cls.crossover_rate=crossover_rate
        cls.mutation_rate=mutation_rate
        cls.mu=mu
        
       
        while len(cls.pop) < nPop:
            order=range(Varsize)
            shuffle( order )
            sol = cls( order )
            if order not in Chromo.Listofsolutions:
                Chromo.Listofsolutions.append(order)
                cls.pop.append(sol.Score_Calc(Data, alpha , beta , gamma))
    @classmethod
    def pop_sort(cls):
        pp=cls.pop
        pp=sorted(pp,key=lambda pp:pp[0],reverse=True)
        cls.pop=pp
        
    def mutation(self):
        gen2change=int(math.ceil(Chromo.mu*Chromo.Varsize))
        mutate=self
        for _ in range(gen2change):
            mutate=mutate.generate_children(1)[0][0]
        return Chromo(mutate.value)
        
    @classmethod    
    def crossover(cls, Dad_value, Mom_value):

        """partially mapped crossover"""
        child_Val_1=[]
        child_Val_2=[]
        
        (x,y)=np.random.choice(cls.Varsize,2,False)        
        if x > y: x,y = y,x

        dadParts = Dad_value[x:y+1]
        momParts = Mom_value[x:y+1]
        dadPartMap = dict(zip(dadParts, momParts))
        momPartMap = dict(zip(momParts, dadParts))
        # create the first child
        for i in xrange(x):
            while Dad_value[i] in momParts :
                Dad_value[i]=momPartMap[Dad_value[i]]
                
            child_Val_1.append(Dad_value[i])
            
        child_Val_1.extend(momParts)
            
        for j in xrange(y+1, cls.Varsize):
            while Dad_value[j] in momParts:
                Dad_value[j]=momPartMap[Dad_value[j]]
            child_Val_1.append(Dad_value[j])
            
        # create the second child
        for i in xrange(x):
            while Mom_value[i] in dadParts:
                Mom_value[i]=dadPartMap[Mom_value[i]]
                
            child_Val_2.append(Mom_value[i])
            
        child_Val_2.extend(dadParts)
    
        for j in xrange(y+1, cls.Varsize):
            while Mom_value[j] in dadParts:
                Mom_value[j]=dadPartMap[Mom_value[j]]
                
            child_Val_2.append(Mom_value[j])
            
            
        child1 = cls(child_Val_1)
        child2 = cls(child_Val_2)
        
        return (child1, child2)
        

    @classmethod 
    def evolve(cls,Data,TotalNoSolution):


        nPop=cls.nPop
        sp=1.8 # parameter in parents selection
        parents_length = int(nPop/1.5) # number of the parents
        pv=[]
        ############################# parents ################################
        # calculate the parents selection probablity
        for r,individual in enumerate(cls.pop):
            rank=float(nPop-r-1)
            pv.append(round((2-sp)/nPop+2*rank*(sp-1)/(nPop*(nPop-1)),5))
        pv = np.array(pv)    
        pv /= pv.sum()
        # selecting the parents 
        parents= roulette_wheel_pop(cls.pop, pv, parents_length)
        #################### mutate some individuals###########################
        Mutation_number=math.ceil(Chromo.mutation_rate*nPop)
        counter=1
        Mutants=[]
        Mut_inner_counter=0
        while counter<=Mutation_number and Mut_inner_counter<=20*Mutation_number:
            #Select the individual
            individual=parents[numr.randint(len(parents))]
            individual=individual.mutation()

            if individual.value not in Chromo.Listofsolutions:
                Chromo.Listofsolutions.append(individual.value)
                Mutants.append(individual)
                counter+=1
                Mut_inner_counter=0
            else:
                Mut_inner_counter+=1
            if len(Chromo.Listofsolutions)==TotalNoSolution:
                #sys.exit("We have all solutions already") 
                break
        ########################### crossover ##############################
        Crossover_number = int(Chromo.crossover_rate*nPop)
        crosscounter=0
        children = []
        while len(children) <= Crossover_number and crosscounter<=2*Crossover_number:
            crosscounter+=1
            
            (male,female)=np.random.choice(parents_length,2,False)
            
            (child1, child2)=cls.crossover( parents[male].value[:] , parents[female].value[:] )
      
            if child1.value not in cls.Listofsolutions : 
                cls.Listofsolutions.append(child1.value)
                children.append(child1)
                
            if child2.value not in cls.Listofsolutions :
                cls.Listofsolutions.append(child2.value)
                children.append(child2)
                
            if len(cls.Listofsolutions)==TotalNoSolution:
                    #sys.exit("We have all solutions already")
                break
               
       ###################################################################         
        children=[x.Score_Calc(Data,  alpha , beta , gamma) for x in children]
        Mutants=[x.Score_Calc(Data,  alpha , beta , gamma) for x in Mutants]
        
        # create the pool
        pool=cls.pop[:parents_length]
        pool.extend(children)
        pool.extend(Mutants)
        # evaluate the pool
        pool=sorted(pool,key=lambda pool:pool[0],reverse=True)
        # truncate the pool and create the new generation
        cls.pop=pool[0:nPop]
        
        return
  


def roulette_wheel_pop(pop, p, number):    
    chosen=np.random.choice(len(pop),number,False,p)
    chosen = [pop[a][1] for a in chosen]
    return chosen 
def Write2Excel(results):
    solution=pd.DataFrame(results, columns=['Box Type','Box Oriantation in Blok','Box quantity in Blok','Box priority','Blok Starting point','lenght','Width','Hight'])
    solution.to_excel('loading hurestic results (GA).xlsx')
    return    



def GA(Data):
    Varsize=Data.ntype 
    TotalNoSolution=math.factorial(Varsize)
    
    nPop=3*int(Varsize )  #Population Size 
    if nPop>=TotalNoSolution: nPop=TotalNoSolution
    MaxIt=80  # Maximum Number of Iterations
    Max_noimprove=25 # Maximum number of iterations without improvement before termination
    crossover_rate=0.7 # 
    mutation_rate=0.3 # Mutation Percentage
    mu=0.15  # Mutation Rate 
    
    start=time.time()
    
    iterationNO=1
    Chromo.initialpop(Data,nPop,Varsize,crossover_rate,mutation_rate,mu) # generate intial solution 
    Chromo.pop_sort() # 
    
    current_bestsol=Chromo.pop[0][1]
    noimprove=0
    while iterationNO<=MaxIt and noimprove<Max_noimprove and time.time()<=start+MaxRunTime and len(Chromo.Listofsolutions)<TotalNoSolution:
        Chromo.evolve(Data,TotalNoSolution)
        last_bestsol=current_bestsol
        current_bestsol=Chromo.pop[0][1]
        if current_bestsol.h_score==last_bestsol.h_score:
            noimprove+=1
        else: noimprove=0
        print("iteration%s" % iterationNO + "--#searched solutions= %s" % len(Chromo.Listofsolutions))
        print("Best objective: %s" %(current_bestsol.h_score) )
        
        iterationNO+=1
    
    return current_bestsol



times=[3,5,10,15,30,60]
filenumbers=[1,2,3,4,5,6,7]
instances=[2,10,15,22,33,45,52,63,78,84]
Final_results=np.zeros((6,7))
for t,T in enumerate(times):
    
    for f,FN in enumerate(filenumbers):

        VU=[]
        
        for PN in instances:

            Data=Input(FN,PN)
            #Data.RandomData(40)
            MaxRunTime=T     
            Best_Sol=GA(Data)
            Chromo.reset()
            
        VU.append(Best_Sol.VU)    
        Final_results[t,f]=np.mean(VU)        
        
    
Runtime=time.time()-start
print('Volume Utilization = %f ' %current_bestsol.VU)
print('Wieght distrbution measure= %f' %current_bestsol.WCG)
print('Distance from back measure= %f where the maximum is %f' %(current_bestsol.DFF,Solution.max_DFF()))
print('Run Time = %f sec' %Runtime)
print('Total number of loaded boxes = %f' %current_bestsol.Total_Box_Number(Data))
print('Total Box volume = %f Container volume = %f' % (sum(Data.boxes[:,7]*Data.boxes[:,6]),reduce(operator.mul,Data.contdim)) )
Write2Excel(current_bestsol.Loading_Results)