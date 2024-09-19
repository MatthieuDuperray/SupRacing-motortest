import csv
import odrive
import time
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pipe


def command(odrv0, motor = 0):
    if motor == 0:
        return odrv0.axis0.controller.pos_setpoint
    if motor == 1:
        return odrv0.axis0.controller.pos_setpoint

def position(odrv0):
    return odrv0.axis0.encoder.pos_estimate

def velocity(odrv0, motor = 0):
    match(motor):
        case 0:
            return odrv0.axis0.encoder.vel_estimate
        case 1:
            return odrv0.axis1.encoder.vel_estimate

def mechanical_power(odrv0):
    return odrv0.axis0.controller.mechanical_power

def elecctrical_power(odrv0):
    return odrv0.axis0.controller.electrical_power

def I_phA(odrv0):
    return odrv0.axis0.motor.current_meas_phA

def I_phB(odrv0):
    return odrv0.axis0.motor.current_meas_phA

def I_phC(odrv0):
    return odrv0.axis0.motor.current_meas_phA

def I_bus(odrv0):
    return odrv0.axis0.motor.I_bus

def input_torque(odrv0):
    return odrv0.axis0.controller.input_torque

def input_vel(odrv0):
    return odrv0.axis0.controller.input_vel

def input_pos(odrv0):
    return odrv0.axis0.controller.input_pos

def Id(odrv0):
    return odrv0.axis0.motor.current_control.Id_measured

def Iq(odrv0):
    return odrv0.axis0.motor.current_control.Iq_measured


def modular_record(
        rec_status=0, com_status=0,
        to_record = {
            'position_(turn)':position,
            'command_(turn)':command
        },
        file='data/measure.csv', freq = 100
    ):
    
    odrv0 = odrive.find_any()

    data = open(file, 'w', newline='')
    data_writer = csv.writer(data, delimiter=',', quotechar='|')
    data_writer.writerow(
        ['time_(s)', *to_record.keys()]
    )

    print("Acquisition ready...")
    rec_status.value=1
    print('Waiting for command to start...')
    while com_status.value != 1:
        pass
    print('Acquisition started...')

    t_start = time.time()
    t_last = time.time() - t_start
    t_sleep = 1/freq

    data_writer.writerow(
            [t_last] + [to_record[item](odrv0) for item in to_record.keys()]
        )
    time.sleep(t_sleep)
    
    while com_status.value == 1:
        t_actual = time.time() - t_start
        data_writer.writerow(
            [t_actual] + [to_record[item](odrv0) for item in to_record.keys()]
        )
        t_last = t_actual
        time.sleep(t_sleep)
    
    data.close()
    print("Acquisition done")