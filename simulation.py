import numpy as np
from google.protobuf import text_format
from matplotlib import pyplot as plt
import os
import copy

from deadband import Deadband
from deadzone import Deadzone
from stickband import Stickband
from first_order_inertial_element import FirstOrderInertialElement

class Simulation(object):

    def __init__(self,objs_dict):
        self.objs_dict = objs_dict
        self.u_list = []
        self.y_list = []
        return

    def update_obj(self,key,obj,u):
        y = 0
        if key == "Deadband":
            obj.update(u)
            y = obj.yw()
        elif key == "Deadzone":
            obj.update(u)
            y = obj.yw()
        elif key == "Stickband":
            obj.update(u)
            y = obj.uv()
        elif key == "FirstOrderInertialElement":
            obj.update(u)
            y = obj.state()
        else:
            print("key error")
            os._exit(0)

        return copy.copy(y)

    def plot_uy(self):
        title_str = '-->'
        for key in self.objs_dict:
            title_str += key + "-->"
        plt.figure()
        plt.subplot(2,1,1)
        plt.title(title_str)
        plt.plot(self.u_list,self.y_list,label='u-y')
        plt.grid()
        plt.legend()

        plt.subplot(2,1,2)
        plt.plot(self.u_list,label='u')
        plt.plot(self.y_list,label='y')
        plt.grid()
        plt.legend()

        # save png
        png_name = "_"
        for key in self.objs_dict:
            png_name += key + "_"
        png_name += '.png'
        figures_root = './figures'
        if not os.path.exists(figures_root):
            os.makedirs(figures_root)
        plt.savefig(figures_root+'/'+png_name)


    def simulate(self):
        # generate inputs signal
        dt = 0.01
        cycle = 1000
        t_span = np.array([dt*i for i in np.arange(cycle)])
        u_span = np.array([np.sin(np.pi/2.0*t) for t in t_span])

        # update
        for u in u_span:
            y = u
            for key in self.objs_dict:
                obj = self.objs_dict[key]
                y = self.update_obj(key,obj,y)
            self.u_list.append(u)
            self.y_list.append(y)

        self.plot_uy()

        return
    
def main():
    dict = {"Deadzone": Deadzone('.'), 
            "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01)}
    # dict = {"Deadzone": Deadzone('.')}
    # dict = {"FirstOrderInertialElement": FirstOrderInertialElement('.',0.01)}

    simu = Simulation(dict)
    simu.simulate()
    # plt.show()

# if __name__ == '__main__':
#     main()