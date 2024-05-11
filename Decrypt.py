"""
Script Description : Extracts decrypted global-metadata.dat from AFK Journey using NEP2 debug strings.
Code Author : ElCapor
Code Author Profile : https://www.unknowncheats.me/forum/members/4547094.html / https://github.com/ElCapor
Note: Made minor tweaks for my own purposes, Logic owned by Code Author
"""
import os
import time
from elevate import elevate
import windbgmon
import pymem

class Exploit:
    def __init__(self, ProgramName=None):
        self.ProgramName = ProgramName
        self.Program = pymem.Pymem()
        self.Addresses = {}
        
        if type(ProgramName) == str:
            self.Program = pymem.Pymem(ProgramName)
        elif type(ProgramName) == int:
            self.Program.open_process_from_id(ProgramName)
            
    def h2d(self, hz: str) -> int:
        if type(hz) == int:
            return hz
        return int(hz, 16)
    
    def d2h(self, dc: int) -> str:
        if type(dc) == str:
            return dc
        if abs(dc) > 4294967295:
            dc = hex(dc & (2**64-1)).replace('0x','')
        else:
            dc = hex(dc & (2**32-1)).replace('0x','')
        if len(dc) > 8:
            while len(dc) < 16:
                dc = '0' + dc
        if len(dc) < 8:
            while len(dc) < 8:
                dc = '0' + dc
        return dc

class NEP2Parser:
    def __init__(self):
        self.NEP2String = "NEP2"
        self.decryptStr = "new code at "
        self.addressSize = 16
        self.decryptAddress = ""
        self.sizeAddress = ""
        self.sizeStr = "dataSize  is "
    
    def ParseDecrypt(self, msg):
        if msg.startswith(self.NEP2String):
            index = msg.find(self.decryptStr)
            if index != -1:
                index += len(self.decryptStr)
                self.decryptAddress = msg[index:]
                return True
        return False
        
    def ParseSize(self, msg):
        if msg.startswith(self.NEP2String):
            index = msg.find(self.sizeStr)
            if index != -1:
                index += len(self.sizeStr)
                self.sizeAddress = msg[index:]
                return True
        return False
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        pass

def main():
    flag1 = False
    flag2 = False
    with NEP2Parser() as parser:
        with windbgmon.DbgMon() as dbgmon:
            for pid, msg in dbgmon:
                print(f"[{pid}] {msg}")
                if parser.ParseDecrypt(msg):
                    flag1 = True
                if parser.ParseSize(msg):
                    flag2 = True
                if flag1 and flag2:
                    dbgmon.stop()
    
    print(f"Got address {parser.decryptAddress} and data size {parser.sizeAddress}")
    print("Giving the game 5 seconds to start up")
    time.sleep(5)
    
    game = Exploit("AFK Journey.exe")
    dataAddr = game.h2d(parser.decryptAddress)
    sizeAddr = game.h2d(parser.sizeAddress)
    bytes_data = game.Program.read_bytes(dataAddr, sizeAddr)
    
    file_path = os.path.join(os.getcwd(), "decrypted-global-metadata.dat")
    
    comp = bool(input("Would you like to make the dump compatible with il2cpp dumper, bepinex, etc? (0 = false or 1 = true), default = 1: ") or True)
    if comp:
        mutable_bytes = bytearray(bytes_data)
        mutable_bytes[4:8] = bytearray([0x1D, 0x0, 0x0, 0x0])
        bytes_data_modified = bytes(mutable_bytes)
        bytes_data = bytes_data_modified
    
    with open(file_path, "wb") as metadata:
        metadata.write(bytes_data)

if __name__ == "__main__":
    elevate()
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
    t = input("Press any key to exit")