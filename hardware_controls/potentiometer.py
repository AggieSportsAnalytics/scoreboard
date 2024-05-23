from gpiozero import PWMLED, MCP3008
from time import sleep

pot = MCP3008(0)

while True:
    #Printed value is between 0 and 1 depending on how much the knob is turned
    print(pot.value)
    sleep(0.1)
