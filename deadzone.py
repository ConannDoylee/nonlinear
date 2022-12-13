import numpy as np
from google.protobuf import text_format
from matplotlib import pyplot as plt

from conf_proto import model_conf_pb2

class Deadzone(object):

    def __init__(self,path_root):
        self.root = path_root
        self.conf_file = self.root + "/conf/deadzone.pb.txt"
        self.load_conf()
        return

    def load_conf(self):
        self.model_conf = model_conf_pb2.DeadzoneConf()
        f = open(self.conf_file,'rb')
        text_format.Parse(f.read(),self.model_conf)
        print("model_conf: ",self.model_conf)
        return

    def update(self,w):
        c_l = self.model_conf.c_l
        c_r = self.model_conf.c_r

        if w < c_l:
            self.y = w - c_l
        elif w > c_r:
            self.y = w - c_r
        else:
            self.y = 0
        return
    
    def yw(self):
        return self.y

    def test(self):
        t_max = 10
        t_span = np.linspace(0,t_max,1000)
        u_span = np.array([np.sin(np.pi/2.0*t) for t in t_span])

        u_v_list = []
        for u in u_span:
            self.update(u)
            u_v_list.append(self.yw())

        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(t_span,u_span,label='v')
        plt.plot(t_span,np.array(u_v_list),label='u')
        plt.grid()
        plt.legend()

        plt.subplot(2,1,2)
        plt.plot(u_span,np.array(u_v_list),label='v-u')
        plt.grid()
        plt.legend()
        return

def main(root):
    model = Deadzone(root)
    model.test()
    plt.show()

if __name__ == '__main__':
    main(".")

