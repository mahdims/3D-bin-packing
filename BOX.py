import numpy as np
from Blok import Blok #the best blok arrangement is determined in the methods of this class

class BOX: 
     AllBoxes=[]
     def __init__(self,Data,No): #build boxes as objects
         if No<=Data.ntype:
            self.dims=Data.boxes[No,(0,2,4)]
            self.l=self.dims[0]
            self.w=self.dims[1]
            self.h=self.dims[2]
            self.oriantation=Data.boxes[No,(1,3,5)]
            self.quantity=Data.boxes[No,6]
            self.weight=Data.boxes[No,7]
            self.type=No
            BOX.AllBoxes.append(self)
         else:
            exit("Try less box numbers")
        
     def Can_Load(self,Data,S):
         # check if the volume of one box in less than or equal to the current remianig space volume
        check=0
        if S.volume>= self.l*self.w*self.h :
            if S.lowerBox_type==[]:
                if sum(map(lambda x: x[0] , self.Possible_Oriatation(S) ))>=1:
                    check=1
            elif np.all(Data.Top_Bot[self.type,S.lowerBox_type]==1) :
                    # box should fit  in the space at least in one oriantation
                if sum(map(lambda x: x[0] , self.Possible_Oriatation(S) ))>=1:
                    check=1
        return check
        
     def Possible_Oriatation(self,S): 
         ori=[[0] for _ in range(6)]
         #Ori #1 y lenght x width
         #Ori #2 y lenght x hight
         if self.l <= S.W:
             if self.w <= S.L and self.h<=S.H and self.oriantation[2]==1:
                 ori[0]=[1,self.l,self.h,self.w] #(w,h,l)
                 
             if self.h <= S.L and self.w<=S.H and self.oriantation[1]==1:
                 ori[1]=[1,self.l,self.w,self.h]
        
         #Ori #3 y width x lenght
         #Ori #4 y width x hight
         if self.w <= S.W:
             
             if self.l <= S.L and self.h<=S.H and self.oriantation[2]==1:
                 ori[2]=[1,self.w,self.h,self.l]
                 
             if self.h <= S.L and self.l<=S.H and self.oriantation[0]==1:
                 ori[3]=[1,self.w,self.l,self.h]
         
         #Ori #5 y hight x lenght
         #Ori #6 y hight x width
         if self.h <= S.W:
             
             if self.l <= S.L and self.w<=S.H and self.oriantation[1]==1:
                 ori[4]=[1,self.h,self.w,self.l]
                 
             if self.w <= S.L and self.l<=S.H and self.oriantation[0]==1:
                 ori[5]=[1,self.h,self.l,self.w]
         
         return ori
         
     def Best_Blok(self,S):
        #Bvol=self.l*self.w*self.h
        #Kmax=int(S.volume/Bvol)
        Pori=self.Possible_Oriatation(S)
        f=[]  # Objective function
        B=[]  # All six bloks
        Ks=[] # Blok quantity
        for i,a in enumerate(Pori):
            if a[0]==1:
                Max_num_in_W=int(S.W/a[1])
                Max_num_in_H=int(S.H/a[2])
                Max_num_in_L=int(S.L/a[3])
                
                rows=int(self.quantity/Max_num_in_W)
                
                if rows==0:
                    
                    Ks.append(self.quantity)
                    B.append(Blok(a[1]*self.quantity,a[2],a[3],self.type,Ks[-1],i))
                elif 1<=rows<=Max_num_in_H:
                    
                    Ks.append(Max_num_in_W*rows)
                    B.append(Blok(a[1]*Max_num_in_W,a[2]*rows,a[3],self.type,Ks[-1],i))
                else:
                    columes=int(self.quantity/(Max_num_in_W*Max_num_in_H))
                    if columes<=Max_num_in_L:
                        
                        Ks.append(Max_num_in_W*Max_num_in_H*columes)
                        B.append(Blok(a[1]*Max_num_in_W,a[2]*Max_num_in_H,a[3]*columes,self.type,Ks[-1],i))
                    else:
                        
                        Ks.append(Max_num_in_W*Max_num_in_H*Max_num_in_L)
                        B.append(Blok(a[1]*Max_num_in_W,a[2]*Max_num_in_H,a[3]*Max_num_in_L,self.type,Ks[-1],i))
                f.append(S.volume-B[-1].volume)
        
        #rule 1
        minvol=min(f)
        if minvol==0: 
            bestblok=f.index(minvol)
            self.quantity-= Ks[bestblok]
            return  B[bestblok] 
            
        # rule 2
        for j,b in enumerate(B):
            if sum([S.L==b.L,S.W==b.W,S.H==b.H])==2:
                bestblok=j
                self.quantity-= Ks[bestblok]
                return  B[bestblok] 
       
        minimal_indecs=[i for i, x in enumerate(f) if x == minvol]
        if len(minimal_indecs)==1:
            # Rule 3 
            bestblok=minimal_indecs[0] 
            self.quantity-= Ks[bestblok]
            return  B[bestblok] 
            
        else:
            # Rule 4 select the one with maximum surface among minimal volume Bloks
            surface=[]
            for inx in minimal_indecs:
                surface.append(B[inx].L*B[inx].W)
            bestblok=minimal_indecs[surface.index(max(surface))]
            
            self.quantity-= Ks[bestblok]
            return  B[bestblok] 
                     
     @classmethod
     def reset(cls):
         cls.AllBoxes=[]
     @classmethod    
     def Is_unloaded_BOX(cls):
         check=0
         for box in cls.AllBoxes:
             if box.quantity!=0:
                 check=1
                 break
         return check      