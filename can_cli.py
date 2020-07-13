#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import cmd
import time
import re
import signal
import sys

# from cheetahbro_can_server.ctbro_can_commands import rt_main, shutdown_can
# why it doesnt work?
from ctbro_can_commands import rt_main, shutdown_can


# sorry its global
global_can_number = None

# args string to autocomplete rt command
RT_args = [
    'can_number:0, dev_id:0, mech_sp:0.0, vel_sp:0.0, mech_gain:0.0, vel_gain:0.0, torq:0.0'
]

# small class to create can cli shell
class MyCmd(cmd.Cmd):
    doc_header = "This is CLI for cheetahbro can interface. Available commands is:"
    prompt = "> "
    intro = 'Welcome to the cheetahbro can shell.   Type help or ? to list commands.\n' \
            'Add here some more info'

    def do_rt(self, line):
        '''sends data to cheetahbro motor through canX interface and then in infinity loop asks for debug info\n
        can_number - number of can interface \n
        dev_id - motor device can address \n
        mech_sp - preferred mechanical setpoint\n
        vel_sp - preferred velocity setpoint\n
        mech_gain - preferred  mechanical gain\n
        vel_gain - preferred velocity gain\n
        torq - preferred torque of motor'''

        print("parsing input args")
        parsed_args_list = parse_RT_args(line)

        rt_main(*parsed_args_list)

    def complete_rt(self, text, line, start_index, end_index):
        if text:
            return [
                address for address in RT_args
                if address.startswith(text)
            ]
        else:
            return RT_args


def parse_RT_args(arg_string):
    global global_can_number

    # monkey code using re
    dev_id = re.findall('can_number:\d*, dev_id:(\d*), mech_sp:\d*.\d*, vel_sp:\d*.\d*, mech_gain:\d*.\d*, vel_gain:\d*.\d*, torq:\d*.\d*', arg_string)
    print("dev_id is {}".format(int(dev_id[0])))

    can_number = re.findall('can_number:(\d*), dev_id:\d*, mech_sp:\d*.\d*, vel_sp:\d*.\d*, mech_gain:\d*.\d*, vel_gain:\d*.\d*, torq:\d*.\d*', arg_string)
    print("can_number is {}".format(int(can_number[0])))

    global_can_number = int(can_number[0])

    mech_sp = re.findall('can_number:\d*, dev_id:\d*, mech_sp:(\d*.\d*), vel_sp:\d*.\d*, mech_gain:\d*.\d*, vel_gain:\d*.\d*, torq:\d*.\d*', arg_string)
    print("mech_sp is {}".format(float(mech_sp[0])))

    vel_sp = re.findall('can_number:\d*, dev_id:\d*, mech_sp:\d*.\d*, vel_sp:(\d*.\d*), mech_gain:\d*.\d*, vel_gain:\d*.\d*, torq:\d*.\d*', arg_string)
    print("vel_sp is {}".format(float(vel_sp[0])))

    mech_gain = re.findall('can_number:\d*, dev_id:\d*, mech_sp:\d*.\d*, vel_sp:\d*.\d*, mech_gain:(\d*.\d*), vel_gain:\d*.\d*, torq:\d*.\d*', arg_string)
    print("mech_gain is {}".format(float(mech_gain[0])))

    vel_gain = re.findall('can_number:\d*, dev_id:\d*, mech_sp:\d*.\d*, vel_sp:\d*.\d*, mech_gain:\d*.\d*, vel_gain:(\d*.\d*), torq:\d*.\d*', arg_string)
    print("vel_gain is {}".format(float(vel_gain[0])))

    torq = re.findall('can_number:\d*, dev_id:\d*, mech_sp:\d*.\d*, vel_sp:\d*.\d*, mech_gain:\d*.\d*, vel_gain:\d*.\d*, torq:(\d*.\d*)', arg_string)
    print("torq is {}".format(float(torq[0])))

    return int(can_number[0]), int(dev_id[0]), float(mech_sp[0]), float(vel_sp[0]), \
                float(mech_gain[0]), float(vel_gain[0]), float(torq[0])


def exit_gracefully(signal, frame):
    global global_can_number
    # ... log exiting information ...
    # ... close any open files ...
    # print("trying gracefully delete device can{}".format(global_can_number))
    # do shutdown canX
    if global_can_number:  # if it was set
        print("trying gracefully delete device can{}".format(global_can_number))
        shutdown_can(can_number=global_can_number)
    print("\n exiting cli shell program")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_gracefully)
    my_cmd = MyCmd()
    my_cmd.cmdloop()