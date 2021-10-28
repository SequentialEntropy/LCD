import asyncio
import time
import sys

def up():
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()

def insert(original, string, pos, length=None, alignRight=False):
    if alignRight:
        if length == None:
            return (original[:len(original) - len(string) - pos] + string + original[len(original) - pos:])[:len(original)]
        return (original[:len(original) - length - pos] + " " * (length - len(string)) + string[max(len(string) - length, 0):] + original[len(original) - pos:])[:len(original)]
    if length == None:
        return (original[:pos] + string + original[pos + len(string):])[:len(original)]
    return (original[:pos] + string[:length] + " " * (length - len(string)) + original[pos + length:])[:len(original)]

class display:
    def __init__(self):
        self.delay = 0.1
        self.strings = [" " * 20, " " * 20, " " * 20, " " * 20]
        asyncio.create_task(self.loop())

    async def display(self, string, line=1, pos=0, length=None, alignRight=False, reset=False):
        if reset:
            self.strings[line - 1] = (insert(" " * 20, string, pos, alignRight=alignRight))
        else:
            self.strings[line - 1] = (insert(self.strings[line - 1], string, pos, length=length, alignRight=alignRight))

    async def loop(self):
        print("\n" * 3)
        while True:
            await self.update()
            await asyncio.sleep(self.delay)

    async def update(self):
        for i in range(4):
            up()
        print("\33[44m" + "\n".join(self.strings) + "\33[0m")