import asyncio
try:
    import i2c as screen
except ImportError:
    import console as screen

import time

from status import StatusPing

import stats

async def displayTime(display):
    while True:
        await display.display("Time: {}".format(time.strftime("%H:%M:%S")), 1)
        await asyncio.sleep(0.1)

async def displayDate(display):
    while True:
        await display.display("Date: {}".format(time.strftime("%m/%d/%Y")), 2)
        await asyncio.sleep(0.1)

async def displayOnline(display, server):
    while True:
        await display.display("Players Online: {}".format(str(server.get_status()["players"]["online"])), 3)
        await asyncio.sleep(0.1)

async def displayTemp(display):
    while True:
        await display.display("Temp: {}".format(stats.temp()), 4)
        await asyncio.sleep(0.1)

async def createDisplay():
    display = screen.display()
    return display

async def main():
    server = StatusPing(input("Enter server name/ip to track: "))

    display = await createDisplay()
    tasks = []
    tasks.append(asyncio.create_task(displayTime(display)))
    tasks.append(asyncio.create_task(displayDate(display)))
    tasks.append(asyncio.create_task(displayOnline(display, server)))
    tasks.append(asyncio.create_task(displayTemp(display)))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())