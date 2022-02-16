import asyncio
try:
    import i2c as screen
except ImportError:
    import console as screen
# import console as screen

import time

from status import StatusPing
import stats

from bus import bus_stop

import os

from loadenv import environ
environ()

async def display_date(display):
    while True:
        date_out = time.strftime("%a %d %b")
        await display.display(date_out, 1, length=10)
        await asyncio.sleep(60)

async def display_time(display):
    while True:
        time_out = time.strftime("%H:%M:%S")
        await display.display(time_out, 1, length=8, alignRight=True)
        await asyncio.sleep(0.1)

async def display_online(display, server):
    while True:
        players_out = "Players: {}".format(server.get_status()["players"]["online"])
        await display.display(players_out, 3, length=10)
        await asyncio.sleep(0.1)

async def display_cpu(display):
    while True:
        percent_cpu_out = "CPU: {}%".format(stats.percent_cpu())
        temp_cpu_out = "Temp: {}°C".format(stats.temp_cpu())
        await display.display(percent_cpu_out, 2, length=9)
        await display.display(temp_cpu_out, 2, length=11, alignRight=True)
        await asyncio.sleep(1)

async def display_ram(display):
    while True:
        ratio_ram_out = "RAM: {}/{} GB".format(stats.used_ram(2), stats.total_ram(1))
        percent_ram_out = "{}%".format(stats.percent_ram())
        await display.display(ratio_ram_out, 3, length=16)
        await display.display(percent_ram_out, 3, length=4, alignRight=True)
        await asyncio.sleep(1)

async def display_disk(display):
    while True:
        ratio_space_out = "Disk: {}/{} GB".format(stats.used_space(), stats.total_space())
        percent_space_out = "{}%".format(stats.percent_space())
        await display.display(ratio_space_out, 4, length=16)
        await display.display(percent_space_out, 4, length=4, alignRight=True)
        await asyncio.sleep(60)

async def bus_time(display):
    stop = bus_stop(os.environ["STOP"])
    route = os.environ["ROUTE"]
    while True:
        await stop.update(os.environ["KEY"])
        try:
            await display.display("{}: {}".format(route, "   ".join([str(bus.waiting_time) for bus in stop.buses[str(route)]])), 4, reset=True)
        except KeyError:
            await display.display("{}: No Services".format(route), 4, reset=True)
        await asyncio.sleep(20)

async def ram_disk(display):
    while True:
        percent_ram_out = "RAM: {}%".format(stats.percent_ram())
        percent_disk_out = "Disk: {}%".format(stats.percent_space())
        await display.display(percent_ram_out, 3, length=10)
        await display.display(percent_disk_out, 3, pos=10, length=10)
        await asyncio.sleep(1)

async def hang(seconds=None):
    if seconds != None:
        await asyncio.sleep(seconds)
    else:
        while True:
            await asyncio.sleep(1)

async def createDisplay():
    display = screen.display()
    return display

async def main():
    # server = StatusPing(input("Enter server name/ip to track: "))

    display = await createDisplay()
    tasks = []
    tasks.append(asyncio.create_task(display_date(display)))
    tasks.append(asyncio.create_task(display_time(display)))
    # tasks.append(asyncio.create_task(display_online(display, server)))
    tasks.append(asyncio.create_task(display_cpu(display)))
    # tasks.append(asyncio.create_task(display_ram(display)))
    # tasks.append(asyncio.create_task(display_disk(display)))
    tasks.append(asyncio.create_task(ram_disk(display)))
    tasks.append(asyncio.create_task(bus_time(display)))
    tasks.append(asyncio.create_task(hang()))
    # await asyncio.gather(*tasks)
    await tasks[len(tasks) - 1]

if __name__ == '__main__':
    asyncio.run(main())
