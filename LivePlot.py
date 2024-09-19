import odrive
from odrive.enums import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import sin, pi
import time
from multiprocessing import Process
import numpy as np

odrv0 = odrive.find_any()

fig, [ax_elec, ax_command, ax_i] = plt.subplots(3, 1, figsize=(6.4, 10))

# electrical & mechanical power
ax_elec.set_title("Elec & Meca power")
ax_meca = ax_elec.twinx()

# command & position
ax_command.set_title("Command & Position")
ax_pos = ax_command.twinx()

# current & voltage
ax_i.set_title("Current & Voltage")
ax_v = ax_i.twinx()

x = []

electrical_power = []
mechanical_power = []

command = []
pos = []

current = []
voltage = []


def animate(i):
    
    x.append(i)

    electrical_power.append(odrv0.axis0.controller.electrical_power)
    mechanical_power.append(odrv0.axis0.controller.mechanical_power)

    command.append(odrv0.axis0.controller.pos_setpoint)
    pos.append(odrv0.axis0.encoder.pos_estimate)

    current.append(odrv0.axis0.motor.I_bus)
    voltage.append(odrv0.vbus_voltage)
    
    if len(x) > 100:

        x.pop(0)

        electrical_power.pop(0)
        mechanical_power.pop(0)

        command.pop(0)
        pos.pop(0)

        current.pop(0)
        voltage.pop(0)

    ax_elec.clear()
    ax_meca.clear()

    ax_command.clear()
    ax_pos.clear()

    ax_i.clear()
    ax_v.clear()

    ax_elec.set_ylabel("Electrical Power (W)", color = 'b')
    ax_elec.plot(x, electrical_power, color='b')

    ax_meca.set_ylabel("Mechanical Power (W)", color='r')
    ax_meca.plot(x, mechanical_power, color='r')

    ax_command.set_ylabel("Command (turn)", color='r')
    ax_command.plot(x, command, color='r')

    ax_pos.set_ylabel("Pos (turn)", color='b')
    ax_pos.plot(x, pos, color='b')


    ax_i.set_ylabel("I (A)", color='r')
    ax_i.plot(x, current, color='r')

    ax_v.set_ylabel("U (V)", color='g')
    ax_v.plot(x, voltage, color='g')


if __name__=="__main__":
    ani = FuncAnimation(fig, animate, interval=50)

    plt.show()

