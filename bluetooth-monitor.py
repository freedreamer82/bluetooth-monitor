#!/usr/bin/env python
from pydbus import SessionBus
from pydbus.generic import signal
from pydbus import SystemBus
from gi.repository import GLib
import subprocess
import ConfigParser
import os
import sys
import time
import commands
from logging.handlers import RotatingFileHandler
import argparse
import signal
import logging


FILELOGSIZE= 1024*10*1024 # 10 mb per 5 file..after that restart again!
DEFAULT_CONFIG_INI = "./config.ini"
global log
g_devices = []

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def sighandler(signum, frame):
    print('\r\nYou pressed Ctrl+C! Game Over...')
    os._exit(0)
    
class BTDevice:
    def __init__(self, name , section):
        self.section = section
        self.mac = name
        self.onconnect = section['onconnect'].strip("\'\"").strip("\"\"")
        self.ondisconnect = section['ondisconnect'].strip("\'\"").strip("\"\"")
        self.hci = section['hci']
        
    def getMacAddress(self):
        return self.mac
    
    def getHci(self):
        self.hci
        
    def getOnConnectScript(self):
        return self.onconnect
    
    def getOnDisconnectScript(self):
        return self.ondiscconnect

    def getDbusObj(self):
        return "/org/bluez/"+self.hci+"/dev_"+self.mac.replace(":","_")

    def onChange(self,interface , changed_properties,invalidated_properties):

        if changed_properties['Connected'] ==  True :
            log.debug("device "+self.mac+ " Connected!") 
            try :
                 result = run_command( self.onconnect )[0]
            except:
                 log.error("Failed running Connect script")
        elif changed_properties['Connected'] == False :
            log.debug("device "+self.mac+ " Disconnected!") 
            try :
                result = run_command( self.ondisconnect )[0]
            except:
                log.error("Failed running Disconnect script")           
    
class ConfigParams:
    def __init__(self, generalSection):
        pass
#        self.delay = int( generalSection['delaysec'] )
#        self.doRemove = str2bool (generalSection['removefile'])
#        self.path = str (generalSection['monitorpath'])

def ConfigSection2Dict(config,section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def run_command(command):
  process = subprocess.Popen(command, shell=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
  stdout = process.communicate()    # execute it, the output goes to the stdout
  exit_code = process.wait()    # when finished, get the exit code
 # print exit_code
  return exit_code == 0,stdout      
      
VERSION         = '7/6/2018'
AUTHOR          = 'SW Engineer Garzola Marco'

parser = argparse.ArgumentParser()
parser.add_argument("-d","--debug", action="store_true", default= False, help="add verbosity")
parser.add_argument("-c","--config", default = DEFAULT_CONFIG_INI ,help=" config file")
parser.add_argument("-l","--log", nargs = 1, metavar =("log File"), default= False, help=" path file to save log")
parser.add_argument('-v', '--version', action='version', version= VERSION  + "\n" +  AUTHOR)

  
if __name__ == '__main__':
    
    signal.signal(signal.SIGINT, sighandler)
    args = parser.parse_args()

    log = logging.getLogger()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    if args.log:
        logging.basicConfig( filename=args.log[0],
                filemode='w',
                format='%(asctime)s,%(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=log_level)
        handler = RotatingFileHandler(args.log[0] ,maxBytes=FILELOGSIZE,backupCount=5)
        log.addHandler(handler)
    else:
        logging.basicConfig(format='%(asctime)s,%(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=log_level)
      #  logging.getLogger().disabled = True
    

    location =  os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(args.config)))
    configFile = os.path.join(location, os.path.basename(args.config) )
    
    config = ConfigParser.ConfigParser()
    config.read(configFile)
   # configParams = ConfigParams( ConfigSection2Dict(config,'general'))
    log.debug( config.sections() )
    bus = SystemBus()

    for d in  config.sections() :
        if d != 'general':
            data = ConfigSection2Dict(config,d)
            btdev = BTDevice(d,data)
            g_devices.append ( btdev )
            log.debug (ConfigSection2Dict(config,d))
            
            log.debug(btdev.getDbusObj())
            bus_session =  bus.get("org.bluez",btdev.getDbusObj())
            bus_session.PropertiesChanged.connect(btdev.onChange)
    
    log.info("starting BT device monitoring");
    loop = GLib.MainLoop()
    loop.run()
