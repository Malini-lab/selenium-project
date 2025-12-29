import threading
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import serialcommunication as se
import data as d
import sys
from concurrent.futures import ThreadPoolExecutor

#taking the 1st image path
im1=os.path.realpath('83_IMAGE_network_1')
im2=os.path.realpath('83_IMAGE_network_2')
OTA152 = os.path.realpath('castota152.zip')
OTA144 = os.path.realpath('castota144.zip')
OTA136 = os.path.realpath('castota136.zip')
OTA128 = os.path.realpath('castota128.zip')

#taking second image real path
#i2=os.path.realpath('83_IMAGE_network_2')
#print(i2)

#a=s.fwversion()
def ipfromfile():
    try:
        with open("ipfile.txt","r") as f:
            ip=f.read()
            return ip
    except:
        print('"DUT is in off state. Please turn on the DUT. close the terminal and rerun the test"')
        sys.exit(1)
fwversion=''
def fwversionfromfileone():
    with open("fwversionfromfileone.txt","r") as f:
        fwversion=f.read()
        return fwversion
        

c = 0
def ls9imageupdate():
    global currentfirmware, newversion,ip
    print("Launching chrome")
    # driver=webdriver.Chrome()
    # To install chorme driver w.r.t current browser version from the server
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    print("Maximize the window")
    driver.maximize_window()

    # This is for ip adresss from terminal and 1 is for 2nd argument

    print("LS9 firmware update")
    # using '+' symbol we are concatinate the strings.
    
    #reading the file
    ip1=ipfromfile()
    
    try:
    # driver.get("http://192.168.250.152/index.asp")
        driver.get("http://" + ip1+ "/index.asp")
    except:
        print("'Please check the Laptop network is connected to the same DUT network and close the terminal and rerun the program'")
        sys.exit(1)
        
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "BigFont")))
    print("scroll the window to the down")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    print("Clicking on update")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "AdvBtn_UPG"))).click()

    if fac == 1:
        print("1")
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='factoryreset_checkbox']"))).click()
        print("Factory reset selected")

    else:
        pass

    print("Selecting ls9 image")
    ls = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "fileid")))

    if d.currentfirmware<d.newversion:
        print("selecting 1st path)")
        ls.send_keys(im1)
        c = d.newversion
        d.newversion = d.currentfirmware
        d.currentfirmware = c

    elif d.currentfirmware > d.newversion:
        print("selecting 1st path)")
        ls.send_keys(im2)
        c = d.newversion
        d.newversion = d.currentfirmware
        d.currentfirmware= c
    else:
        print("File not found")

    print("clicking on update")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))).click()
    print("Image is uploading")

    print("clicking on OK")
    # time.sleep(3)
    # driver.find_element(By.NAME,"button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@accesskey='o']"))).click()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        print("Firmware is Updating")
    except:
        print("'There is a problem with firmware. Please check the firmware'")

    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, "//body[contains(text(),'100% Completed. Rebooting to Application')]")))
        print("Firmware updated successfully.Now DUT is rebooting")
    except:
        print("'There is a problem with firmware. Please check the firmware'")

    # Rebooting will take 1 min..so here i need to talk with tera term
    time.sleep(60)

    print("Refreshing the page")
    driver.refresh()
    fwversion=fwversionfromfileone()
    print("***LS9 image updated sucessfully and the firmware version is***",fwversion)
    time.sleep(30)
    print("returning to main fun after 30 sec")
    #return True

def otaimageupdateifcastshellisnotmatcing():
    print("Launching chrome")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    print("Maximize the window")
    driver.maximize_window()

    print("OTA update")
    ip1=ipfromfile()
    # Typing the url in browser
    try:
        driver.get("http://"+ip1+"/chrome_update.asp")
        # driver.get("http://192.168.250.152/chrome_update.asp")
    except:
        return False
        
    # time.sleep(3)
    # ota=driver.find_element(By.ID,"fileid")
    print("selecting the OTA image")
    ota=WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID,"fileid")))

    #Checking the Chrome version from terminal
    fwversion=fwversionfromfileone()
    fwversion=fwversion.strip()# it will remove the sapces from ending and starting of the string
    #print(fwversion.startswith('p15'))
    if fwversion.startswith('p15'):
        print("OTA version is 1.52")
        ota.send_keys(OTA152)
    elif fwversion.startswith('p14'):
        print("OTA version is 1.44")
        ota.send_keys(OTA144)
    elif fwversion.startswith('p13'):
        print("OTA version is 1.36")
        ota.send_keys(OTA136)
    elif fwversion.startswith('p12'):
        print("OTA version is 1.28")
        ota.send_keys(OTA128)
    else:
        print("OTA image not found from the path")

    time.sleep(1)
    WebDriverWait(driver,120).until(EC.element_to_be_clickable((By.XPATH,"//input[@type='submit']"))).click()
    print("Chrome image is updating")

    WebDriverWait(driver,60).until(EC.presence_of_element_located((By.XPATH,"//body[contains(text(),'Chrome Update Successful . Rebooting the System')]")))
    print("Chrome update successful. Rebooting the system")

    # netcfg using pyserial
    time.sleep(60)

    driver.refresh()
    print("***Cast firmware updated successfully***")
    time.sleep(10)
    return True

def paralallogs(n):
    se.main(n)
    print("Thread1 completed")
    print('\r\n')


def main():
    global fac
    n=0
    count=0
    i=1
    fac=0
    while True:
        print('*'*50)
        try:
            n = int(input("Enter how many time u need to update the firmware:"))
            break

        except:
            print('"Hi..Please enter only the digits`"')
            pass

    while True:
        print('*'*50)
        try:
            fac = int(input("You want to do factory reset for the DUT?\n Enter '1' for yes\n Enter '2' for No\n Enter '3' for Quit\n"))
            
        except:
            print('\n')
            print("Please select only the digits '1' or '2'")
            pass
            
        if fac == 1:
            break
        elif fac == 2:
            break
        elif fac == 3:
            sys.exit(0)
        else:
            print('\n')
            print('"Please enter the option 1 or 2"')#    

    for i in range(n):     
        print('*'*50)
        print(f'Iteration number {i} Started')
        print('\r\n')
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(paralallogs,i)
            time.sleep(18)
            executor.submit(ls9imageupdate)
        print('\r\n')
        print(f'Iteration number {i} Completed')
        print('*'*50) 
        
        print("m1")
        fw=fwversionfromfileone()
        result=se.checkingthecastshellserviceafterreboot(fw,i)
        if result==True:
            print("cast shell is matching with the ls9 image")
        else:
            print("cast shell is not matching so updating the respective ota package")
            print('*'*50)
            print('\r\n')
            print(f'Iteration number {i} Started')
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(paralallogs,i)
                time.sleep(28)
                executor.submit(otaimageupdateifcastshellisnotmatcing)       
            print('\r\n')
            print(f'Iteration number {i} Completed')
            print('*'*50)
            
        print("m2")

