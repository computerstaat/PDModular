import socket
import select
import sys
import thread
import mido
import OSC
import glob
import time

#import Adafruit_CharLCD as LCD


NEWPATCH = 3
READY = 1
TYPELENGTH = 8

DEFAULTSYNTH = "synth1"
MIDIDEVICE = "MPKmini2 MIDI 1"
DEFAULTPATCH = "synth1"

MIDI_ON = "note_on"
MIDI_OFF = "note_off"
MIDI_PARAM = "control_change"
MIDI_WHEEL = "pitchwheel"


class VoiceManager():
    def __init__(self, maxVoices, ip, port):
        self.playing = []
        self.ip = ip
        self.port = port
        self.osc = OSC.OSCClient()
        self.osc.connect((ip, port))

    def play(self, note, velocity):
        self.playing.append(note)
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress("/PLAY/MIDI")
        oscmsg.append(note)
        oscmsg.append(velocity)
        self.osc.send(oscmsg)

    def stop(self, note):
        self.playing.remove(note)
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress("/PLAY/MIDI")
        oscmsg.append(note)
        oscmsg.append(0)
        self.osc.send(oscmsg)

    def control(self, value, path):
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress("/CONTROL/" + path)
        oscmsg.append(value)
        self.osc.send(oscmsg)

    def load(self, patch):
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress("/LOAD")
        oscmsg.append(patch)
        self.osc.send(oscmsg)


class Conductor():
    def __init__(self):
        self.voiceManagers = []
        #self.lcd = LCD.Adafruit_CharLCDPlate()
        #self.keyb = mido.open_input(MIDIDEVICE)
        self.synthesizers = self.getAllPatches()
        self.midiToOSC = self.loadMidiToOSC(DEFAULTPATCH)
        self.defaults = self.loadDefaults(DEFAULTPATCH)
        self.currentPatch = DEFAULTPATCH
        self.LCDcounter = 0

    ##simple implementation of round robbin could be optimized to use ring buffer instead
    def play(self, note, velocity):
        vm = self.voiceManagers.pop(0)
        vm.play(note, velocity)
        self.voiceManagers.append(vm)

    def stop(self, note):
        for vm in self.voiceManagers:
            if note in vm.playing:
                vm.stop(note)
                return

    def load(self, patch):
        for vm in self.voiceManagers:
            vm.load(patch)
        sleep(1)
        self.midiToOSC = self.loadMidiToOSC(patch)
        self.loadDefaults(patch)
        self.setDefaultsAll()

    def control(self, cc, value):
        path = self.midiToOSC[cc]
        for vm in self.voiceManagers:
            vm.control(value, path)

    def loadMidiToOSC(self, patch):
        file = open("./Patches/" + patch + ".properties", 'r')
        midiToOSC = {}
        for line in file:
            line = line.split()
            midiToOSC[line[0]] = line[1]
        return midiToOSC


    def loadDefaults(self, patch):
        file = open("./Patches/" + patch +".defaults", 'r')
        defaults = {}
        for line in file:
            line = line.split()
            defaults[line[0]] = line[1]
        return defaults

    def setDefaultsAll(self):
        for path,value in self.defaults.iteritems():
            for voiceManager in self.VoiceManagers:
                voiceManager.control(value,path)


    def setDefaultsOne(self, voiceManager):
        for path,value in self.defaults.iteritems():
            voiceManager.control(value,path)

    def loadSynthesizer(self, patch):
        self.load(patch)


    def getAllPatches(self):
        synths = []
        files = glob.glob("/Users/jerett/Documents/Tufts Server/Project/Patches/*.pd")
        for f in files:
            synths.append(f.split('/')[-1][0:-3])
        synths.remove("voiceMaster")
        return synths

    def LCDchecker():
        if lcd.is_pressed(LCD.SELECT):
            print "SELECT"
            lcd.clear()
            name = self.synthesizers[self.LCDcounter]
            lcd.message("[" + name + "]")
            self.loadSynthesizer(name)
        # elif lcd.is_pressed(LCD.LEFT):
        #     lcd.clear()
        # elif lcd.is_pressed(LCD.RIGHT):
        #     lcd.clear()
        elif lcd.is_pressed(LCD.UP):
            print "UP"
            lcd.clear()
            self.LCDcounter = max(self.LCDcounter - 1, 0)
            name = self.synthesizers[self.LCDcounter]
            if(name == self.currentPatch):
                name = "[" + name + "]"
            lcd.message(name)

        elif lcd.is_pressed(LCD.DOWN):
            print "DOWN"
            lcd.clear()
            self.LCDcounter = min(self.LCDcounter + 1, len(self.synthesizers))
            name = self.synthesizers[self.LCDcounter]
            if(name == self.currentPatch):
                name = "[" + name + "]"
            lcd.message(name)

    # This needs to parse message correctly
    def midiCheck():
        for message in self.keyb:
            if message.type == MIDI_ON:
                print "ON"
                self.play(message.note, message.velocity)
            elif message.type == MIDI_OFF:
                print "OFF"
                self.stop(message.note)
            elif message.type == MIDI_PARAM:
                print "PARAM"
                self.control(message.cc, message.value)

    def mainLoop(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.bind(("localhost", 9999))
        server.listen(10)
        inputs = [server]
        lcd.message("["+ DEFAULTPATCH+ "]")
        while inputs:
            self.midiCheck()
            self.LCDchecker()
            readable, _, _ = select.select(inputs, [], [])
            for s in readable:
                if s == server:
                    connection, client_address = s.accept()
                    messageType = s.recv(TYPELENGTH)
                    if(messageType == READY):
                        maxVoices = int(s.recv(intLength))
                        vMPort = s.recv(ipLength)
                        newVM = VoiceManager( maxVoices, client_address, vMPort)
                        newVM.load(self.currentPatch)
                        self.setDefaultsOne(newVM)
                        voiceManagers.append(newVM)
                        inputs.append(connection)


c = Conductor()
c.load
print c.defaults
print c.midiToOSC
c.mainLoop()
