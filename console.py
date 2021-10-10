from threading import Thread
import time
import sys

def up():
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()

class display:
    def __init__(self):
        self.delay = 0.1
        self.strings = [" " * 20, " " * 20, " " * 20, " " * 20]
        t = Thread(target=self.loop)
        t.daemon = True
        t.start()

    def display(self, string, line=1, pos=0):
        self.strings[line - 1] = (" " * pos + string + " " * 20)[:20]

    def loop(self):
        print("\n" * 3)
        while True:
            self.update()
            time.sleep(self.delay)

    def update(self):
        for i in range(4):
            up()
        print("\33[44m" + "\n".join(self.strings) + "\33[0m")