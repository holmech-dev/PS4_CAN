from PS4_CAN_Send_FU import PS4Controller # for controller class
import time # for sleep pausing
import os # for input driver search
import can # for CAN transmission

if __name__ == "__main__":
    
    # variable to hold status of control connection status
    game_connection = False
    
    # variable to hold state of programming running
    python_running = True
    
    # pretty much infinite loop
    while python_running == True:        
        # if there is no connection to the controller then find one
        if game_connection == False:
            # wait for controller connection
            while not game_connection == True:
                        
                # start sending CAN ~100Hz
                bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
                msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
                bus.send(msg)
                
                # message to show status - waiting for connection to game controller
                print('Waiting For Controller Connection, CAN value = 0 sent')
                # sleep for one second before recheck
                time.sleep(0.01)
                # loop through all drivers that are created in inputs area
                for fn in os.listdir('/dev/input'):
                    # check if joystick is present
                    if fn.startswith('js'):
                        # message to indicate joystick communication is established
                        print("Joystick Controller Connected")
                        # set flag to true to allow exit from loop
                        game_connection = True
        else:
            # if physical controller is connected create class instance of controller
            ps4 = PS4Controller()
            # initialise the controller
            ps4.init()
            # loop to listen to game controller
            while game_connection == True:
                # listen to controller inputs
                ps4.listen()
                # loop in listen has ended - controller communcation has issue
                # kill class completely
                ps4.__del__()
                # set loop flag to false
                game_connection = False
                # debug message to understand controller is no longer being listend for
                print('Game Controller Connection issue - will retry to connect with controller')

