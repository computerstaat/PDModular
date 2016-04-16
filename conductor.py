import socket
import sys
import thread
import mido
import OSC
import glob

import Adafruit_CharLCD as LCD


NEWPATCH = 3
READY = 1
TYPELENGTH = 8

DEFAULTSYNTH = "synth1"
MIDIDEVICE = "MPKmini2 MIDI 1"

MIDI_ON = "note_on"
MIDI_OFF = "note_off"
MIDI_PARAM = "control_change"
MIDI_WHEEL = "pitchwheel"

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()
keyb = mido.open_input(MIDIDEVICE)
synthesizers = getAllPatches()


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
        self.lcd = LCD.Adafruit_CharLCDPlate()
        self.keyb = mido.open_input(MIDIDEVICE)
        self.synthesizers = self.getAllPatches()
        self.midiToOSC = self.loadMidiToOSC()

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

    def control(self, cc, value):
        path = self.midiToOSC[cc]
        for vm in self.voiceManagers:
            vm.control(value, path)

    def loadMidiToOSC(self, patch):
        file = open(patch + "mtoosc", 'r')
        midiToOSC = {}
        for line in file:
            line = line.split()
            midiToOSC[line[0]] = line[1]
        return midiToOSC


    def setDefaults(self, patch):
        file = open(patch + "defaults", 'r')
        for line in file:
            line = line.split()
            for vm in self.voiceManagers:
                vm.control(line[1], line[0])

    def getAllPatches(self):
        synths = []
        files = glob.glob("/Users/jerett/Documents/Tufts Server/Project/Patches/*.pd")
        for f in files:
            synths.append(f.split('/')[-1][0:-3])
        synths.remove("voiceMaster")
        return synths

    @static_var("counter", 0)
    def LCDchecker():
        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            name = synthesizers[LCDchecker.counter].name
            lcd.message("[" + name + "]")
            loadSynthesizer(name)
        elif lcd.is_pressed(LCD.LEFT):
            lcd.clear()
        elif lcd.is_pressed(LCD.RIGHT):
            lcd.clear()
        elif lcd.is_pressed(LCD.UP):
            lcd.clear()
            LCDchecker.counter = max(LCDchecker.counter - 1, 0)
            lcd.message(synthesizers[LCDchecker.counter].name)
        elif lcd.is_pressed(LCD.DOWN):
            lcd.clear()
            LCDchecker.counter = min(LCDchecker.counter + 1, len(synthesizers))
            lcd.message(synthesizers[LCDchecker.counter].name)

    # This needs to parse message correctly
    def midiCheck():
        for message in self.keyb:
            if message.type == MIDI_ON:
                self.play(message.note, message.velocity)
            elif message.type == MIDI_OFF:
                self.stop(message.note)
            elif message.type == MIDI_PARAM:
                self.control(message.cc, message.value)

    def mainLoop(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.bind(("localhost", 9999))
        server.listen(10)
        inputs = [server]
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
                        voiceManagers.append(VoiceManager(
                            maxVoices, client_address, vMPort))
                        inputs.append(connection)

c = Conductor()
c.mainLoop()

