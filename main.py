import asyncio
try:
    import i2c as screen
except ImportError:
    import console as screen
# import console as screen

from loadenv import environ
environ()

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
    # tasks.append(asyncio.create_task(d.display_online(display, server)))
    tasks.append(asyncio.create_task(d.display_cpu(display)))
    # tasks.append(asyncio.create_task(d.display_ram(display)))
    # tasks.append(asyncio.create_task(d.display_disk(display)))
    tasks.append(asyncio.create_task(d.ram_disk(display)))
    tasks.append(asyncio.create_task(d.bus_time(display)))
    tasks.append(asyncio.create_task(d.hang()))
    await asyncio.gather(*tasks)
    # await tasks[len(tasks) - 1]

if __name__ == '__main__':
    asyncio.run(main())
