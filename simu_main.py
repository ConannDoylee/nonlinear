from matplotlib import pyplot as plt
import numpy as np

from simulation import Simulation
from deadband import Deadband
from deadzone import Deadzone
from stickband import Stickband
from first_order_inertial_element import FirstOrderInertialElement

test_group = [
    {
        "Deadzone": Deadzone('.'), 
    },
    {
        "Deadband": Deadband('.'),
    },
    {
        "Stickband": Stickband('.'),
    },
    {
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01)
    },
    {
        "Deadzone": Deadzone('.'), 
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01)

    },
    {
        "Deadband": Deadband('.'),
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01)
    },
    {
        "Stickband": Stickband('.'),
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01)
    },
    {
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01),
        "Deadzone": Deadzone('.'), 
    },
    {
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01),
        "Deadband": Deadband('.'),
    },
    {
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01),
        "Stickband": Stickband('.'),
    },
    {
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01),

    },
    {
        "Deadzone": Deadzone('.'), 
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01),
        "Deadband": Deadband('.'),
    },
    {
        "Deadzone": Deadzone('.'), 
        "Stickband": Stickband('.'),
        "FirstOrderInertialElement": FirstOrderInertialElement('.',0.01),
        "Deadband": Deadband('.'),
    },
]

simu_dict = {}
for i,dict in zip(np.arange(len(test_group)),test_group):
    simu_dict[i] = Simulation(dict)
    simu_dict[i].simulate()

plt.show()
