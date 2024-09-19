import serial
import time
import numpy as np
import pandas as pd
from math import pi
from tqdm import tqdm
from Record import velocity
import odrive


def init(com_status):
    odrv0 = serial.Serial("COM3")

    odrv0.write(b'sc\n')
    odrv0.write(b'w axis0.requested_state 8\n')

    time.sleep(.1)

    odrv0.write(bytes("p 0 {}\n".format(0), "utf-8"))

    time.sleep(.5)

    com_status.value=1
    print('Command started...')
    return odrv0


def sin_command(com_status=0):
    freq = 1 # frequency of the sin wave in Hz
    n_turn = 2 # number of turn
    resolution = 100 # commands per second
    amplitude = 2

    pos = amplitude*np.sin(np.linspace(0, n_turn*2*pi, int(n_turn/freq*resolution)))

    odrv0 = init(com_status)

    time.sleep(.5)

    for p in pos:
        odrv0.write(bytes("p 0 {}\n".format(p), "utf-8"))

        time.sleep(1/resolution)
    
    time.sleep(.5)

    com_status.value = 0


def increasing_frequency(com_status=0):

    odrv0 = init(com_status)

    freq_start = 0
    freq_end = 5
    increase_rate = .5
    resolution = 100
    amplitude = 5

    freq = 2*pi*np.linspace(freq_start, freq_end, int((freq_end-freq_start)*resolution/increase_rate))
    pos = amplitude*np.sin(freq*np.linspace(0, (freq_end-freq_start)/increase_rate, int((freq_end-freq_start)*resolution/increase_rate)))

    time.sleep(.5)

    for p in tqdm(pos):
        odrv0.write(bytes("p 0 {}\n".format(p), "utf-8"))

        time.sleep(1/resolution)
    
    time.sleep(.5)

    com_status.value = 0

def real_data(com_status=0):

    data = pd.read_csv('data/data_AC.csv')
    resolution = np.polyfit(range(data.index.size), data['Time'], 1)[0]
    pos = data['Position droite']

    # time correction (experimental value)
    t_sleep = resolution*0.946
    
    odrv0 = init(com_status)

    time.sleep(.5)

    for p in tqdm(pos):
        odrv0.write(bytes("p 0 {}\n".format((p-33)/10), "utf-8"))
        time.sleep(t_sleep)

    time.sleep(.5)

    com_status.value = 0

def step(com_status=0):

    # time correction (experimental value)
    
    odrv0 = init(com_status)

    time.sleep(1)

    odrv0.write(bytes("p 0 {}\n".format(0), "utf-8"))

    time.sleep(2)

    com_status.value = 0

if __name__ == '__main__':
    # Rodage avec sinus
    pos_max = 55
    pos_min = 0

    amplitude = (pos_max - pos_min) / 2
    pos_repos = pos_min + amplitude

    print(amplitude, pos_repos)

    freq_com = 60 # Hz (?)
    omega = 25 / amplitude

    print(omega)


    # init
    odrv0 = serial.Serial("COM3")
    odrv_mes = odrive.find_any()
    print('asking for motion')
    odrv0.write(b'sc\n')
    odrv0.write(b'w axis0.requested_state 8\n')
    odrv0.write(b'w axis1.requested_state 8\n')

    odrv0.write(b'w axis0.controller.config.input_mode 3\n')
    odrv0.write(b'w axis1.controller.config.input_mode 3\n')

    odrv0.write(b'r axis1.controller.config.input_mode\n')
    time.sleep(1)
    param = odrv0.read(1)

    print(param)

    if False:
        time.sleep(.1)
        print('return to 0')
        odrv0.write(bytes("p 0 {}\n".format(pos_repos), "utf-8"))
        odrv0.write(bytes("p 1 {}\n".format(pos_repos), "utf-8"))

        time.sleep(2)

        cnt = 0
        while cnt < 3 * freq_com / omega * 2 * np.pi:
            pos = pos_repos + amplitude * np.sin(cnt / freq_com * omega)
            odrv0.write(bytes("p 0 {}\n".format(pos), "utf-8"))
            odrv0.write(bytes("p 1 {}\n".format(pos), "utf-8"))
            time.sleep(1/freq_com) # ~100 Hz

            if cnt % 10 == 0:
                print("pos_com = {:.3f} | vel_mes = {:.3f}".format(pos, velocity(odrv_mes, 1)))

            cnt += 1

        odrv0.write(bytes("p 0 {}\n".format(pos_max - 5), "utf-8"))
        odrv0.write(bytes("p 1 {}\n".format(pos_max - 5), "utf-8"))

        time.sleep(5)

    odrv0.write(b'w axis0.requested_state 1\n')
    odrv0.write(b'w axis1.requested_state 1\n')
    
    odrv0.write(b'w axis0.controller.config.input_mode 1\n')
    odrv0.write(b'w axis0.controller.config.input_mode 1\n')

    print('Over')




