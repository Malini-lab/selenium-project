import webpageupdate as fi
import upgradeanddowngradeloop as up
import sys

def main():
    option=0
    while True:
        print('*'*50)
        try:
            choice='1:Select 1 for same firmware loop update\n2:Select 2 for upgrade and downgrade the loop update\n3:Select 3 for quit\n'
            option=int(input(choice))
        except:
            print("'NOTE:Please enter only the numbers as mentioned'")
            pass
    
        if option ==1:
            fi.main()
            break
        elif option==2:
            up.main()
            break
        elif option==3:
            break
        else:
            print("' NOTE:Please enter only the mentioned  choice'")
            pass
            
       
if __name__=="__main__":
    main()
