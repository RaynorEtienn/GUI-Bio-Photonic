# -*- coding: utf-8 -*-
"""
Piezo Control Library
 for BioPhotonics labworks.

Model of piezo : XX
Control with Nucleo G431KB


Co-Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2023-06-22
"""

import serial
import serial.tools.list_ports
import time

class piezo:
    """Class for controlling piezoelectric motion system, 
	using an interface of type Nucleo-G431KB.

    This class uses PySerial library to communicate with Nucleo board.
	The baudrate is 115200 bds.

	
    """

    def __init__(self):
        """
        Initialize a piezo system
		"""
        self.connected = False
        self.serialCom = None
        self.serialLink = None
        self.comList = None
         
    def listSerialHardware(self):
        self.comList = serial.tools.list_ports.comports()
        return self.comList
    
    def setSerialCom(self, value):
        """
        Set the serial port number
        
        Parameters
        ----------
        value : STR
            number of the communication port - COMxx for windows
            
        Returns
        -------
        None
        """
        self.serialCom = value
        print(self.serialCom)

    def connect(self):
        """
        Connect to the hardware interface
		via a Serial connection
        
        Returns
        -------
            True if connection is done
            False if not
		"""
        if(self.connected == False):
            if(self.serialCom != None):
                try:
                    self.serialLink = serial.Serial(self.serialCom, baudrate=115200)
                    self.connected = True
                    return True
                except:
                    print('Cant connect')
                    self.connected = False
                    return False
            
    def isConnected(self):
        """
        Return if the hardware is connected
        
        Returns
        -------
            True if hardware is connected
            False if not
        """
        if(self.connected):
            try:
                self.serialLink.write(b'_C!')
            except:
                print('Error Sending') 
            # Timeout 
            for k in range(10):
                if(self.serialLink.in_waiting == 4):
                    self.readBytes = self.serialLink.read(4).decode('utf-8')
                    if(self.readBytes[2] == '1'):
                        return True
                    else:
                        return False
                else:
                    time.sleep(0.02)
        return False
        
    def disconnect(self):
        if(self.connected):
            if(self.isConnected()):
                try:
                    self.serialLink.close()
                    self.connected = False
                    return True
                except:
                    print("Cant disconnect")
                    return False
                
    def getPosition(self):
        """
        Return the position of the piezo
        
        Returns
        -------
        pos_um : INT 
            position in um (integer part)
        pos_nm : INT
            position in nm (integer part)
        """
        if(self.connected):
            try:
                self.serialLink.write(b'_G!')
            except:
                print('Error Sending - GetPosition') 
            # Detection of acknowledgement value
            for k1 in range(10):
                if(self.serialLink.in_waiting < 2):
                    self.readBytes = self.serialLink.read(2).decode('utf-8')
                    # if position sended
                    if(self.readBytes[1] == 'G'):
                        # Detection of acknowledgement value
                        for k2 in range(10):
                            if(self.serialLink.in_waiting == 7):
                                self.readBytes = self.serialLink.read(7).decode('utf-8')
                                pos_um = 0
                                pos_nm = 0
                                if(self.readBytes[0] != ' '):
                                    pos_um += (int(self.readBytes[0]))*10
                                if(self.readBytes[1] != ' '):
                                    pos_um += (int(self.readBytes[1]))*1

                                if(self.readBytes[3] != ' '):
                                    pos_nm += (int(self.readBytes[3]))*100
                                if(self.readBytes[4] != ' '):
                                    pos_nm += (int(self.readBytes[4]))*10
                                if(self.readBytes[5] != ' '):
                                    pos_nm += (int(self.readBytes[5]))*1

                                return pos_um, pos_nm
                            else:
                                time.sleep(0.1)
                    else:
                        pos_um = -1
                        pos_nm = -1
                        return pos_um, pos_nm
                else:
                    time.sleep(0.1)
        print('Enf of function')
        return -1,-1
    
    def getHWVersion(self):
        """
        Get hardware version.

        Returns
        -------
        None.

        """
        if(self.connected):
            try:
                self.serialLink.write(b'_V!')
            except:
                print('Error Sending - HW Version') 
            # Timeout / 1 s
            for k in range(10):
                if(self.serialLink.in_waiting == 5):
                    self.readBytes = self.serialLink.read(5).decode('utf-8')
                    return self.readBytes[2:3]
                else:
                    time.sleep(0.01)
        return -1        
    
    def movePosition(self, pos_um, pos_nm):
        """
        Move piezo to a specific position.
        
        Parameters
        ----------
        pos_um : INT
            um value of the piezo motion
            
        pos_nm : INT
            nm value of the piezo motion
        
        Returns
        -------
        None.

        """
        if((pos_um < 0) or (pos_um) > 10):
            return False
        if((pos_nm < 0) or (pos_nm > 999)):
            return False
        
        data = '_M'
        if(pos_um < 10):
            data+= ' '+str(pos_um)+'.'
        else:
            data+= str(pos_um)+'.'
        
        if(pos_nm < 10):
            data+= '  '+str(pos_nm)+'!'
        elif(pos_nm < 100):
            data+= ' '+str(pos_nm)+'!'
        else:
            data+= str(pos_nm)+'!'
        
        if(self.connected):
            try:
                self.serialLink.write(data.encode())
            except:
                print('Error Sending - movePosition') 
            # Timeout / 1 s
            for k in range(10):
                if(self.serialLink.in_waiting == 4):
                    self.readBytes = self.serialLink.read(4).decode('utf-8')
                    if(self.readBytes[2] == '1'):
                        return True
                    else:
                        return False
                else:
                    time.sleep(0.02)
        return False
    