class space:
    remainlist=[] #class attribute
    wastelist=[] #class attribute
    
    def __init__(self,l1,w1,h1,l2,w2,h2): #to define each space it suffices to know the coordinates of two points of the space.
        self.L=l2-l1
        self.W=w2-w1
        self.H=h2-h1
        self.pos=(l1,w1,h1,l2,w2,h2)
        self.volume=self.L*self.W*self.H
        self.lowerBox_type=[]
        if self.L!=0 and self.W!=0 and self.H!=0:
            space.remainlist.append(self)
    
    def waste(self): #moves a space from remain list to waste list
        if self.L!=0 and self.W!=0 and self.H!=0:
            space.wastelist.append(self)
            if self in space.remainlist:
                del space.remainlist[space.remainlist.index(self)]
        
    def delet(self): #removes the space from both remain list and waste list
        if self in space.remainlist:
            del space.remainlist[space.remainlist.index(self)]
        elif self in space.wastelist:
            del space.wastelist[space.wastelist.index(self)]  
        else:
            print("Already deleted!!!!")  
        
    def merge(self): #merges the current space with neighbor spaces to obtain larger new space
        newspace=self
        #self is W and s in re by article notation
        spacelist=space.remainlist+space.wastelist
        spacelist.remove(self)
        
        #Case 3 parameters
        PSC3_a=[] #Possible Spaces for Case 3_a
        PSC3_b=[] #Possible Spaces for Case 3_b
        Iw2C3_a=0  # if Space w2 exist like the way defined in paper for case3 a
        Iw2C3_b=0   # if Space w2 exist like the way defined in paper for case3 b
        
        for s in spacelist:
            #check to see if the hights are the same
            if s.H==self.H and s.pos[2]==self.pos[2]: #to merge two space they should have same height
                ## First Case 
                if (s.pos[0]==self.pos[0] and s.L==self.L):
                    if (s.pos[4]==self.pos[1]): #check if the two spaces are neighbors
                        
                        newspace=self.__class__(s.pos[0],s.pos[1],s.pos[2],s.pos[3],self.pos[4],s.pos[5])
                        lowerBoxType=set( self.lowerBox_type + s.lowerBox_type )
                        lowerBoxType.discard(None)
                        if bool(lowerBoxType):
                            newspace.lowerBox_type=list(lowerBoxType)                      
                        s.delet()
                        self.delet()
                        return newspace
                    if (s.pos[1]==self.pos[4]): #check if the two spaces are neighbors
                        newspace=self.__class__(self.pos[0],self.pos[1],self.pos[2],self.pos[3],s.pos[4],self.pos[5])
                        lowerBoxType=set( self.lowerBox_type + s.lowerBox_type )
                        lowerBoxType.discard(None)
                        if bool(lowerBoxType):
                            newspace.lowerBox_type=list(lowerBoxType)                          
                        s.delet()
                        self.delet()
                        return newspace
                ## Case1-b        
                elif (s.pos[1]==self.pos[1] and s.W==self.W):
                    if (s.pos[3]==self.pos[0]):
                        newspace=self.__class__(s.pos[0],s.pos[1],s.pos[2],self.pos[3],s.pos[4],s.pos[5])
                        lowerBoxType=set( self.lowerBox_type + s.lowerBox_type )
                        lowerBoxType.discard(None)
                        if bool(lowerBoxType):
                            newspace.lowerBox_type=list(lowerBoxType)                          
                        s.delet()
                        self.delet()
                        return newspace
                    if (s.pos[0]==self.pos[3]):
                        newspace=self.__class__(self.pos[0],self.pos[1],self.pos[2],s.pos[3],self.pos[4],self.pos[5])
                        lowerBoxType=set( self.lowerBox_type + s.lowerBox_type )
                        lowerBoxType.discard(None)
                        if bool(lowerBoxType):
                            newspace.lowerBox_type=list(lowerBoxType)                          
                        s.delet()
                        self.delet()
                        return newspace
                        
                # Second Case 
                ##Case2-a   
                if self.pos[1]>=s.pos[1] and s.pos[3]==self.pos[0] and s.pos[4]>=self.pos[4]:
                    newspace=self.__class__(s.pos[0],self.pos[1],s.pos[2],self.pos[3],self.pos[4],s.pos[5])
                    lowerBoxType=set( self.lowerBox_type + s.lowerBox_type )
                    lowerBoxType.discard(None)
                    if bool(lowerBoxType):
                        newspace.lowerBox_type=list(lowerBoxType)                      
                    s.delet()
                    self.delet() 
                    newaste=self.__class__(s.pos[0],self.pos[4],s.pos[2],s.pos[3],s.pos[4],s.pos[5])
                    
                    newaste2=self.__class__(s.pos[0],s.pos[1],s.pos[2],s.pos[3],self.pos[1],s.pos[5])
                    
                    return newspace    
                ##Case2-b
                elif s.pos[0]>=self.pos[0] and self.pos[4]==s.pos[1] and self.pos[3]>=s.pos[3]:
                    newspace=self.__class__(s.pos[0],self.pos[1],s.pos[2],s.pos[3],s.pos[4],s.pos[5])
                    lowerBoxType=set( self.lowerBox_type + s.lowerBox_type )
                    lowerBoxType.discard(None)
                    if bool(lowerBoxType):
                        newspace.lowerBox_type=list(lowerBoxType)                      
                    s.delet()
                    self.delet()
                    newaste=self.__class__(s.pos[0],s.pos[1],s.pos[2],self.pos[0],s.pos[4],s.pos[5])
                    newaste2=self.__class__(self.pos[3],s.pos[1],s.pos[2],s.pos[3],s.pos[4],s.pos[5])
                    
                    return newspace
                                        
                #Third Case 
                ## Case 3_a                        
                # We collect all the spaces that adjacent to self in X && staring point of them in Y in before ending of Self
                if (s.pos[3]==self.pos[0]) and (s.pos[1]<=self.pos[4]): #colect potential for case 3-a
                    PSC3_a.append(s)
                    # Find the one that start as same Y as self started
                    if self.pos[1]==s.pos[1]: 
                        w2_a=s
                        Iw2C3_a=1
                ## Case 3_b    
                if (s.pos[4]==self.pos[1]) and (s.pos[0]<=self.pos[3]) : #colect potential for case 3-b
                    PSC3_b.append(s)
                    if self.pos[0]==s.pos[0]: 
                        w2_b=s
                        Iw2C3_b=1
                        
        ## Case 3_a (Contiued) 
                        
        for s in PSC3_a: # for all possible candidate spaces we found 
            if Iw2C3_a: # we need to have a space that start as the same Y self started
                # 
                if w2_a.pos[4]==s.pos[1] and w2_a.W+s.W>=self.W :
                    
                    if w2_a.pos[0]>=s.pos[0]:
                        newspace=self.__class__(w2_a.pos[0],self.pos[1],w2_a.pos[2],self.pos[3],self.pos[4],self.pos[5])
                        lowerBoxType=set( self.lowerBox_type + w2_a.lowerBox_type + s.lowerBox_type )
                        lowerBoxType.discard(None)
                        if bool(lowerBoxType):
                            newspace.lowerBox_type=list(lowerBoxType)                          
                        newaste=self.__class__(s.pos[0],s.pos[1],s.pos[2],w2_a.pos[0],s.pos[4],s.pos[5])
                        #newaste.waste()
                        w2_a.delet()
                        s.delet()
                        self.delet()

                    if w2_a.pos[0]<s.pos[0]:
                        newspace=self.__class__(s.pos[0],self.pos[1],w2_a.pos[2],self.pos[3],self.pos[4],self.pos[5])
                        lowerBoxType=set( self.lowerBox_type + w2_a.lowerBox_type + s.lowerBox_type )
                        lowerBoxType.discard(None)
                        if bool(lowerBoxType):
                            newspace.lowerBox_type=list(lowerBoxType)                         
                        
                        newaste=self.__class__(w2_a.pos[0],w2_a.pos[1],w2_a.pos[2],s.pos[0],w2_a.pos[4],w2_a.pos[5])
                        #newaste.waste()
                        w2_a.delet()
                        s.delet()
                        self.delet()
                        
                    return newspace
        ## Case 3_b (Contiued)  
        for s in PSC3_b:
            if Iw2C3_b:
                if w2_b.pos[3]==s.pos[0] and w2_b.L+s.L>=self.L :
                    
                    if w2_b.pos[4]>=s.pos[4]:
                        newspace=self.__class__(self.pos[0],self.pos[1],self.pos[2],self.pos[3],s.pos[4],self.pos[5])
                        lowerBoxType=set( self.lowerBox_type + w2_b.lowerBox_type + s.lowerBox_type )
                        lowerBoxType.discard(None)
                        if bool(lowerBoxType):
                            newspace.lowerBox_type=list(lowerBoxType)     
                        newaste=self.__class__(w2_b.pos[0],s.pos[4],w2_b.pos[2],w2_b.pos[3],w2_b.pos[4],w2_b.pos[5])
                        
                        #newaste.waste()
                        w2_b.delet()
                        s.delet()
                        self.delet()
                         
                    if w2_b.pos[4]<s.pos[4]:
                        newspace=self.__class__(self.pos[0],self.pos[1],self.pos[2],self.pos[3],w2_b.pos[4],self.pos[5])
                        lowerBoxType=set( self.lowerBox_type + w2_b.lowerBox_type + s.lowerBox_type )
                        lowerBoxType.discard(None)
                        if bool(lowerBoxType):
                            newspace.lowerBox_type=list(lowerBoxType)                         
                        newaste=self.__class__(s.pos[0],w2_b.pos[4],s.pos[2],s.pos[3],s.pos[4],s.pos[5])
                        #newaste.waste()
                        w2_b.delet()
                        s.delet()
                        self.delet()
                        
                    return newspace        
            
            
        '''if we reach to following line and wouldn't exsit the function 
                we will return newspace which is for sure equal to self.    
        '''        
        return newspace 
                   
    @classmethod     
    def curentspace(cls):
        volumes=[s.volume for s in cls.remainlist]
        minindx=volumes.index(min(volumes))            
        return cls.remainlist[minindx]
    @classmethod  
    def reset(cls):
        cls.remainlist=[]
        cls.wastelist=[]