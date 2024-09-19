import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_odrive(pow=True, pos=True, volt=True, vel=True, file='data/data_Odrive.csv'):

    n_plot = pow + pos + volt + vel
    fig, axs = plt.subplots(n_plot, 1, figsize=(6.4, 8), layout='constrained', sharex=True)

    data = pd.read_csv(file)

    i = 0

    if pow:
        ax_power = axs[i]
        i += 1
        # electrical & mechanical power
        ax_power.set_title("Elec & Meca power")
        ax_power.set_xlabel('time (s)')
        ax_power.set_ylabel('power (W)')

        artists = ax_power.plot(
        data['time_(s)'],
        data[['meca_power_(W)', 'elec_power_(W)']],
        )
        ax_power.legend(artists, ['Mechanical power', 'Electrical power'])

    if pos:
        ax_position = axs[i]
        i += 1
        # command & position
        ax_position.set_title("Command & Position")
        ax_position.set_xlabel('time (s)')
        ax_position.set_ylabel('position (turn)')

        ax_position.plot(
        data['time_(s)'],
        data[['command_(turn)', 'position_(turn)']]
        )

    if volt:
        ax_i = axs[i]
        i += 1
        # current & voltage
        ax_i.set_title("Current & Voltage")
        ax_i.set_ylabel("Current (I)", color='r')
        ax_i.set_xlabel('time (s)')
        ax_i.tick_params(color='r')

        ax_v = ax_i.twinx()
        ax_v.set_ylabel("Voltage (V)", color='b')
        ax_v.set_xlabel('time (s)')
        ax_v.tick_params(color='b')

        ax_i.plot(
        data['time_(s)'],
        data['current_(I)'],
        color='r'
        )

        ax_v.plot(
        data['time_(s)'],
        data['voltage_(V)'],
        color='b', alpha=.2
        )

    if vel:
        ax_vel = axs[i]
        i += 1
        # velocity
        ax_vel.set_title("Velocity")
        ax_vel.set_ylabel("Velocity (turn/s)")
        ax_vel.set_xlabel('time (s)')

        ax_vel.plot(
        data['time_(s)'],
        data['velocity_(turn/s)']
        )

    plt.show()


def plot_AC():

    data_AC = pd.read_csv('data_AC.csv', index_col='Time')
    data_Odrive = pd.read_csv('data_Odrive.csv', index_col='time_(s)')
    data_Odrive = data_Odrive[
        np.logical_and(
            data_Odrive.index < data_Odrive.index[-1] - .6,
            data_Odrive.index > data_Odrive.index[0] + .6
            )
        ]
    data_Odrive.index = data_Odrive.index - data_Odrive.index[0]

    ax = data_AC.plot(y='Position droite', label='AC raw data')
    ax.plot(data_Odrive.index, data_Odrive['command_(turn)'], label='AC filtered data')

    plt.show()


def plot_modular(file, to_plot):
    data = pd.read_csv(file)

    data.plot(x='time_(s)', y=to_plot)

    plt.show()

    return

if __name__=='__main__':
    plot_modular('data/I_vel_pow.csv', ['power_(W)', 'velocity_(turn/s)', 'I_(A)'])
    plot_modular('data/pos_command.csv', ['command_(turn)', 'position_(turn)'])