modules = {"VCO":[
    ["Slider", "FREQ", "frequency"],
    ["Slider", "FINE", "fine"],
    ["List", [["Input", "1V/O"]]],
    ["Slider", "PWM", "pwm"],
    ["Slider", "AMNT", "pwmamount"],
    ["List", [["Input", "CV"]]],
    ["Slider", "FM AMNT", "fmamount1"],
    ["List", [["Input", "CV"]]],
    ["Slider", "FM AMNT", "fmamount2"],
    ["List",[["Input", "CV"]]],
    ["List", [["Output", "SQR"],["Output", "SIN"],["Output", "TRI"],["Output", "RMP"],["Output", "SAW"]]]
  ],
  "VCF": [
    ["List", [["Input", "INPUT"], ["Input", "INPUT"]]],
    ["Slider", "FREQ", "frequency"],
    ["Slider", "AMNT", "fqamount1"],
    ["List", [["Input", "CV"]]],
    ["Slider", "AMNT", "fqamount1"],
    ["List", [["Input", "CV"]]],
    ["Slider", "RES", "resonance"],
    ["Slider", "AMNT", "resamount1"],
    ["List", [["Input", "CV"]]],
    ["Slider", "AMNT", "resamount2"],
    ["List", [["Input", "CV"]]],
    ["List", [["Output", "LP"],["Output", "HP"],["Output", "BP"],["Output", "NP"]]]
  ],
  "KNOBY": [
    ["List", [["Knob", "FOO", "foo"],["Input", "INPUT"],["Knob", "BAR", "bar"],["Output", "OUTPUT"] ]]
  ],
  "SLOPE":[
    ["Slider", "RISE", "rise"],
    ["Slider", "FALL", "fall"],
    ["Slider", "VC", "vc"],
    ["List", [["Input", "1V/O"],["Input", "VC"],["Input", "TRIG"],["Input", "INPUT"]]],
    ["List", [["Output", "GATE"],["Output", "OUT"]]],
  ],
  "SMPL":[
    ["List", [["Input", "IN"],["Input", "GATE"],["Output", "OUT"]]],
  ],
  "SINE":[
    ["Slider", "FREQ", "freq"],
    ["List", [["Input", "1V/O"],["Output", "OUT"]]],
  ],
  "CLOCK":[
    ["Slider", "SPEED", "speed"],
    ["List", [["Output", "OUT"]]],
  ],
  "LPF":[
    ["Slider", "FREQ", "cut"],
    ["Slider", "AMNT", "vcamnt"],
    ["Slider", "RES", "res"],
    ["List", [["Input", "VC"],["Input", "IN"],["Output", "OUT"]]],
  ],
  "BPF":[
    ["Slider", "FREQ", "cut"],
    ["Slider", "FREQ", "res"],
    ["List", [["Input", "IN"],["Output", "OUT"]]],
  ],
  "SWRMP":[
    ["Slider", "FREQ", "freq"],
    ["List", [["Input", "1V/O"],["Output", "RAMP"],["Output", "SAW"]]],
  ],
  "ATN":[
    ["Slider", "AMNT", "amount"],
    ["List", [["Input", "IN"],["Output", "OUT"]]],
  ],
  "BI-ATN":[
    ["Slider", "AMNT", "amount"],
    ["List", [["Input", "IN"],["Output", "OUT"]]],
  ],
  "SQR":[
    ["Slider", "FREQ", "freq"],
    ["Slider", "FREQ", "width"],
    ["List", [["Input", "1V/O"],["Output", "OUT"]]],
  ],
  "SLFO":[
    ["Slider", "FREQ", "freq"],
    ["List", [["Input", "RESET"],["Output", "OUT"]]],
  ],
  "MLFO":[
    ["Slider", "FREQ", "freq"],
    ["List", [["Output", "SINE"],["Output", "SQUARE"],["Output", "SAW"],["Output", "RAMP"],["Output", "TRI"]]],
  ],
  "ADSR": [
    ["List", [["Input", "GATE"]]],
    ["Slider", "A", "attack"],
    ["Slider", "D", "decay"],
    ["Slider", "S", "sustain"],
    ["Slider", "R", "release"],
    ["List",[["Output", "OUT"]]]
  ],
  "VCA": [
    ["Slider", "GAIN", "gain"],
    ["Slider", "AMNT", "amount"],
    ["List", [["Input", "INPUT"],["Input", "ENV"],["Output", "OUT"]]]
  ],
  "MIDI": [
    ["List", [["Output", "PITCH",],["Output", "VLCTY"],["Output", "GATE"]]]
  ],
  "MIXER": [
    ["List", [["Input", "IN 1"],["Input", "IN 2"],["Input", "IN 3"],["Input", "IN 4"]]],
    ["Slider", "LVL 1", "level1"],
    ["Slider", "LVL 2", "level2"],
    ["Slider", "LVL 3", "level3"],
    ["Slider", "LVL 4", "level4"],
    ["Slider", "MIX", "mix"],
    ["List",[["Output", "OUT"]]]
  ],
  "OUT": [
    ["List", [["Input", "RIGHT"]]],
    ["List", [["Input", "LEFT"]]]

  ],
  "DIV": [
    ["List", [["Input", "IN"],["Output", "/2"],["Output", "/3"],["Output", "/4"]]],
    ["List", [["Output", "/5"],["Output", "/6"],["Output", "/7"],["Output", "/8"]]]
  ],
  "GSEQ": [
    ["List", [["Input", "IN"],["Input", "RST"],["Output", "1"],["Output", "2"],["Output", "3"]]],
    ["List", [["Output", "4"],["Output", "4"],["Output", "6"],["Output", "7"],["Output", "8"]]]
  ],
  "VSEQ": [
    ["List", [["Input", "CLOCK"],["Input", "RST"],["Output", "OUT"]]],
    ["Slider", "1", "1"],
    ["Slider", "2", "2"],
    ["Slider", "3", "3"],
    ["Slider", "4", "4"],
    ["Slider", "5", "5"],
    ["Slider", "6", "6"],
    ["Slider", "7", "7"],
    ["Slider", "8", "8"]
  ],
  "NOISE": [
    ["Slider", "FREQ", "freq"],
    ["List", [["Output", "WHITE"],["Output", "PINK"],["Output", "LOW"]]]
  ],
  "INV": [
    ["List", [["Input", "x"],["Output", "not x"]]]
  ],
  "LOGIC": [
    ["List", [["Input", "A"],["Input", "B"]]],
    ["List", [["Output", "AND"],["Output", "NAND"],["Output", "OR"],["Output", "XOR"],["Output", "NOR"]]],
    ["List", [["Input", "C"],["Output", "NOT C"], ["Input", "D"],["Output", "NOT D"]]],
  ]
}
