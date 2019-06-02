import sys
import datetime, time
import RPi.GPIO as GPIO 
import configparser


if len(sys.argv) <2:
   print('Usage:')
   print(sys.argv[0]+' Z -100')
   sys.exit()

configFilePath = '/etc/pycnc.conf'

configParser = configparser.RawConfigParser()
configParser.read(configFilePath)

interval=0.005

STEPPER_STEP_PIN_X  = configParser.getint('axis', 'stepper_step_pin_x')
STEPPER_DIR_PIN_X   = configParser.getint('axis', 'stepper_dir_pin_x')
ENDSTOP_PIN_X       = configParser.getint('axis', 'endstop_pin_x')

STEPPER_STEP_PIN_Y  = configParser.getint('axis', 'stepper_step_pin_y')
STEPPER_DIR_PIN_Y   = configParser.getint('axis', 'stepper_dir_pin_y')
ENDSTOP_PIN_Y       = configParser.getint('axis', 'endstop_pin_y')

STEPPER_STEP_PIN_Z  = configParser.getint('axis', 'stepper_step_pin_z')
STEPPER_DIR_PIN_Z   = configParser.getint('axis', 'stepper_dir_pin_z')
ENDSTOP_PIN_Z       = configParser.getint('axis', 'endstop_pin_z')

STEPPER_STEP_PIN_E  = configParser.getint('axis', 'stepper_step_pin_e')
STEPPER_DIR_PIN_E   = configParser.getint('axis', 'stepper_dir_pin_e')


#set relay config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(STEPPER_STEP_PIN_X, GPIO.OUT)
GPIO.setup(STEPPER_STEP_PIN_Y, GPIO.OUT)
GPIO.setup(STEPPER_STEP_PIN_Z, GPIO.OUT)
GPIO.setup(STEPPER_STEP_PIN_E, GPIO.OUT)

GPIO.setup(STEPPER_DIR_PIN_Y, GPIO.OUT)
GPIO.setup(STEPPER_DIR_PIN_X, GPIO.OUT)
GPIO.setup(STEPPER_DIR_PIN_Z, GPIO.OUT)
GPIO.setup(STEPPER_DIR_PIN_E, GPIO.OUT)


axis = ['X','Y','Z','E']
stepPins = [STEPPER_STEP_PIN_X, STEPPER_STEP_PIN_Y,  STEPPER_STEP_PIN_Z, STEPPER_STEP_PIN_E]
dirPins = [STEPPER_DIR_PIN_X, STEPPER_DIR_PIN_Y, STEPPER_DIR_PIN_Z, STEPPER_DIR_PIN_E]


def sendOne(gpioID):
    GPIO.output(gpioID, GPIO.HIGH)
    time.sleep(interval)


def sendZero(gpioID):
    GPIO.output(gpioID, GPIO.LOW)
    time.sleep(interval)

key = axis.index(sys.argv[1])
stepcount=int(sys.argv[2])


if stepcount < 0:
    sendOne(dirPins[key])
    stepcount = stepcount * -1
else:
    sendZero(dirPins[key])

for step in range(stepcount):
    sendOne(stepPins[key])
    sendZero(stepPins[key])


