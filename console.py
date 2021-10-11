import asyncio
import time
import sys

def up():
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()

def insert(original, string, pos):
    return original[:pos] + string + original[pos + len(string):]

class display:
    def __init__(self):
        self.delay = 0.1
        self.strings = [" " * 20, " " * 20, " " * 20, " " * 20]
        asyncio.create_task(self.loop())

    async def display(self, string, line=1, pos=0):
        self.strings[line - 1] = (insert(self.strings[line - 1], string, pos))[:20]

    async def loop(self):
        print("\n" * 3)
        while True:
            await self.update()
            await asyncio.sleep(self.delay)

    async def update(self):
        for i in range(4):
            up()
        print("\33[44m" + "\n".join(self.strings) + "\33[0m")