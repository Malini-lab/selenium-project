
import serial
import os
import time
import sys

print("first")
port1=serial.Serial(port='COM3',baudrate=115200,timeout=5)
word1='OTP_SUCCESS'

def readingthedeviceip():
    print('I\'m inside the teraterm to get the ip')
    # To open serial port
    #port1 = serial.Serial(port='COM6', baudrate=115200, timeout=5)
    word = 'wlan0'  # store the word wlan0 in word
    port1.write("netcfg\r\n".encode('utf-8'))  # write the data "netcfg".\r\n is for new line
    Count = 1
    ip = ""
    while True:  # infinite loop
        # reading the file
        a = port1.readline()
        r = a.decode('utf-8')

        if word in r:  # serching word wlan0 in netcfg(r) if there print that line
            # print(r)
            a = r.split()  # split the line
            ip = a[2].split('/')  # split the /
            if ip[0] == '0.0.0.0':
                print("DUT is not connected to the network. connecting DUT to the network")
                res=configuringdutusinglucicommand()
                return True
                # Don't exit we should call the configure function
            else:
                print("DUT ip is",ip[0])
                with open("ipfile.txt","w") as f:
                    f.write(ip[0])
                break 
                # print(ip[0])#taking 1st argument
                # ip1 = ip[0]
                # print("Ip address of the DUT is",ip1)
             # Once condition satisfied done break
        #Count += 1  # To check at which iteration this condition satified
        # port1.close()
    #with open("ipfile.txt","w") as f:
        #f.write(ip[0])
    #return ip[0] 
    #print("Out sidw of ip fun")

def creatingthedircetoryforlogs():
    #print("inside the directory")
    if os.path.exists('Logs'):
        return os.path.realpath('Logs')
       
    else:
        os.mkdir('Logs')
        return os.path.realpath('Logs')
    print("outside the directory")
# This will create the directory for DUT logs.


def logcapturetillotpsucess(i):
    print("inside logcapture fun")
    port1.write('logcat -c\r\n'.encode('utf-8'))
    port1.write('logcat &\r\n'.encode('utf-8'))
    while True:
        l1=port1.readline()
        l2=l1.decode('unicode-escape')#
        
        
        with open(creatingthedircetoryforlogs()+os.sep+"firmware_Logs"+"_"+str(i)+".txt",'a',encoding='utf-8') as f:
        #It will open a file and it will add the content to that perticular file
            f.write(l2)
        
        if 'OTP_SUCCESS' in l2:
            print("OTP success found and DUT rebooted successfully")
            break
        
     
    '''with open(createdircetorydut()+os.sep+'sinchu.txt','r')as f:
        lr1=f.readline()
        for word1 in lr1:
            return True'''
    
    print("outside logcapture fun")
            


def configuringdutusinglucicommand():
    result = checkingthedutisinsetupmode()
    if result==True:
        print("malini")
        port1.write('LUCI_local 125 FLAT17,newjourney\r\n'.encode('utf-8'))
        time.sleep(18)
        readingthedeviceip()
    else:
        print("DUT is is not going for the setup")


def readingfwversionfromteraterm():
    time.sleep(5)
    print("Going inside the fwfuncton")
    #port2 = serial.Serial(port='COM6', baudrate=115200, timeout=5)
    word2 = 'ENV: Value found FwVersion :'  # store the word wlan0 in word
    port1.write("getenv FwVersion\r\n".encode('utf-8'))  # write the data "netcfg".\r\n is for new line
    Count = 1
    fwversion = ""
    while True:
        # reading the file
        a1 = port1.readline()
        r1 = a1.decode('utf-8')
        if word2 in r1:  # serching word wlan0 in netcfg(r) if there print that line
            b = r1.split()  # spliting the line into list
            print(b[5])  # selecting the eltae using the index from the list
            fwversion = b[5]
            break
        Count += 1  # To check at which iteration this condition satified
    print("outside of fwfun")
    with open("fwversionfromfileone.txt","w") as f:
        f.write(fwversion)
    #return fwversion

def creatingdirectoryforps():
    if os.path.exists('ps'):
        return os.path.realpath('ps')
       
    else:
        os.mkdir('ps')
        return os.path.realpath('ps')
# This will create the directory



def checkingthecastshellserviceafterreboot(fw,i):
    print("going inside the castchecker")
    port1.write("ps\r\n".encode('utf-8'))  # write the data "netcfg".\r\n is for new line
    while True:  # infinite loop
        # reading the sentence line by line so used realine()
        a2 = port1.readline()
        r2 = a2.decode('utf-8')
        
        #print(r2)
        with open(creatingdirectoryforps()+os.sep+fw+'_'+str(i)+".txt","a") as f: 
            f.write(r2)#writing the r2 line by line uisng enter
    
        if 'R ps' in r2:
            break
        if '/system/chrome/cast_shell' in r2:
            break

    print("out of while loop")     
    with open(creatingdirectoryforps()+os.sep+fw+'_'+str(i)+".txt","r") as f:
        data=f.readlines()
        for line in data:
            if '/system/chrome/cast_shell' in line:
                #print("matching")
                return True
        return False 

def checkingthedutisinsetupmode():

    port1.write('netcfg\r\n'.encode('utf-8'))
    dicts = {1: '', 2: '', 3: ''}
    #dictw = {4:''}
    while True:
        read = port1.readline()
        decoded_d = read.decode('utf-8')
        #print(decoded_d)#It will print netcfg status

        if 'wlan0' in decoded_d:
            w0=decoded_d.split()#line splited in to list
            dicts[1]=(w0[2].split("/"))[0]#took 2nd ip and splited agian converted into list and selected the index 0

        if 'p2p0' in decoded_d:
            p0=decoded_d.split()
            dicts[2]=(p0[2].split("/"))[0]#this id for p2p0 ip

        if 'p2p1' in decoded_d:
            p1=decoded_d.split()
            dicts[3]=(p1[2].split("/"))[0]

        if dicts[1].startswith('0') and dicts[2].startswith('192') and dicts[3].startswith('192'):
            return True
        if dicts[1].startswith('0') and dicts[2].startswith('0') and dicts[3].startswith('0'):    
            return True
        if dicts[1].startswith(('192') or ('172')):
            return False

def main(i):
    res=readingthedeviceip()
    print("res is",res)
    time.sleep(1)
    print("After sleep")
    time.sleep(1)
    readingfwversionfromteraterm()
    print("Reading the fw version from 1st")
    logcapturetillotpsucess(i)
    time.sleep(5)
    readingfwversionfromteraterm()
    
    time.sleep(20)
    

if __name__=='__main__':
    main()
    
