import threading
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import serialcommunication as se


# for real path's
IMAGE = os.path.realpath('83_IMAGE_network')
OTA152 = os.path.realpath('castota152.zip')
OTA144 = os.path.realpath('castota144.zip')
OTA136 = os.path.realpath('castota136.zip')
OTA128 = os.path.realpath('castota128.zip')

def ipfromfile():
    try:
        with open("ipfile.txt","r") as f:
            ip=f.read()
            return ip
    except:
        print('"DUT is in off state. Please turn on the DUT. close the terminal and rerun the test"')
        sys.exit(1)
        
def fwversionfromfileone():
    with open("fwversionfromfileone.txt","r") as f:
        fwversion=f.read()
        return fwversion



def ls9imageupdate():
    print('*'*50)
    print('\r\n')
    time.sleep(5)
    print("Launching chrome")
    # driver=webdriver.Chrome()
    # To install chorme driver w.r.t current browser version from the server
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    print("Maximize the window")
    driver.maximize_window()

    # This is for ip adresss from terminal and 1 is for 2nd argument

    print("LS9 firmware update")
    # using '+' symbol we are concatinate the strings.
    
    
    ip1=ipfromfile()
    # driver.get("http://192.168.250.152/index.asp")
    
    try:
        driver.get("http://"+ip1+"/index.asp")
    except:
        #WebDriverWait(driver,60).until(EC.presence_of_element_located((By.XPATH,"//body[contains(text(),'This site can’t be reached')]")))
        return False
   
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"BigFont")))
    print("scroll the window to the down")
        
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    print("Clicking on update")
    WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.ID,"AdvBtn_UPG"))).click()

    if fac==1:
        print("1")
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='factoryreset_checkbox']"))).click()
        print("Factory reset selected")

    else:
        pass

    print("Selecting ls9 image")
    ls=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "fileid")))
    ls.send_keys(IMAGE)

    print("clicking on update")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))).click()
    print("Image is uploading")

    print("clicking on OK")
    #time.sleep(3)
    #driver.find_element(By.NAME,"button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@accesskey='o']"))).click()

    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,"p")))
        print("Firmware is Updating")
    except:
        print("'There is a problem with firmware. Please check the firmware'")
        sys.exit(1)
    
    try:
        WebDriverWait(driver,120).until(EC.presence_of_element_located((By.XPATH,"//body[contains(text(),'100% Completed. Rebooting to Application')]")))
        print("Firmware updated successfully.Now DUT is rebooting")
    except:
        print("'There is a problem with firmware. Please check the firmware'")
        sys.exit(1)
    
    # Rebooting will take 1 min..so here i need to talk with tera term
    time.sleep(60)

    print("Refreshing the page")
    driver.refresh()
    fwversion=fwversionfromfileone()
    print("***LS9 image updated sucessfully and the firmware version is***",fwversion)
    
    time.sleep(10)
    driver.close()
    print('\r\n')

    #WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//div[contains(text(),'Network status : Connected to')]")))
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "BigFont")))
    #print("Scroll down")
    #driver.execute_script("window.scrollTo(0,document.scrollHeight)")
    
def otaimageupdate():
    
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
    #time.sleep(4)
    print("1")
    fwversion=fwversionfromfileone()
    print("2")
    fwversion=fwversion.strip()# it will remove the sapces from ending and starting of the string
    #print(fwversion.startswith('p15'))
    print("3")
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
    driver.close()
    return True

def paralallogs(n):
    se.main(n)
    print("Thread1 completed")
    print('\r\n')

n=0
n2=0

def main():
    global fac
    i=1
    n=0
    count=0
    fac=0
    #ip = l.serialportcomminication()
    while True:
        print('*'*50)
        try:
            n = int(input("Enter how many time u need to update the firmware:"))
            break
        except:
            print('"Hi..Please enter only the digits"')
            pass

    while True:
        print('*'*50)
        options = '1: Type for ls9 image update\n2: Type 2 for chrome image update\n3: Type 3 for both ls9 and chrome image update\n4: Type 4 for quit\n'
        try:
            n2 = int(input(options))

        except:
            print('\n')
            print('"Please enter only the number as mention"')

        if n2 == 1:
            break
        elif n2 == 2:
            break
        elif n2 == 3:
            break
        elif n2 == 4:
            sys.exit(0)
        else:
            print('\n')
            print('"Enter only the mentioned option"')
    
    
    if n2==2:
        print("we can't select the factory reset option in webpage during the chrome update")
        pass
    
    else:
        while True:
            print('*'*50)
            try:
                fac = int(input("You want to do factory reset for the DUT?\n Enter '1' for yes\n Enter '2' for No\n Enter '3' for Quit\n"))
            except:
                print('\n')
                print("Please select only the digits '1' or '2'")
            
            if fac == 1:
                break
            elif fac == 2:
                break
            elif fac == 3:
                exit(0)
            else:
                print('\n')
                print('"Please enter the option 1 or 2"')#   
           
    if n2 == 1:               
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
       
    elif n2 == 2:
        for i in range(n):
            print('*'*50)
            print('\r\n')
            print(f'Iteration number {i} Started')
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(paralallogs,i)
                time.sleep(28)#Chrome update first it will refe the fwvesrion so thread1 it will take time to give the fwversion
                #so gave +10 delay than the ls9 update. 
                executor.submit(otaimageupdate)       
            print('\r\n')
            print(f'Iteration number {i} Completed')
            print('*'*50)
    elif n2 == 3:
        for i in range(n):
            print('*'*50)
            print(f'Iteration number {i} Started')
            print('\r\n')
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(paralallogs,i)
                time.sleep(18)
                executor.submit(ls9imageupdate)

            with ThreadPoolExecutor(max_workers=2) as executor1:
                executor1.submit(paralallogs,i)
                time.sleep(28)
                executor1.submit(otaimageupdate)
            #print('\r\n')
            print(f'Iteration number {i} Completed')
            print('*'*50)
            
if __name__=='__main__':
    main()