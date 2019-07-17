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
            my_components[key].setup()

        else:
            print("It's not a valid component")
    return my_components


def get_max_min_poll_rate(my_components):
    max_rate = -1.0
    min_rate = 1000.0
    for component in my_components:
        if my_components[component].pollingRate <= min_rate:
            min_rate = my_components[component].pollingRate

        if my_components[component].pollingRate >= max_rate:
            max_rate = my_components[component].pollingRate

    return max_rate, min_rate


def update_loop_cycles(my_components, min_rate):
    for key, component in my_components.iteritems():
        component.calculate_loop_cycles(min_rate)

# Main behaviour


def main():
    # Get components and setup CTRL+C handling
    signal.signal(signal.SIGINT, signal_handler)
    my_components = get_components()

    # Get the sampling ratios of all components in order to
    # define the cycle speed, the number of cycles
    # in between measurements for each component as well as
    # the number of cycles of the slowest component in order
    # to reset the counter
    max_rate, min_rate = get_max_min_poll_rate(my_components)
    max_loops = int(max_rate/min_rate)
    update_loop_cycles(my_components, min_rate)
    print(max_rate, min_rate, max_loops)

    loopcount = 0
    loop_timer = 0
    # Get timestamp, call handle data for each component
    # sleep the rate - time_spent_on_loop
    while True:
        begin = time.time()
        timestamp = int(begin*1000000)  # microseconds

        for key, component in my_components.iteritems():
            if component.loopCycles <= loopcount:
                # p = threading.Thread(
                #     target=component.handleData, args=(timestamp,))
                # p.daemon = True
                # p.start()
                component.handleData(timestamp)

        loopcount += 1
        loop_timer += time.time() - begin
        end = time.time()
        if (end-begin)< min_rate:
            time.sleep(min_rate-(end-begin))
        if loopcount > max_loops:
            loop_timer = loop_timer/loopcount
            print "Loop rate {} ||| Loop exec time avg {} ".format(min_rate,loop_timer)
            loopcount = 0

    sys.exit(0)


if __name__ == "__main__":
    main()
