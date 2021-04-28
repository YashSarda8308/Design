import matplotlib.pyplot as plt
import numpy as np

class SSB:  #SImply Supported Beam
    Ma=0
    def __init__(self,length,forces):
        '''Please give forces from left to right with length in metre and force in N'''
        self.length = length
        self.forces = forces
    Fall = 0
    ra,rb = 0,0
    def param(self):
        global Fall,ra,rb
        print(self.forces.keys())
        Fall = sum(self.forces.keys())
        for k,v in self.forces.items():
            SSB.Ma += (k*v)
        return SSB.Ma, Fall
    def calculate_reaction(self):
        global Fall,ra,rb
        self.param()
        rb = SSB.Ma/self.length
        ra = Fall - rb
        return ra,rb
    def draw_sfd(self):
        self.calculate_reaction()
        all_Forces = []
        all_moment = []
        for i in range(len(np.linspace(0,self.length,100))):
                       all_Forces.append((self.forces.keys(_)*self.forces(_) for _ in self.forces))
        plt.plot(all_Forces,len(all_Forces))
        plt.show()
