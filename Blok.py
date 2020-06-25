from space import space

class Blok:
    AllBloks=[] #class attribute (we need to store the loaded blocks)
    def __init__(self,w,h,l,boxtype,quantity,orientation): #creates blocks
        self.L=l            
        self.W=w
        self.H=h
        self.volume=self.L*self.W*self.H
        self.boxtype=boxtype
        self.boxori=orientation
        self.pos=[]
        self.quantity=quantity
        self.weight=[]
        self.priority=[]    
  
    def partition(self,S):
        # According to Figure a in the article
        # Front space 
        self.pos=[S.pos[0],S.pos[4]-self.W,S.pos[2]]
        fl2=S.pos[0]+self.L
        fw2=S.pos[4]-self.W
        Front_space=space(S.pos[0],S.pos[1],S.pos[2],fl2,fw2,S.pos[5])
        # Upper sapce 
        ul2=self.L+S.pos[0]
        uw1=S.pos[4]-self.W
        uh1=self.H+S.pos[2]
        Upper_space=space(S.pos[0],uw1,uh1,ul2,S.pos[4],S.pos[5])
        Upper_space.lowerBox_type=[self.boxtype]
        # Right space 
        rl1=S.pos[0]+self.L
        Right_space=space(rl1,S.pos[1],S.pos[2],S.pos[3],S.pos[4],S.pos[5])
        # delete the initial space
        S.delet()
        Blok.AllBloks.append(self) 
        return 
    
    @classmethod 
    def reset(cls):
        cls.AllBloks=[]
    @classmethod    
    def blokweights(cls,Data):
        maxpri=max(Data.boxes[:,8])
        for a in cls.AllBloks:
            a.weight=a.quantity*Data.boxes[a.boxtype,7]
            a.priority=maxpri-Data.boxes[a.boxtype,8]
        