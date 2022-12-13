import numpy as np
from google.protobuf import text_format
from matplotlib import pyplot as plt

from conf_proto import model_conf_pb2

class Stickband(object):

    def __init__(self,path_root,uv=0,u_pre=0,ur=0):
        self.root = path_root
        self.conf_file = self.root + "/conf/stickband.pb.txt"
        self.load_conf()
        self.u_pre = u_pre
        self.ur = ur
        self.u_v = uv
        return

    def load_conf(self):
        self.model_conf = model_conf_pb2.StickbandConf()
        f = open(self.conf_file,'rb')
        text_format.Parse(f.read(),self.model_conf)
        print("model_conf: ",self.model_conf)
        return

    def update(self,u):
        cum_u = self.ur + (u - self.u_pre)
        J = self.model_conf.J
        FD = self.model_conf.fd
        FS = J + FD
        if np.fabs(cum_u) > FS:
            self.u_v = u - np.sign(cum_u - FS) * FD
            self.ur = np.sign(cum_u - FS) * FS
        else:
            # self.u_v = self.u_v
            self.ur = cum_u
        
        # u_pre
        self.u_pre = u
        return
    
    def uv(self):
        return self.u_v

    def test(self):
        t_max = 10
        t_span = np.linspace(0,t_max,1000)
        u_span = np.array([np.sin(np.pi/2.0*t) for t in t_span])

        u_v_list = []
        for u in u_span:
            self.update(u)
            u_v_list.append(self.uv())

        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(t_span,u_span,label='u')
        plt.plot(t_span,np.array(u_v_list),label='uv')
        plt.grid()
        plt.legend()

        plt.subplot(2,1,2)
        plt.plot(u_span,np.array(u_v_list),label='u-uv')
        plt.grid()
        plt.legend()
        return

def main(root):
    model = Stickband(root)
    model.test()
    plt.show()

if __name__ == '__main__':
    main(".")