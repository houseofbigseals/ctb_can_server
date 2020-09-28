# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 09:39:32 2020

@author: pi
"""

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



import os
import can
import time
import struct

# import numpy as np

os.system('sudo ifconfig can0 down')
os.system(
    'sudo ip link set can0 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')

can0 = can.interface.Bus(channel='can0', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)

flag = 0

# unlock EEPROM
message_array = bytearray(struct.pack('=3B', 17, 0, 0))
msg_tx = can.Message(arbitration_id=0x20 * 1 + 3, dlc=3, data=message_array, is_fd=True, extended_id=False)
can0.send(msg_tx, 0.5)

msg_rx = can0.recv()
b1, b2 = struct.unpack('=BB', msg_rx.data)
print(b1, format(b2, '#010b'))

# enable motor
message_array = bytearray(struct.pack('=3B', 12, 0, 2))
msg_tx = can.Message(arbitration_id=0x20 * 1 + 3, dlc=3, data=message_array, is_fd=True, extended_id=False)
can0.send(msg_tx, 0.5)

msg_rx = can0.recv()
b1, b2 = struct.unpack('=BB', msg_rx.data)
print(b1, format(b2, '#010b'))

message_array = bytearray(struct.pack('5f', 0.0, 0.0, 3.0, 0.1, 0.0))
msg_tx = can.Message(arbitration_id=0x20 * 1, dlc=20, data=message_array, is_fd=True, extended_id=False)
can0.send(msg_tx, 0.5)

# change offset
message_array = bytearray(struct.pack('=2Bf', 8, 0, 0.0))
msg_tx = can.Message(arbitration_id=0x20 * 1 + 3, dlc=6, data=message_array, is_fd=True, extended_id=False)
can0.send(msg_tx, 0.5)

msg_rx = can0.recv()
b1, b2 = struct.unpack('=BB', msg_rx.data)
print(b1, format(b2, '#010b'))

print("finished")
