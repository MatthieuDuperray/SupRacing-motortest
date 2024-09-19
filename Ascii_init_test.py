import serial
import time
import odrive

pos_max = 55
pos_min = 0

amplitude = (pos_max - pos_min) / 2
pos_repos = pos_min + amplitude

# init
odrv0 = serial.Serial("COM3", timeout=0.01)
odrv0.write(b'sc\n')
odrv0.write(b'w axis0.requested_state 11\n')
odrv0.write(b'w axis1.requested_state 11\n')

state_axis0 = 11
state_axis1 = 11

while (state_axis0 != 1) or (state_axis1 != 1):
    # Reading state
    time.sleep(.5)
    odrv0.write(b'r axis0.current_state\n')
    state_axis0 = int(odrv0.read(4).decode('utf-8'))

    odrv0.write(b'r axis1.current_state\n')
    state_axis1 = int(odrv0.read(4).decode('utf-8'))
    print("axis0 : {} | axis1 : {}".format(state_axis0, state_axis1))

time.sleep(.1)

# Controller config check

odrv0.write(b'r axis0.controller.config.control_mode\n')
odrv0.write(b'r axis0.controller.config.input_mode\n')
odrv0.write(b'r axis1.controller.config.control_mode\n')
odrv0.write(b'r axis1.controller.config.input_mode\n')
print(odrv0.read(16).decode())

odrv0.write(b'w axis0.controller.config.input_mode 3\n')
odrv0.write(b'w axis1.controller.config.input_mode 3\n')
odrv0.write(b'w axis0.controller.config.control_mode 3\n')
odrv0.write(b'w axis1.controller.config.control_mode 3\n')

odrv0.write(b'w axis0.requested_state 8\nw axis1.requested_state 8\n')
time.sleep(.1)
odrv0.write(b'r axis0.current_state\nr axis1.current_state\n')
print(odrv0.read(8).decode())

print("Homing done")

odrv0.write(bytes("p 0 {}\n".format(pos_repos), "utf-8"))
odrv0.write(bytes("p 1 {}\n".format(pos_repos), "utf-8"))

print("Init done")

pos0 = 0.0
pos1 = 0.0

while abs(pos0 - pos_repos) > 0.1 or abs(pos1 - pos_repos) > 0.1:
    odrv0.write(b'r axis0.encoder.pos_estimate\n')
    pos0 = float(odrv0.read(12).decode())
    odrv0.write(b'r axis1.encoder.pos_estimate\n')
    pos1 = float(odrv0.read(12).decode())

    print(pos0, pos1)

odrv0.write(b'w axis0.requested_state 1\n')
odrv0.write(b'w axis1.requested_state 1\n')
