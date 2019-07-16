from config.configuration import componentDic
from componentClass import Component
import multiprocessing as mp
import threading
import signal
import sys
import time


# CTRl+C handler to exit the program properly
def signal_handler(sig, frame):
    print('Bye Bye')
    sys.exit(0)

# Get components from the config file
def get_components():
    my_components = {}
    for key in componentDic:
        # Imports the name of the class and creates an object
        mod = __import__(key, fromlist=[componentDic.get(key)])
        klass = getattr(mod, componentDic.get(key))
        aux_component = klass()
        # Ignores objects which are not Components
        if isinstance(aux_component, Component):
            my_components[key] = klass()
        else:
            print("It's not a valid component")
    return my_components

# Create a thread to run each component
def get_max_min_poll_rate(my_components):
    max_rate = -1.0
    min_rate = 1000.0
    for component in my_components:
        if my_components[component].pollingRate <= min_rate:
            min_rate = my_components[component].pollingRate

        if my_components[component].pollingRate >= max_rate:
            max_rate = my_components[component].pollingRate
        
    return max_rate,min_rate

def calculate_loop_cycles(my_components,min_rate):
   for component in my_components:
       my_components[component].loopCycles = int(my_components[component].pollingRate / min_rate)

# Wait for all the proccesses to finish (shouldn't get here
# since they run in a loop)
def wait_components_finish(p):
    print("Waiting for threads to finish")
    for component in p:
        p.get(component).join()

# Main behaviour
def main():
    signal.signal(signal.SIGINT, signal_handler)
    my_components = get_components()
    
    max_rate,min_rate = get_max_min_poll_rate(my_components)
    max_loops = int(max_rate/min_rate)
    calculate_loop_cycles(my_components,min_rate)
    loopcount =0
    while True:
        begin = time.time()
        timestamp = begin*1000000 #microseconds
        for component in my_components:
            if my_components[component].loopCycles <= loopcount:
                my_components[component].handleData(timestamp)
        loopcount+=1
        time.sleep(min_rate-(begin-time.time()))
        if loopcount > max_loops:
            loopcount=0
    # Used for testing purpouses to kill the program with ctrl + c
    # by force (not ideal)
    # while True:
    #     time.sleep(3)

    sys.exit(0)


if __name__ == "__main__":
    main()
