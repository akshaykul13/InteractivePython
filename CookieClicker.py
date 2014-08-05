"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_generated = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self._current_time) +  " Current Cookies: " + str(self._current_cookies) + " CPS = " + str(self._current_cps)+ " Total Cookies: " + str(self._total_cookies_generated) + " History: " + str(self._history)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        required_cookies = cookies - self._current_cookies
        if required_cookies <= 0:
            return 0.0
        else:
            return (float)(math.ceil(required_cookies/self._current_cps))
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_cookies = self._current_cookies + time*self._current_cps
            self._total_cookies_generated = self._total_cookies_generated + time*self._current_cps
            self._current_time = self._current_time + time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies > cost :
            self._history.append((self._current_time, item_name, cost, self._total_cookies_generated))
            self._current_cps = self._current_cps + additional_cps
            self._current_cookies = self._current_cookies - cost        
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    # Replace with your code
    #build_info_clone = build_info.clone()
    clicker_state_class = ClickerState()
    time = 0
    while True :
        if time >= duration:
            break
        item = strategy(clicker_state_class.get_cookies(), clicker_state_class.get_cps(), duration-time, build_info)
        print item
        if item == None :
            break
        
    return clicker_state_class


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always returns the cheapest item
    """
    build_list = build_info.build_items()
    #print build_list
    cheap = None
    lowest_cost = 99999999
    for item in build_list:
        #print item
        #print build_info.get_cost(item)
        if build_info.get_cost(item) < lowest_cost and (cookies + cps*time_left) >= build_info.get_cost(item) :
            lowest_cost = build_info.get_cost(item)              
            cheap = item
    return cheap

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always returns the most expensive item
    """
    build_list = build_info.build_items()
    #print build_list
    expensive = None
    highest_cost = -1
    for item in build_list:
        #print item
        #print build_info.get_cost(item)
        if build_info.get_cost(item) > highest_cost and (cookies + cps*time_left) >= build_info.get_cost(item) :
            highest_cost = build_info.get_cost(item)              
            expensive = item
    return expensive

def strategy_best(cookies, cps, time_left, build_info):
    """
    Always returns item for the best strategy
    """
    build_list = build_info.build_items()
    #print build_list
    select = None
    highest_value = -1
    for item in build_list:
        #print item
        #print build_info.get_cost(item)
        if (cookies + cps*time_left) >= build_info.get_cost(item) :
            if build_info.get_cps(item)/build_info.get_cost(item) > highest_value :
                highest_value = build_info.get_cps(item)/build_info.get_cost(item)              
                select = item
    return select
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
#strategy_cheap(500000.0, 1.0, 5.0, BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))

