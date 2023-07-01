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
        'bridged'
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
        '"SATA Controller"',
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
        '"SATA Controller"',
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
        '"IDE Controller"',
        '--add',
        'ide'
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

    createDVDController(vm_name)


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('--name', nargs=1, type=str)
    parser.add_argument('--memory', nargs=1, type=str)
    parser.add_argument('--cpu', nargs=1, type=str)
    parser.add_argument('--size', nargs=1, type=str)
    parser.add_argument('--root', nargs=1, type=str)
    parser.add_argument('--remove', action='store_true')

    args = parser.parse_args()

    if args.name and args.memory and args.cpu and args.size and args.root:
        go(args.name[0], args.memory[0], args.cpu[0], args.size[0], args.root[0])

    elif args.name and args.remove:
        removeVM(args.name[0])

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
