'''
Created on Oct 28, 2018

@author: Kyle Santiago
'''

#Start

import asyncio
import os
import sys
import psutil
import time



# CPU

def cpu_status():
    value1 = psutil.cpu_count()
    print('Number of CPUs:', value1)
    value2 = psutil.cpu_percent(interval=2,percpu=True)
    print('Percent in use:',value2)

def inefficient():
    print(cpu_status())

def cpu_stat():
    cpu_status()
    inefficient()

if __name__ == '__cpu_stat__':
    cpu_stat()
#Temp

'''
Having a difficult time accessing hardware temperature.
I'll come back to this later.
'''

# RAM

def v_mem():
    mem = psutil.virtual_memory()
    breakingPoint = (100 * 1024 * 1024) * 10 #1000mb
    if mem.available <= breakingPoint:
        print("WARNING: less than 1000mb of ram available")


def mem_Readability(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def pprint_ntuple(nt):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = mem_Readability(value)
        print('%-10s : %7s' % (name.capitalize(), value))


def main_Memory():
    print('MEMORY\n------')
    pprint_ntuple(psutil.virtual_memory())
    print('\nSWAP\n----')
    pprint_ntuple(psutil.swap_memory())


if __name__ == '__main_Memory__':

    main_Memory()

#HDD and SSD

def forHumans(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def main_Storage():
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
                   "Mount"))
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        print(templ % (
            part.device,
            forHumans(usage.total),
            forHumans(usage.used),
            forHumans(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))

if __name__ == '__main_Storage__':
    main_Storage()


#Hello There

def welcome():
    print("Overseer: Online...")
    print("Always Watching:")

#Exit

async def main_closing():
    
    async def closing():
        input('Press any key to terminate')
        return input
    
  
    task = asyncio.create_task(closing())
    done, pending = await asyncio.wait({task})

    if task in done:
            print('Closing...')
            await asyncio.sleep(1)
            print('Closed')
            sys.exit()


def main():
    welcome()
    cpu_stat()
    main_Storage()
    main_Memory()
    asyncio.run(main_closing())
    welcome()
    sys.exit(app.exec_())


main()
