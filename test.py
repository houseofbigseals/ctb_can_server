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

dev_id = 1
 
def main(params):
    os.system('sudo ifconfig can1 down')
    os.system('sudo ip link set can1 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')
   
    can0 = can.interface.Bus(channel = 'can1', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)
   
    message_array = bytearray(struct.pack('5f', *params))
    msg_tx = can.Message(arbitration_id=0x20*dev_id, dlc=20, data= message_array, is_fd=True, extended_id=False)
   
    can0.send(msg_tx, 0.5)
   
    msg_rx = can0.recv()
 
    while 1:
        # we can send this message again and again to see device debug info in answers
        message_array = bytearray(struct.pack('5f', *params))
        msg_tx = can.Message(arbitration_id=0x20*dev_id, dlc=20, data= message_array, is_fd=True, extended_id=False)
       
        can0.send(msg_tx, 0.5)
       
        msg_rx = can0.recv()
        print( msg_rx.data )
        f1, f2, f3 = struct.unpack('3f', msg_rx.data)
       
        print (msg_rx)
        print ( f1, f2, f3)
       
        time.sleep(0.3)
 
        #can0.send(msg_tx, 0.5)
       
def main1(params):
    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')
   
    can0 = can.interface.Bus(channel = 'can0', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)
   
    # so much Indian code
    if type(params[1]) == float:
        message_array = bytearray(struct.pack('Lf', *params))
    else:
        message_array = bytearray(struct.pack('LL', *params))
       
    msg_tx = can.Message(arbitration_id= 0x20*dev_id + 3, dlc=8, data= message_array, is_fd=True, extended_id=False)
   
    can0.send(msg_tx, 0.5)
   
    while 1:
           
        msg_rx = can0.recv()
        f1, f2, f3 = struct.unpack('3f', msg_rx.data)
       
        print (msg_rx)
        print ( f1, f2, f3)
       
def main2(params):
    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')
   
    can0 = can.interface.Bus(channel = 'can0', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)
       
    message_array = bytearray(struct.pack('L', *params))
   
    msg_tx = can.Message(arbitration_id= 0x20*dev_id + 7, dlc=4, data= message_array, is_fd=True, extended_id=False)
   
    can0.send(msg_tx, 0.5)
   
    while 1:
        msg_rx = can0.recv()
        print (msg_rx)
         
def int_float(value):
    try:
        return np.array(value, dtype=np.int32).tobytes('C')#int(value, 0) # handle hex int format
    except:
        return np.array(value, dtype=np.float32).tobytes('C') # or just float
   
def main3(params):
    byte1 = params[0]
    byte2 = params[1]
   
    print( byte1, byte2)
 
    arr = bytearray(int_float(np.delete(params, [0,1])))
    print([ "0x%02x" % b for b in arr ])
    print(len(arr))
 
    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 up type can bitrate 1000000   dbitrate 1000000 restart-ms 1000 loopback on berr-reporting on fd on')
   
    can0 = can.interface.Bus(channel = 'can0', bustype='socketcan_ctypes', bitrate=1000000, data_bitrate=8000000, fd=True)
       
    message_array = arr
    msg_tx = can.Message(arbitration_id= 0x20*dev_id + 7, dlc=len(arr)+2, data= message_array, is_fd=True, extended_id=False)
   
    can0.send(msg_tx, 0.5)
   
    while 1:
        msg_rx = can0.recv()
        print (msg_rx)