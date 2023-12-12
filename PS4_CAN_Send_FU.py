import pygame
import time
#from time import sleep
import can
import os, stat, sys
import glob

from colorama import Fore, Back, Style, init
init(autoreset=True)

#Initialise CANbus
#bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
#msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
#bus.send(msg)


class PS4Controller(object):
    def __init__(self):# declare variables for controller
        self.controller = None
        self.axis_data = None
        self.button_data = None
        self.hat_data = None
        
        # variables to hold location of drive for this instance of controller
        self.blueDir = None
        self.greenDir = None
        self.redDir = None
        # variable to hold satus of controller connection
        self.active = False
        
        # create a CANbus socket
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        #create message for sending to CAN (ch)
        self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
        #sebd message to can up on init (ch)
        self.bus.send(self.msg)
        
    
    def init(self):
            #initialise pygame joystick
            pygame.init()
            pygame.joystick.init()
            
            # llop through joysticks and assign to class
            for x in range(pygame.joystick.get_count()):
                self.controller = pygame.joystick.Joystick(x)
                # initialise class controller
                self.controller.init()
            # set controller cativity flag to true - indicate controller is fully setup
            self.active = True
            
            
            #Set LED Green
            # set folder for LED control - varies with each new connection
            self.blueDir = (glob.glob("/sys/class/leds/*:blue/brightness"))
            self.greenDir = (glob.glob("/sys/class/leds/*:green/brightness"))
            self.redDir = (glob.glob("/sys/class/leds/*:red/brightness"))
            
            # Set LED Permissions - this program must be ran with sudo
            os.chmod(self.blueDir[0], stat.S_IWOTH)
            os.chmod(self.greenDir[0], stat.S_IWOTH)
            os.chmod(self.redDir[0], stat.S_IWOTH)
            
            # set blue LED == OFF
            led = open(self.blueDir[0], "w")
            led.write ("0")
            led.close()
            # set green LED == ON - indcates controller is fully connected
            led = open(self.greenDir[0], "w")
            led.write ("255")
            led.close()
            # set ref LED == OFF
            led = open(self.redDir[0], "w")
            led.write ("0")
            led.close()
            
    def button_finder(self,num):

            print("This is the dict: {}".format(num))
            
            # loop through the button array passed into function
            for k in num:
                # when button press status in array is found
                if (num[k] == True):
                    # set the index to found value
                    index = k
            # 'X' Button pressed
            if index == 0:
                    print (Fore.WHITE+ "X")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 32], extended_id=False)
                    #
                    #time.sleep(0.2)
            # 'CIRCLE' Button Pressed
            elif index == 1:
                    print (Fore.RED+ "CIRCLE")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 128], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # 'TRIANGLE' Button Pressed
            elif index == 2:
                    print (Fore.GREEN+ "TRIANGLE")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 16], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # 'SQUARE' Button Pressed
            elif index == 3:
                    print(Fore.MAGENTA+ "SQUARE")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 64], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # 'L1' Button Pressed
            elif index == 4:
                    print(Fore.WHITE+ "L1")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 1], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # 'R1' Button Pressed
            elif index == 5:
                    print(Fore.WHITE+ "R1")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 2], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # 'L2' Button Pressed
            elif index == 6:
                    print(Fore.WHITE+ "L2")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 1, 0], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # 'R2' Button Pressed
            elif index == 7:
                    print(Fore.WHITE+ "R2")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 2, 0], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # 'Share' Button Pressed
            elif index == 8:
                    print(Fore.CYAN+ "Share Button")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 1, 0, 0], extended_id=False)
            # 'Options' Button Pressed
            elif index == 9:
                    print(Fore.CYAN+ "Options Button")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 2, 0, 0], extended_id=False)
            # 'PS' Button Pressed
            elif index == 10:
                    print(Fore.CYAN+ "PS Button")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 1, 0, 0, 0], extended_id=False)
            # 'LEFT JOYSTICK' Pushed down
            elif index == 11:
                    print(Fore.CYAN+ "LEFT")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 1, 0, 0, 0, 0], extended_id=False)
                    #msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 4], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # 'RIGHT JOYSTICK' Pushed down
            elif index == 12:
                    print(Fore.CYAN+ "RIGHT")
                    self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 2, 0, 0, 0, 0], extended_id=False)
                    #msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 8], extended_id=False)
                    #bus.send(msg)
                    #time.sleep(0.2)
            # Other button catch - but should never happen as button limit is 12
            else:
                    print(Fore.RED + "UNKNOWN button value: ")
                    self.msg=can.Message(arbitration_id=0x599, data=[1, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
            
            return -1

    
    
    def listen(self):
        # Listen for button press events
        status = self.controller.get_init()
        
        # check if button data array has any values
        if not self.button_data:
            # if button_data array is None, then add array
            self.button_data = {}
            # build array based on number of buttons avaialble from controller
            for i in range (self.controller.get_numbuttons()):
                # set each value in array to false for intialisation
                self.button_data[i] = False
                
                
        # run while controller active flag is set to true
        while self.active == True:
            # create start for loop timer (ch)
            #start = 0
            #start = time.clock()
            # Gets button data from controller
            
            
            
                
            for event in pygame.event.get():
                    #print("Entered For")
                    #button_values= []
                    #n = 0
                    if event.type == pygame.JOYBUTTONDOWN:
                            # set LED colour green == OFF
                            ledchange = open(self.greenDir[0], "w")
                            ledchange.write ("0")
                            ledchange.close()
                            # set LED colour red == ON
                            ledchange = open(self.redDir[0], "w")
                            ledchange.write ("255")
                            ledchange.close()
                            # recognise button pressed
                            self.button_data[event.button] = True
                            
                            # if a button press is registered
                            if (self.button_data[event.button]):
                                # run function to find whihc button was pressed
                                self.button_finder(self.button_data)

                    elif event.type == pygame.JOYBUTTONUP:
                            # recognise button relase
                            self.button_data[event.button] = False
                            # send out CAN message with nothing pressed
                            self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
                            #self.bus.send(msg)
                            

                            # check if controller is still connected
                            try:					
                                    ledchange = open(self.redDir[0], "w")
                                    ledchange.write ("0")
                                    ledchange.close()
                                    ledchange = open(self.greenDir[0], "w")
                                    ledchange.write ("255")
                                    ledchange.close()
                            except:
                                    # controller is lost
                                    print("Can't communicate with controller")
                                    self.active = False
                                    self.controller.quit()
                    # publish rate ~100HZ (ch)                
            time.sleep(0.01)
                    # send to CAN bus (ch)
            self.bus.send(self.msg)
                    
                    # hold value on button press for 0.01 sec
                    ##time.sleep(0.2)
                    # reset values to zero from previous button press
                    ##self.msg=can.Message(arbitration_id=0x599, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
                    # send 0 value to can bus ready for next loop iteration
                    ##self.bus.send(self.msg)
                    # find time taken per loop and print (ch)              
                    #print("Time taken this loop: ", time.clock() - start)
                                         
    def __del__(self):
        print('Cleaned class - safe to create new instance')
    
    def __exit__(self, exc_type, exc_value, traceback):
        # clean up class if gets destroyed
        print('Package destroyed')
        self.package_obj.cleanup()
        
						
