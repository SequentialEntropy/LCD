import asyncio
try:
    import i2c as screen
except ImportError:
    import console as screen
# import console as screen

from loadenv import environ
environ()

import loadbustasks
bus_tasks_list = loadbustasks.load()

import display_task as d

async def createDisplay():
    display = screen.display()
    return display

async def main():
    # server = StatusPing(input("Enter server name/ip to track: "))

    display = await createDisplay()
    tasks = []
    tasks.append(asyncio.create_task(d.display_date(display)))
    tasks.append(asyncio.create_task(d.display_time(display)))
    # tasks.append(asyncio.create_task(d.display_cpu(display)))
    # tasks.append(asyncio.create_task(d.ram_disk(display)))
    for bus_task in bus_tasks_list:
        tasks.append(asyncio.create_task(d.bus_time(display, bus_task["row"], bus_task["stop_id"], bus_task["route"])))
    tasks.append(asyncio.create_task(d.hang()))
    await asyncio.gather(*tasks)
    # await tasks[len(tasks) - 1]

if __name__ == '__main__':
    asyncio.run(main())
