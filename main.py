import asyncio
try:
    import i2c as screen
except ImportError:
    import console as screen

import time

from status import StatusPing
import stats

async def display_date(display):
    while True:
        await display.display(time.strftime("%a %d %b"), 1, reset=False)
        await asyncio.sleep(60)

async def display_time(display):
    while True:
        await display.display(time.strftime("%H:%M:%S"), 1, 20, alignRight=True, reset=False)
        await asyncio.sleep(1)

async def display_online(display, server):
    while True:
        await display.display("Players Online: {}".format(str(server.get_status()["players"]["online"])), 3)
        await asyncio.sleep(0.1)

async def display_cpu(display):
    while True:
        await display.display("CPU: {}%".format(stats.percent_cpu()), 2)
        await display.display("Temp: {}°C".format(stats.temp_cpu()), 2, 20, alignRight=True, reset=False)
        await asyncio.sleep(1)

async def display_ram(display):
    while True:
        await display.display("RAM: {}/{} GB".format(stats.used_ram(3), stats.total_ram()), 3)
        await display.display("{}%".format(stats.percent_ram()), 3, 20, alignRight=True, reset=False)
        await asyncio.sleep(1)

async def display_disk(display):
    while True:
        await display.display("Disk: {}/{} GB".format(stats.used_space(), stats.total_space()), 4)
        await display.display("{}%".format(stats.percent_space()), 4, 20, alignRight=True, reset=False)
        await asyncio.sleep(60)

async def createDisplay():
    display = screen.display()
    return display

async def main():
    server = StatusPing(input("Enter server name/ip to track: "))

    display = await createDisplay()
    tasks = []
    tasks.append(asyncio.create_task(display_date(display)))
    tasks.append(asyncio.create_task(display_time(display)))
    # tasks.append(asyncio.create_task(display_online(display, server)))
    tasks.append(asyncio.create_task(display_cpu(display)))
    tasks.append(asyncio.create_task(display_ram(display)))
    tasks.append(asyncio.create_task(display_disk(display)))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())