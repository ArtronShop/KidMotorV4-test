import wmi
import os
import time
import shutil
import serial
import serial.tools.list_ports

base_path = os.path.dirname(__file__)
MicroPython_Firmware_uf2 = os.path.realpath(base_path + "/MicroPython.uf2")
MicroPython_MainScript_py = os.path.realpath(base_path + "/script.py")

print("MicroPython_Firmware_uf2", MicroPython_Firmware_uf2)
print("MicroPython_MainScript_py", MicroPython_MainScript_py)

c = wmi.WMI()
"""
for item in c.Win32_PhysicalMedia():
    print(item)

for drive in c.Win32_DiskDrive():
    print(drive)
"""
for disk in c.Win32_LogicalDisk():
    print(disk)


def isFoundRP2Drive():
    for disk in c.Win32_LogicalDisk():
        # if int(disk.Size) == 134066176 and disk.MediaType == :
        return disk.Name
    return None

def isFoundMicroPythonDrive():
    for disk in c.Win32_LogicalDisk():
        # if int(disk.Size) == 1417216 and disk.MediaType == :
        return disk.Name
    return None

while True:
    # os.system("cls")
    print("===|| KidMotorV4 auto uploader ||===")
    print("------------------------------------")
    print("wait RP2 drive are present...")
    drive = None
    while not drive:
        time.sleep(0.5)
        drive = isFoundRP2Drive()
    print("copy {} to {} ...".format(os.path.basename(MicroPython_Firmware_uf2), drive))
    try:
        shutil.copy(MicroPython_Firmware_uf2, os.path.realpath(drive + "/firmware.uf2"))
    except:
        input("Copy FAIL !, Press the <ENTER> key to try again...")
        continue
    print("wait MicroPython drive are present...")
    drive = None
    while not drive:
        time.sleep(0.5)
        drive = isFoundMicroPythonDrive()
    print("copy {} to {} ...".format(os.path.basename(MicroPython_MainScript_py), drive))
    shutil.copy(MicroPython_MainScript_py, os.path.realpath(drive + "/main.py"))
    ports = serial.tools.list_ports.comports()
    port = None
    for info in ports:
        if info.vid == 0x2E8A and info.pid == 0x0005:
            port = info.port
            break
    print("found {} send soft reset command...", port)
    with serial.Serial(port, 115200, timeout=1) as ser:
        ser.write(b'\x03') # Ctrl + C
        time.sleep(0.1)
        ser.write(b'\x04') # Soft reset
        ser.close()
    print("finish ! wait board disconnect")
    while isFoundMicroPythonDrive():
        time.sleep(0.5)
    