import sys
from managementSystem import ManagementSystem

#main system
def main():
    #create an instance of the ManagementSystem class
    ms = ManagementSystem()
    #start of main loop
    while True:
        ms.login_register()
        ms.operations()
main()