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
  "SLOPE":[
    ["Slider", "RISE", "rise"],
    ["Slider", "FALL", "fall"],
    ["Slider", "VC", "vc"],
    ["List", [["Input", "1V/O"],["Input", "VC"],["Input", "TRIG"],["Input", "INPUT"]]],
    ["List", [["Output", "GATE"],["Output", "OUT"]]],
  ],
  "SINE":[
    ["Slider", "FREQ", "freq"],
    ["List", [["Input", "1V/O"],["Output", "OUT"]]],
  ],
  "ATN":[
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
    ["List", [["Output", "OUT"]]],
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
    ["List", [["Input", "INPUT 1"],["Input", "INPUT 2"],["Input", "INPUT 3"],["Input", "INPUT 4"]]],
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
  "NOISE": [
    ["List", [["Output", "WHITE"],["Output", "PINK"],["Output", "LOW"]]]
  ],
  "INV": [
    ["List", [["Input", "x"],["Output", "not x"]]]
  ],
  "LOGIC": [
    ["List", [["Input", "A"],["Input", "B"]]],
    ["List", [["Output", "AND"],["Output", "OR"],["Output", "NOR"],["Output", "NAND"],["Output", "XOR"]]],
    ["List", [["Input", "C"],["Output", "NOT C"], ["Input", "D"],["Output", "NOT D"]]],
  ]
}