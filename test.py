from multiprocessing import Process, Pipe, Value
import time
from Ascii_command import sin_command, increasing_frequency, real_data, step
import Record as r
from Plot import plot_odrive, plot_modular

        
if __name__=='__main__':

    rec_status, com_status = Value('i', 0), Value('i', 0)

    to_record = {
        'command':r.command,
        'position':r.position
    }
    file = 'data/dump.csv'

    recording = Process(target=r.modular_record, args=(rec_status, com_status, to_record, file, 500))
    commanding = Process(target=real_data, args=(com_status,))

    recording.start()
    print('waiting for acquisition to start...')
    while rec_status.value != 1:
        pass
        

    commanding.start()

    while recording.is_alive():
        pass

    # plot_odrive(pow=False, volt=False, vel=False, file='data/measure.csv')
    plot_modular(file, [*to_record.keys()])