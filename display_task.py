import sys

import asyncio

import time

import functools

from status import StatusPing
import stats

from bus import bus_stop

import os

def display_task(function):
    @functools.wraps(function)
    def io_exit(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except OSError as e:
            print(e)
            sys.exit()
    return io_exit



@display_task
async def display_date(display):
    while True:
        date_out = time.strftime("%a %d %b")
        await display.display(date_out, 1, length=10)
        await asyncio.sleep(60)

@display_task
async def display_time(display):
    while True:
        time_out = time.strftime("%H:%M:%S")
        await display.display(time_out, 1, length=8, alignRight=True)
        await asyncio.sleep(0.1)

@display_task
async def display_online(display, server):
    while True:
        players_out = "Players: {}".format(server.get_status()["players"]["online"])
        await display.display(players_out, 3, length=10)
        await asyncio.sleep(0.1)

@display_task
async def display_cpu(display):
    while True:
        percent_cpu_out = "CPU: {}%".format(stats.percent_cpu())
        temp_cpu_out = "Temp: {}°C".format(stats.temp_cpu())
        await display.display(percent_cpu_out, 2, length=9)
        await display.display(temp_cpu_out, 2, length=11, alignRight=True)
        await asyncio.sleep(1)

@display_task
async def display_ram(display):
    while True:
        ratio_ram_out = "RAM: {}/{} GB".format(stats.used_ram(2), stats.total_ram(1))
        percent_ram_out = "{}%".format(stats.percent_ram())
        await display.display(ratio_ram_out, 3, length=16)
        await display.display(percent_ram_out, 3, length=4, alignRight=True)
        await asyncio.sleep(1)

@display_task
async def display_disk(display):
    while True:
        ratio_space_out = "Disk: {}/{} GB".format(stats.used_space(), stats.total_space())
        percent_space_out = "{}%".format(stats.percent_space())
        await display.display(ratio_space_out, 4, length=16)
        await display.display(percent_space_out, 4, length=4, alignRight=True)
        await asyncio.sleep(60)

@display_task
async def bus_time(display):
    stop = bus_stop(os.environ["STOP"])
    route = os.environ["ROUTE"]
    while True:
        await stop.update(os.environ["KEY"])
        try:
            await display.display("{}: {}".format(route, "   ".join(["Arr" if bus.waiting_time == 0 else str(bus.waiting_time) for bus in stop.buses[str(route)]])), 4, reset=True)
        except KeyError:
            await display.display("{}: No Services".format(route), 4, reset=True)
        await asyncio.sleep(20)

@display_task
async def ram_disk(display):
    while True:
        percent_ram_out = "RAM: {}%".format(stats.percent_ram())
        percent_disk_out = "Disk: {}%".format(stats.percent_space())
        await display.display(percent_ram_out, 3, length=10)
        await display.display(percent_disk_out, 3, pos=10, length=10)
        await asyncio.sleep(1)

@display_task
async def hang(seconds=None):
    if seconds != None:
        await asyncio.sleep(seconds)
    else:
        while True:
            await asyncio.sleep(1)