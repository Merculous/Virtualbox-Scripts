#!/usr/bin/env python3

import shutil
import subprocess
from argparse import ArgumentParser
from typing import Sequence

VBoxManage_path = shutil.which('VBoxManage')

if not VBoxManage_path:
    raise FileNotFoundError('VBoxManage not found within $PATH!')


def manage(args: Sequence) -> None:
    cmd = [
        VBoxManage_path
    ]
    cmd.extend(args)
    subprocess.run(cmd)


def createVM(vm_name: str) -> None:
    cmd = (
        'createvm',
        '--name',
        vm_name,
        '--ostype',
        'MacOS_64',
        '--register'
    )
    manage(cmd)


def addSettings(vm_name: str, memory: str, cpu: str) -> None:
    cmd = (
        'modifyvm',
        vm_name,
        '--memory',
        memory,
        '--vram',
        '128',
        '--cpus',
        cpu,
        '--nic1',
        'bridged',
        '--bridgeadapter1',
        'eno1',
        '--chipset',
        'ich9',
        '--firmware',
        'efi',
        '--vrde',
        'on',
        '--usbehci',
        'on',
        '--mouse',
        'usbtablet',
        '--keyboard',
        'usb',
        '--defaultfrontend',
        'separate'
    )
    manage(cmd)


def createHDD(hdd_path: str, size: str) -> None:
    cmd = (
        'createmedium',
        '--filename',
        hdd_path,
        '--size',
        size,
        '--variant',
        'Fixed'
    )
    manage(cmd)


def createHDDController(vm_name: str) -> None:
    cmd = (
        'storagectl',
        vm_name,
        '--name',
        'SATA Controller',
        '--add',
        'sata',
        '--controller',
        'IntelAHCI'
    )
    manage(cmd)


def attachHDD(vm_name: str, hdd_path: str) -> None:
    cmd = (
        'storageattach',
        vm_name,
        '--storagectl',
        'SATA Controller',
        '--device',
        '0',
        '--port',
        '0',
        '--type',
        'hdd',
        '--medium',
        hdd_path
    )
    manage(cmd)


def attachImageToOpticalDrive(vm_name: str, image: str) -> None:
    cmd = (
        'storageattach',
        vm_name,
        '--storagectl',
        'SATA Controller',
        '--port',
        '1',
        '--device',
        '0',
        '--type',
        'dvddrive',
        '--medium',
        image
    )
    manage(cmd)


def detachImageFromOpticalDrive(vm_name: str) -> None:
    cmd = (
        'storageattach',
        vm_name,
        '--storagectl',
        'SATA Controller',
        '--port',
        '1',
        '--device',
        '0',
        '--medium',
        'none'
    )
    manage(cmd)


def removeHDD(hdd_path: str) -> None:
    cmd = (
        'closemedium',
        'disk',
        hdd_path,
        '--delete'
    )
    manage(cmd)


def removeVM(vm_name: str) -> None:
    cmd = (
        'unregistervm',
        vm_name,
        '--delete'
    )
    manage(cmd)


# TODO
# Allow enableBoot to accept other arguments, most important is cpuidset.

# https://dortania.github.io/OpenCore-Install-Guide/extras/smbios-support.html

def enableBoot(vm_name: str) -> None:
    cmds = (
        (
            'modifyvm',
            vm_name,
            '--cpuidset',
            '00000001',
            '000106e5',
            '00100800',
            '0098e3fd',
            'bfebfbff'
        ),
        (
            'setextradata',
            vm_name,
            'VBoxInternal/Devices/efi/0/Config/DmiSystemProduct',
            'iMac14,3'
        ),
        (
            'setextradata',
            vm_name,
            'VBoxInternal/Devices/efi/0/Config/DmiSystemVersion',
            '1.0'
        ),
        (
            'setextradata',
            vm_name,
            'VBoxInternal/Devices/efi/0/Config/DmiBoardProduct',
            'Mac-77EB7D7DAF985301'
        ),
        (
            'setextradata',
            vm_name,
            'VBoxInternal/Devices/smc/0/Config/DeviceKey',
            'ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc'
        ),
        (
            'setextradata',
            vm_name,
            'VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC',
            '0'
        ),
        (
            'setextradata',
            vm_name,
            'VBoxInternal2/EfiGraphicsResolution',
            '1920x1080'
        )
    )

    for cmd in cmds:
        manage(cmd)


def go(vm_name: str, memory: str, cpu: str, size: str, root: str) -> None:
    hdd_path = f'{root}/{vm_name}/{vm_name}.vdi'

    createVM(vm_name)
    addSettings(vm_name, memory, cpu)

    # Virtualbox complains about one being left over even if you actually delete thes files/folder, there's still a mention about the hdd
    # It is mentioned in ~/.VirtualBox/VirtualBox.xml
    # Might have to add try/except block for this bit here (inside manage())
    removeHDD(hdd_path)

    createHDD(hdd_path, size)
    createHDDController(vm_name)
    attachHDD(vm_name, hdd_path)

    enableBoot(vm_name)


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('--name', nargs=1, type=str, help='VM Name', metavar='')
    parser.add_argument('--memory', nargs=1, type=str, help='RAM Size', metavar='MB')
    parser.add_argument('--cpu', nargs=1, type=str, help='# of CPU/Processors', metavar='#')
    parser.add_argument('--size', nargs=1, type=str, help='Size of HDD', metavar='MB')
    parser.add_argument('--root', nargs=1, type=str, help='Virtualbox VM root path', metavar='')
    parser.add_argument('--image', nargs=1, type=str, help='Image to boot from', metavar='ISO/DMG')
    parser.add_argument('--remove', action='store_true', help='Remove VM')
    parser.add_argument('--attach', action='store_true', help='Attach image to DVD Drive')
    parser.add_argument('--detach', action='store_true', help='Detach image from DVD Drive')

    args = parser.parse_args()

    # For linux users, using "readlink -f <file>" will give you the absolute path for a file.
    # This is helpful when debugging, especially with VSCode.
    # This is best if you need to get the path of an ISO/DMG if it's not in the same directory.

    # TODO
    # Figure out UUID issue

    # VBoxManage startvm <name> --type headless
    # VBoxManage controlvm <name> acpipowerbutton
    # VBoxManage controlvm <name> poweroff

    # VBoxManage guestproperty enumerate <name>
    # VBoxManage guestproperty get <name> "/VirtualBox/GuestInfo/Net/0/V4/IP" | awk '{ print $2 }'`

    if args.name and args.memory and args.cpu and args.size and args.root:
        go(args.name[0], args.memory[0], args.cpu[0], args.size[0], args.root[0])

    elif args.name and args.remove:
        removeVM(args.name[0])

    elif args.name and args.attach and args.image:
        attachImageToOpticalDrive(args.name[0], args.image[0])

    elif args.name and args.detach:
        detachImageFromOpticalDrive(args.name[0])

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
