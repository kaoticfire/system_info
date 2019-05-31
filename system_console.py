__version__ = '1.5'
__author__ = 'Virgil Hoover'

from os import getenv, name, system
from platform import release, uname
from socket import getfqdn, gethostbyname_ex, gethostname
import platform.system as ps
from pypsexec.client import Client
from wmi import WMI


def connection(exe, computer, user_pass):
    user_id = getenv('UserName')
    c = Client(computer, username=user_id, password=user_pass)
    c.connect()
    try:
        c.create_service()
        c.run_executable(exe)
    finally:
        c.cleanup()
        c.disconnect()
    return


class SystemInfo():
    def __init__(self):
        self.full_name = getfqdn('127.0.0.1')
        self.host_end = self.full_name.find('.')
        self.prefix = self.full_name.find('-')
        self.clinic = self.full_name[:self.prefix]
        self.host_name = gethostname()
        self.s_number = self.full_name[self.prefix:self.host_end]
        self.domain = self.full_name[self.host_end:]
        self.ip = gethostbyname_ex(self.host_name)[2][0]
        self.proc = uname()[5]
        self.processor = self.proc.find('=')
        self.drive = getenv('SystemDrive')
        self.username = getenv('UserName')
        self.os = ps() + ' ' + release()

    @staticmethod
    def sys_ram():
        comp = WMI()
        total_ram = ''
        available_ram = ''
        for i in comp.Win32_ComputerSystem():
            total = i.TotalPhysicalMemory
            total_ram = str(round(int(total) / 1024 / 1024 / 1024, 2)) + ' GB'
        for av in comp.Win32_OperatingSystem():
            available = av.FreePhysicalMemory
            available_ram = str(round(int(available) / 1024 / 1024, 2)) + ' GB'
        return available_ram, total_ram

    @staticmethod
    def disk():
        c = WMI()
        free_disk = ''
        total_disk = ''
        for disk in c.Win32_LogicalDisk(DriveType=3):
            if disk.DeviceID == "C:":
                free_disk = str(round(int(disk.FreeSpace) / 1024 / 1024 / 1024, 2)) + ' GB'
                total_disk = str(round(int(disk.Size) / 1024 / 1024 / 1024, 2)) + ' GB'
        return free_disk, total_disk

    def display(self):
        # Display information
        if '-' not in self.host_name:
            print('Clinic: None Found')
        else:
            try:
                int(self.clinic)
                print('Clinic:', self.clinic.replace('-', ''))
            except ValueError:
                print('Clinic: None Found')
        print('Hostname:', self.host_name)
        print('Service Tag:', self.s_number.replace('-', ''))
        print('Domain:', self.domain.replace('.', '', 1))
        print('')
        print('IP Address:', self.ip)
        print('')
        print('Operating System:', self.os)
        print('CPU:', self.proc[:self.processor] + 'l')
        print('Current User:', self.username)
        print('')
        print('Available Memory:', self.sys_ram()[0])
        print('Total Memory:', self.sys_ram()[1])
        print('')
        print('System Drive:', self.drive)
        print('Available Disk Space:', self.disk()[0])
        print('Total Disk Space:', self.disk()[1])


if __name__ == '__main__':
    # Clear the screen before displaying the menu.
    if name == 'nt':
        _ = system('cls')
        app = SystemInfo()
        app.display()
    else:
        _ = system('clear')
        print('This requires a windows operating system.')

