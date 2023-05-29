#!/usr/bin/env python3

import subprocess
from argparse import ArgumentParser

def manage(args):
    cmd = [
        "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
    ]
    cmd.extend(args)
    subprocess.run(cmd)


def createVM(vm_name):
    cmd = (
        'createvm',
        '--name',
        vm_name,
        '--ostype',
        'MacOS_64',
        '--register'
    )
    manage(cmd)


def addSettings(vm_name, memory, cpu):
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


def createHDD(hdd_path, size):
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


def createHDDController(vm_name):
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


def attachHDD(vm_name, hdd_path):
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


def createDVDController(vm_name):
    cmd = (
        'storagectl',
        vm_name,
        '--name',
        '"IDE Controller"',
        '--add',
        'ide'
    )
    manage(cmd)


def removeHDD(hdd_path):
    cmd = (
        'closemedium',
        'disk',
        hdd_path,
        '--delete'
    )
    manage(cmd)


def go(vm_name, memory, cpu, size):
    hdd_path = f"F:\VM Stuff\VM's\Virtualbox\{vm_name}\{vm_name}.vdi"

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


def main():
    parser = ArgumentParser()

    parser.add_argument('--name', nargs=1, required=True)
    parser.add_argument('--memory', nargs=1, required=True)
    parser.add_argument('--cpu', nargs=1, required=True)
    parser.add_argument('--size', nargs=1, required=True)

    args = parser.parse_args()

    go(args.name[0], args.memory[0], args.cpu[0], args.size[0])


if __name__ == '__main__':
    main()
