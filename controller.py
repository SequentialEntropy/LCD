from threading import Thread
import time
import hid

# for device in hid.enumerate():
#     print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

gamepad = hid.device()
gamepad.open(0x20d6, 0xa713)
gamepad.set_nonblocking(True)

while True:
    report = gamepad.read(64)
    if report:
        print(report)
        print(bin(report[0]))
        print(report[0] & 0b00000100 != 0)
        print(report[0] & 0b00000010 != 0)
        print()