# -*- coding: utf-8 -*-
"""
Piezo Control Library Test
 for BioPhotonics labworks.

Model of piezo : XX
Control with Nucleo G431KB


Co-Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2023-06-22
"""

import piezo

my_piezo = piezo.piezo()

comList = my_piezo.listSerialHardware()

for port in comList:
    print(f"{port}")
    

selectedPort = input('Com Number ?')

my_piezo.setSerialCom('COM'+str(selectedPort))
my_piezo.connect()

vers = my_piezo.getHWVersion()
print(f'V = {vers}')

position1, position2 = my_piezo.getPosition()
print(f'Pos_um = {position1} / Pos_nm = {position2}')


my_piezo.movePosition(5, 50)

if(my_piezo.isConnected() == True):
    for kk in range(10):
        position1, position2 = input('Saisir 2 valeurs entières : ').split()
        position1 = int(position1)
        position2 = int(position2)
        my_piezo.movePosition(position1, position2)
        position1, position2 = my_piezo.getPosition()
        print(f'Pos_um = {position1} / Pos_nm = {position2}')


my_piezo.disconnect()