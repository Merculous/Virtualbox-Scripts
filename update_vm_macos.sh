#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <name>"
else
    echo "Setting $1 settings..."
    cd /c/Program\ Files/Oracle/VirtualBox
    ./VBoxManage.exe modifyvm "$1" --cpuidset 00000001 000306a9 04100800 7fbae3ff bfebfbff
    ./VBoxManage.exe setextradata "$1" "VBoxInternal/Devices/efi/0/Config/DmiSystemProduct" "MacBookPro15,1"
    ./VBoxManage.exe setextradata "$1" "VBoxInternal/Devices/efi/0/Config/DmiSystemVersion" "1.0"
    ./VBoxManage.exe setextradata "$1" "VBoxInternal/Devices/efi/0/Config/DmiBoardProduct" "Mac-551B86E5744E2388"
    ./VBoxManage.exe setextradata "$1" "VBoxInternal/Devices/smc/0/Config/DeviceKey" "ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc"
    ./VBoxManage.exe setextradata "$1" "VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC" 0
    ./VBoxManage.exe setextradata "$1" "VBoxInternal2/EfiGraphicsResolution" 1920x1080
fi
