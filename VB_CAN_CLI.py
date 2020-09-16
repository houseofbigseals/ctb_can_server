import argparse
 
from ctb_can_server.test import main, main1, main2, main3
       
def RT_set(params):
    print(len(params))
    if len(params) != 5:
        print("Noncorrect number of parameters given! 5 parameters needed")
    print("Realtime mode choosen")
    main(params)
   
def Reg_set(params):
    print(len(params))
    if len(params) != 2:
        print("Noncorrect number of parameters given! 2 parameters needed")
    print("U nas tut registry!")
    main1(params)
   
def Id(params):
    if len(params) != 1:
        print("Noncorrect number of parameters given! 1 parameter needed")
    print("U nas tut Id!")
    main2(params)
   
def RF(params):
    if len(params) < 2:
        print("Noncorrect number of parameters given! At least 2 needed")
    print("U nas tut RF!")
    main3(params)
   
def int_or_float(value):  # wtf
    try:
        return int(value, 0) # handle hex int format
    except:
        return float(value) # or just float
 
parser = argparse.ArgumentParser(description='Simple CAN communication script')

parser.add_argument('-RT', dest='process', action='store_const',
                    const=RT_set,
                    help='specifies RT communication')
 
parser.add_argument('-Reg', dest='process', action='store_const',
                    const=Reg_set,
                    help='specifies Reg writing')
 
parser.add_argument('-Id', dest='process', action='store_const',
                    const=Id,
                    help='specifies device Id')
 
 
parser.add_argument('-RF', dest='process', action='store_const',
                    const=RF,
                    help='specifies reg fields access')
 
parser.add_argument('variables', type=int_or_float, nargs='*',
                    help='floats to send to CAN device')
 
args = parser.parse_args() #values extracted from command line
args.process(args.variables) #callback is callbacked. Fuck you!