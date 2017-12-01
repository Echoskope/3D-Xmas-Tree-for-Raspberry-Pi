from gpiozero import LEDBoard
from gpiozero.tools import random_values
from signal import pause
import random, time

tree = LEDBoard(*range(2,28),pwm=True)

effectsSpeed = 0.025 #This is the speed at which the LEDs update. Bigger number = slower updates.

###################################
#                                 #
#  The LEDs are setup with PWM    #
#  and can accept values between  #
#  0.0 and 1.0.                   #
#                                 #
#  The star is on GPIO 2, or LED  #
#  tree[0].                       #
#                                 #
###################################

led_dict = {} #Setup the main dictionary
led_list = range(len(tree)) #make a list of sequential numbers, 1 number per LED

for ident in led_list: #Cycle through each LED and setup default values
 ledMotion = ident%2 #This will give us alternating 1's and 0's to make effects look better
 ledSpeed = random.randrange(0,5) #Pick a random speed range

 randomValueList = [0,0,0,0] #Define the list to hold all the seed brightness values
 randomValueList[0] = (random.randrange(1,25))/100.0 #0.01 through 0.25
 randomValueList[1] = (random.randrange(26,50))/100.0 #0.26 through 0.50
 randomValueList[2] = (random.randrange(51,75))/100.0 #0.51 through 0.75
 randomValueList[3] = (random.randrange(76,99))/100.0 #0.76 through 0.99
 value_group = random.randrange(0,3) #Pick one of the brightness vaules to assign LED

 #Setup the LED dictionary
 led_dict[str(ident)] = {"value":randomValueList[value_group], "motion":ledMotion, "speed":ledSpeed}



###############################################################################
#                                                                             #
#  brightnessModify(value, motion, speed):                                    #
#  value = LED brightness value                                               #
#  motion = increasing or decreasing brightness (1=increasing 0=decreasing)   #
#  speed = speed at which brightness changes; 6 speed settings (0 through 5)  #
#                                                                             #
#  returns:                                                                   #
#  function returns new value, motion, and speed values                       #
#  value should always be new except around boundary values                   #
#  motion and speed may or may not change                                     #
#                                                                             #
###############################################################################
def brightnessModify(value, motion, speed):
 if speed == 0: #slowest speed
  deltaChange = 0.001 #step size
 if speed == 1:
  deltaChange = 0.005
 if speed == 2:
  deltaChange = 0.008
 if speed == 3:
  deltaChange = 0.01
 if speed == 4:
  deltaChange = 0.0175
 if speed == 5: #fastest speed
  deltaChange = 0.0225

 if motion == 1: #increasing in value
  value = value + deltaChange
 if motion == 0: #decreasing in value
  value = value - deltaChange

 if (motion == 1) and (value > 0.5): #chance for motion and speed to change for effects
  motion = random.randrange(0,1)
  speed = random.randrange(0,5)

 if (motion == 0) and (value < 0.5): #chance for motion and speed to change for effects
  motion = random.randrange(0,1)
  speed = random.randrange(0,5)


 if ((value < 0.000) or (value > 1.0)): #if we've hit a boundary for the PWM

  if value < 0.0: #If we are at the lower boundary
   value = 0.0 #Force value to be 0
   motion = 1 #Change motion to increase on next pass through

  if value > 1.0: #If we are at the upper boundary
   value = 1.0 #Force value to be 1
   motion = 0 #Change motion to decrease on next pass through

 return [value, motion, speed]



#############################################################
#                                                           #
#  Main While Loop                                          #
#  Gets the new settings out of the dictionary              #
#  Sets the brightness of the LED via "value"               #
#  Calls to brightnessModify() to get new parameters        #
#  Writes new parameters into dictionary and gets next LED  #
#                                                           #
#############################################################

while (1):

 for leds in led_list:
  ledString = str(leds) #Needed to ref the dict

  value = led_dict[ledString]['value'] #Pull the value info
  motion = led_dict[ledString]['motion'] #Pull the motion info
  speed = led_dict[ledString]['speed'] #Pull the speed info

  tree[leds].value = value #Set the LED brightness

  newSettings = brightnessModify(value, motion, speed) #Get the new settings
#  print str(newSettings[0]) + " --- " + str(newSettings[1]) + " --- " + str(newSettings[2])
  led_dict[ledString]['value'] = newSettings[0] #Update the value info
  led_dict[ledString]['motion'] = newSettings[1] #Update the motion info
  led_dict[ledString]['speed'] = newSettings[2] #Update the speed info

 time.sleep(effectsSpeed) #Time between LED updates

