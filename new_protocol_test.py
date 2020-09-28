# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import can
import struct
import time

"""
how to generate new message of that type

format of new nessages:

CAN command (like can.Message https://python-can.readthedocs.io/en/master/message.html
) consists of | id, data, crc&etc |

id is 11 bits and it is separated to three parts too:
| 000000 | 0         | 0000    |
| Addr   | Direction | Command |

 - Addr - 6 bit | 000000 | is number of device who (whom) communicate
        000000 is master broadcast
 - Direction - 1 bit | 0 | is bit of direction :
        master -> slave is 0 , slave -> master is 1
 - Command - 4 bits | 0000 | is type of command we send
        we have 7 commands with numbers
        
        1. RT_set
        Code 1 
        Desc: Sends RT float values to drive
        To device: mech_setp, velocity_setp, torque_setp, Kd, Kp
        From device:  None OR RT_get
        Size: 0 / 12
        
        
        https://docs.google.com/spreadsheets/d/e/2PACX-1vRI_Li7lG7eVITgmja1_bDd6evGn6rl4kw2CKIZUERmqUndKNHACREgHenyKhjkRqpbaGyyk127KdbF/pubhtml
        
        https://www.waveshare.com/wiki/2-CH_CAN_FD_HAT		
"""

def main1():
    os.system('sudo ifconfig can0 down')
    os.system(
        'sudo ip link set can0 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')

    # dev_id = 1

    can0 = can.interface.Bus(channel='can0', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)

    # # so much Indian code
    # if type(params[1]) == float:
    #     message_array = bytearray(struct.pack('Lf', *params))
    # else:
    #     message_array = bytearray(struct.pack('LL', *params))

    # lets create new message
    # example id = 0b00000100011   (|000001|0|0011|)
    # data = [0b10100 , 0b0]
    #dlc = 2

    # msg_tx = can.Message(arbitration_id=0b00000100011, dlc=2, data=[20, 0], is_fd=True, extended_id=False)

    message_array = bytearray(struct.pack('=3B', 17, 0, 0))
    # msg_tx = can.Message(arbitration_id=0x20 * 1 + 3, dlc=3, data=message_array, is_fd=True, extended_id=False)

    # NOTE we can generate msg_id using short formula: 0x20*slave_id + num_of_cmd  where
    #  0x20 is |000001|0|0000 - default msg from master to slave with id=1



    msg_tx = can.Message(arbitration_id=0x20 * 1 + 2, dlc=2, data=[10, 0], is_fd=True, extended_id=False)

    print("we sent:")
    print(msg_tx)

    can0.send(msg_tx, 0.5)

    msg_rx = can0.recv(6)
    print("we got:")
    print(msg_rx)

    os.system('sudo ifconfig can0 down')

    print("only data that we got:")
    print(msg_rx.data)

    f1, f2, f3 = struct.unpack('3B', msg_rx.data)
    print(f1, f2, f3)

    # can0.send(msg_tx, 0.5)



    # for i in range(0, 10):
    #     try:
    #         can0.send(msg_tx, 0.5)
    #         msg_rx = can0.recv(6)
    #         print(msg_rx)
    #         # f1, f2, f3 = struct.unpack('3f', msg_rx.data)
    #         # print(f1, f2, f3)
    #         # time.sleep(0.5)
    #
    #     except Exception as e:
    #         print("Error: {}".format(e))



if __name__ == "__main__":
    main1()