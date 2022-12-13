import numpy as np
from google.protobuf import text_format
import os
from matplotlib import pyplot as plt
import copy

from conf_proto import model_conf_pb2

class FirstOrderInertialElement(object):
    def __init__(self,path_root,T):
        self.root = path_root
        self.conf_file = self.root + "/conf/first_order_inertial_element.pb.txt"
        self.load_conf()
        self.T = T
        return

    def load_conf(self):
        self.model_conf = model_conf_pb2.FirstOrderInertialElementConf()
        f = open(self.conf_file,'rb')
        text_format.Parse(f.read(),self.model_conf)
        print("model_conf: ",self.model_conf)
        f.close() 

        self.X = np.array(self.model_conf.init_value)
        self.N = self.model_conf.N
        self.k = self.model_conf.k
        self.tau = self.model_conf.tau

        return
    
    def f(self,X_k,u):
        # f = dx = AX + Bu
        A = -1 / self.tau
        B = self.k / self.tau
        f = A * X_k + B * u
        return f
    
    def odeRK4(self,u):
        dt = self.T / self.N
        for i in np.arange(self.N):
            K1 = self.f(self.X,u)
            K2 = self.f(self.X+K1*dt/2,u)
            K3 = self.f(self.X+K2*dt/2,u)
            K4 = self.f(self.X+K3*dt,u)
            self.X += dt/6.0*(K1+2.0*K2+2.0*K3+K4)
        return

    def update(self,u):
        self.odeRK4(u)
        return
    
    def state(self):
        return self.X
    
    def test(self):
        x_list = []
        for i in np.arange(1000):
            self.update(1)
            X = self.state()
            x_list.append(copy.copy(X))
        
        plt.figure()
        plt.plot(x_list)
        plt.grid()
        return
    
def main(root):
    model = FirstOrderInertialElement(root,0.01)
    model.test()

    plt.show()

# if __name__ == '__main__':
#     main(".")