#!/usr/bin/env python3

import shutil
import subprocess
from argparse import ArgumentParser
from typing import Sequence

VBoxMange_path = shutil.which('VBoxManage')

if not VBoxMange_path:
    raise FileNotFoundError


def manage(args: Sequence) -> None:
    cmd = [
        VBoxMange_path
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
        '--chipset',
        'ich9'
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


def createDVDController(vm_name: str) -> None:
    cmd = (
        'storagectl',
        vm_name,
        '--name',
        'IDE Controller',
        '--add',
        'ide'
    )
    manage(cmd)


def attachImageToOpticalDrive(vm_name: str, image: str) -> None:
    cmd = (
        'storageattach',
        vm_name,
        '--storagectl',
        'IDE Controller',
        '--port',
        '0',
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
        'IDE Controller',
        '--port',
        '0',
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
# Allow enableBoot to accept other arguments

def enableBoot(vm_name: str) -> None:
    cmds = (
        (
            'modifyvm',
            vm_name,
            '--cpuidset',
            '00000001',
            '000306a9',
            '04100800',
            '7fbae3ff',
            'bfebfbff'
        ),
        (
            'setextradata',
            vm_name,
            'VBoxInternal/Devices/efi/0/Config/DmiSystemProduct',
            'MacBookPro15,1'
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
            'Mac-551B86E5744E2388'
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


def go(vm_name: str, memory: str, cpu: str, size: str, root: str, image: str) -> None:
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

    createDVDController(vm_name)
    attachImageToOpticalDrive(vm_name, image)

    enableBoot(vm_name)


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('--name', nargs=1, type=str, help='VM Name', metavar='')
    parser.add_argument('--memory', nargs=1, type=str, help='RAM Size', metavar='MB')
    parser.add_argument('--cpu', nargs=1, type=str, help='# of CPU/Processors', metavar='#')
    parser.add_argument('--size', nargs=1, type=str, help='Size of HDD', metavar='MB')
    parser.add_argument('--root', nargs=1, type=str, help='Virtualbox root path', metavar='')
    parser.add_argument('--image', nargs=1, type=str, help='Image to boot from', metavar='ISO/DMG')
    parser.add_argument('--remove', action='store_true', help='Remove VM')
    parser.add_argument('--attach', action='store_true', help='Attach image to DVD Drive')
    parser.add_argument('--detach', action='store_true', help='Detach image from DVD Drive')

    args = parser.parse_args()

    if args.name and args.memory and args.cpu and args.size and args.root and args.image:
        go(args.name[0], args.memory[0], args.cpu[0], args.size[0], args.root[0], args.image[0])

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