import numpy as np
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
class Input:

    def __init__(self,fileNo,ProblemNo):
        self.contdim=[]
        self.ntype=[]
        self.boxes=[]
     ## Obtain Data ####
        ifile=open(dir_path+'\Data\wtpack%d.txt' % fileNo, "rb")
        lines=ifile.readlines()
        self.ntype=int(lines[1].split()[0])
        lines=lines[ProblemNo*(self.ntype+2):(ProblemNo+1)*(self.ntype+2)]
        ifile.close()
    ### Convert strings to numbers ###
        self.contdim=lines[0].split()
        self.contdim=[int(a) for a in self.contdim]
        box=[]
        for line in lines[2:2+self.ntype]:
            box.append(line.split())
        box=np.array(box,dtype=float)[:,0:9]
        box[:,7]=box[:,0]*box[:,2]*box[:,4]
        box[:,8]=np.random.randint(10,size=(1,self.ntype))
        box=box[np.argsort(box[:,7]),:]
        self.boxes=box
        #del lines[0:2+self.ntype[0]]
   ##### generate the constraint     
        self.Top_Bot=np.ones((self.ntype,self.ntype ))
        inx1=np.random.randint(0,self.ntype , self.ntype)
        inx2=np.random.randint(0,self.ntype , self.ntype)
        self.Top_Bot[inx1,inx2]=0
    def RandomData(self,NO_Box_type,contdim=[587, 233, 220]):
        self.contdim=contdim
        self.ntype=NO_Box_type 
        box=np.zeros((self.ntype,9))
        for i in range (self.ntype):
            box[i,0]=np.random.randint(contdim[0]/15,contdim[0]/4.5) # lenght
            box[i,1]=np.random.randint(2)
            box[i,2]=np.random.randint(contdim[1]/15,contdim[1]/4.5) # width
            box[i,3]=np.random.randint(2)
            box[i,4]=np.random.randint(contdim[2]/15,contdim[2]/4.5) # hieght
            box[i,5]=np.random.randint(2)
            
            box[i,6]=np.random.randint(2,15) # quantity 
        
        box[:,7]=box[:,0]*box[:,2]*box[:,4]
        
        box[:,8]=np.random.randint(10,size=(1,self.ntype))
        box=box[np.argsort(box[:,7]),:]
        self.boxes=box
        self.Top_Bot=np.ones((self.ntype,self.ntype ))
        inx1=np.random.randint(0,self.ntype , self.ntype)
        inx2=np.random.randint(0,self.ntype , self.ntype)
        self.Top_Bot[inx1,inx2]=0
        
        