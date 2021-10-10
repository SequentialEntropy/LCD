try:
    import i2c as screen
except ImportError:
    import console as screen

import time

from status import StatusPing

server = StatusPing(input("Enter server name/ip to track: "))

display = screen.display()

while True:
    display.display("Time: {}".format(time.strftime("%H:%M:%S")), 1)
    display.display("Date: {}".format(time.strftime("%m/%d/%Y")), 2)
    display.display("Players Online: {}".format(str(server.get_status()["players"]["online"])), 3)