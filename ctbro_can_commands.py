#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:33:30 2020

@author: pi
"""

import os
import can
import time
import struct
import numpy as np

# dev_id = 1


class CtbroRTCanHandler:
    """ simply to open-close canX"""
    def __init__(self, can_number=0, dev_id=1, mech_sp=0.0, vel_sp=0.0, mech_gain=0.0, vel_gain=0.0, torq=0.0):
        self.can_number = can_number
        self.dev_id = dev_id
        self.mech_sp=mech_sp
        self.vel_sp=vel_sp
        self.mech_gain=mech_gain
        self.vel_gain=vel_gain
        self.torq=torq

        # lets create can and can bus
        self.create_can()

    def shutdown_can(self):
        print('trying to do sudo ifconfig can{} down'.format(self.can_number))
        os.system('sudo ifconfig can{} down'.format(self.can_number))

    def stop_motor(self):
        print("trying to stop motor")
        # stop params?
        params = [0.0, 0.0, 0.0, 0.0, 0.0]
        # pack params to byte message
        message_array = bytearray(struct.pack('5f', *params))
        msg_tx = can.Message(arbitration_id=0x20 * self.dev_id, dlc=20, data=message_array, is_fd=True, extended_id=False)

        self.can_bus.send(msg_tx, 0.5)


    def create_can(self):
        # try to create device
        print("try to create device can{}".format(self.can_number))
        os.system('sudo ifconfig can{} down'.format(self.can_number))
        os.system(
            'sudo ip link set can{} up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on'.format(self.can_number))

        self.can_bus = can.interface.Bus(channel='can{}'.format(self.can_number), bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)

    def rt_main(self):

        # sorry
        params = [self.mech_sp, self.vel_sp, self.mech_gain, self.vel_gain, self.torq]

        canX = self.can_bus
        # pack params to byte message
        message_array = bytearray(struct.pack('5f', *params))
        # create msg
        msg_tx = can.Message(arbitration_id=0x20 * self.dev_id, dlc=20, data=message_array, is_fd=True, extended_id=False)
        # send it
        canX.send(msg_tx, 0.5)

        msg_rx = canX.recv()

        while 1:
            # we can send this message again and again to see device debug info in answers
            # nothing exept ctrl-C will stop it
            message_array = bytearray(struct.pack('5f', *params))
            msg_tx = can.Message(arbitration_id=0x20 * self.dev_id, dlc=20, data=message_array, is_fd=True, extended_id=False)

            canX.send(msg_tx, 0.5)

            msg_rx = canX.recv()
            print(msg_rx.data)
            f1, f2, f3 = struct.unpack('3f', msg_rx.data)

            print(msg_rx)
            print(f1, f2, f3)

            time.sleep(0.3)

            # can0.send(msg_tx, 0.5)


# TODO fix names
#  and add more comments
#  and fix args

def main1(params):
    os.system('sudo ifconfig can0 down')
    os.system(
        'sudo ip link set can0 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')

    can0 = can.interface.Bus(channel='can0', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)

    # so much Indian code
    if type(params[1]) == float:
        message_array = bytearray(struct.pack('Lf', *params))
    else:
        message_array = bytearray(struct.pack('LL', *params))

    msg_tx = can.Message(arbitration_id=0x20 * dev_id + 3, dlc=8, data=message_array, is_fd=True, extended_id=False)

    can0.send(msg_tx, 0.5)

    while 1:
        msg_rx = can0.recv()
        f1, f2, f3 = struct.unpack('3f', msg_rx.data)

        print(msg_rx)
        print(f1, f2, f3)


def main2(params):
    os.system('sudo ifconfig can0 down')
    os.system(
        'sudo ip link set can0 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')

    can0 = can.interface.Bus(channel='can0', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)

    message_array = bytearray(struct.pack('L', *params))

    msg_tx = can.Message(arbitration_id=0x20 * dev_id + 7, dlc=4, data=message_array, is_fd=True, extended_id=False)

    can0.send(msg_tx, 0.5)

    while 1:
        msg_rx = can0.recv()
        print(msg_rx)


def int_float(value):
    try:
        return np.array(value, dtype=np.int32).tobytes('C')  # int(value, 0) # handle hex int format
    except:
        return np.array(value, dtype=np.float32).tobytes('C')  # or just float


def main3(params):
    byte1 = params[0]
    byte2 = params[1]

    print(byte1, byte2)

    arr = bytearray(int_float(np.delete(params, [0, 1])))
    print(["0x%02x" % b for b in arr])
    print(len(arr))

    os.system('sudo ifconfig can0 down')
    os.system(
        'sudo ip link set can0 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')

    can0 = can.interface.Bus(channel='can0', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)

    message_array = arr
    msg_tx = can.Message(arbitration_id=0x20 * dev_id + 7, dlc=len(arr) + 2, data=message_array, is_fd=True,
                         extended_id=False)

    can0.send(msg_tx, 0.5)

    while 1:
        msg_rx = can0.recv()
        print(msg_rx)