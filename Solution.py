from numpy.random import choice
from space import space
from BOX import BOX
from Blok import Blok

class Solution:
    DisFromFront=[]
    def __init__(self, value ):
        self.value = value
        self.h_score = None
        self.VU=None
        self.WCG=None
        self.DFF=None
        self.Loading_Results=None
    
    def generate_children(self,Childern_No):
        children=[]
        for  _ in xrange(Childern_No):
            rep=choice(len(self.value),2,replace=False)
            rep.sort()
            children.append((Solution(self.value[:rep[0]]+[self.value[rep[1]]]
            +self.value[rep[0]+1:rep[1]]
            +[self.value[rep[0]]]+self.value[rep[1]+1:]),tuple(rep)))
        return children
    

    def Total_Box_Number(self,Data):
        self.loading(Data)
        TotalNumberBox=sum([a.quantity for a in Blok.AllBloks ])      
        return int(TotalNumberBox)
        
        
        
    def loading(self,Data):
    #### loading hurestic ###
        space.reset()
        BOX.reset()
        Blok.reset()
        (L,W,H)=Data.contdim
        S=space(0,0,0,L,W,H)
        BOXS=[]
        for j in self.value:
            BOXS.append(BOX(Data,j))
    
        while len(space.remainlist)!=0 or BOX.Is_unloaded_BOX():
            S=S.merge()
            j=0
            while(j<Data.ntype and len(space.remainlist)!=0):
                currentbox=BOXS[j]
                
                if (currentbox.quantity>0 and currentbox.Can_Load(Data,S)):
                    BBlok=currentbox.Best_Blok(S)
                    BBlok.partition(S)
                    if len(space.remainlist)!=0:
                        S=space.curentspace()
                        j=0
                    else:
                        break
                        
                    S=S.merge()
                    #j+=1
                else:
                    j+=1
                    
            S.waste()
            if len(space.remainlist)!=0:
                S=space.curentspace()
            else:
                break
            

    
    def Score_Calc(self, Data, alpha, beta, gamma ) :
        (L,W,H)=Data.contdim
        self.loading(Data)
        results=[]
        con_volume=L*W*H
        Utilized_volume=0
        CGX,CGY,CGZ = 0, 0, 0
        Totalweight=0
        DisX,Totalpriority=0,0
        Blok.blokweights(Data) # assign weights and priorities to Best Blockes
        for a in Blok.AllBloks:
            results.append((a.boxtype,a.boxori,a.quantity,a.priority,a.pos,a.L,a.W,a.H))
            Utilized_volume+=a.volume
            #Calculating the weight distrbution
            CGX += a.weight*(a.pos[0]+a.L/2)
            CGY += a.weight*(a.pos[1]+a.W/2)
            CGZ += a.weight*(a.pos[2]+a.H/2)
            Totalweight += a.weight
            #Calculating the distance from front
            DisX+=a.priority*(a.pos[0]+a.L/2)
            Totalpriority+=a.priority
            
        CGX=CGX/Totalweight
        CGY=CGY/Totalweight
        CGZ=CGZ/Totalweight
        He=Utilized_volume/(L*W)
        Dist=max(abs(CGX-L/2)/(L/2),abs(CGY-W/2)/(W/2),abs(CGZ-He/2)/(He/2))
        WCG=(1-Dist)*100
        #Calculating the Volume utilisation
        VU=(Utilized_volume/con_volume)*100
        # Calcualting the distance from front
        DisX=DisX/Totalpriority
        
        DFF=((DisX)/L)*100
        
        self.h_score=alpha*VU+beta*WCG+gamma*DFF
        self.Loading_Results=results
        self.VU=VU
        self.DFF=DFF
        self.WCG=WCG
        Solution.DisFromFront.append(self.DFF)
        return (self.h_score,self)
        
        
    @classmethod
    def max_DFF(cls):
        return max(cls.DisFromFront)