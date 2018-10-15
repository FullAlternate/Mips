'''
Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
import common
from testElement import TestElement

class RegisterFile(CPUElement):
  def __init__(self):
    # Dictionary mapping register number to register value
    self.register = {}

    # All registers default to 0
    for i in range(0, 32):
      self.register[i] = format(0, "#034b")

  def connect(self, inputSources, outputValueNames, control, outputSignalNames):
    CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

    # Implement me!
    assert (len(inputSources) == 4), 'Registers should have four inputs'
    assert (len(outputValueNames) == 2), 'Registers has two outputs'
    assert (len(control) == 1), 'Registers only have one control signal'
    assert (len(outputSignalNames) == 0), 'Registers does not have any control output'

    self.input_Register1 = inputSources[0][1]
    self.input_Register2 = inputSources[1][1]
    self.input_Writeregister = inputSources[2][1]
    self.input_Writedata = inputSources[3][1]
    self.controlRegwrite = control[0][1]
    self.output_Read1 = outputValueNames[0]
    self.output_Read2 = outputValueNames[1]
    # Notice me senpai :3

  def printAll(self):
    '''
    Print the name and value in each register.
    '''

    # Note that we won't actually use all the registers listed here...
    registerNames = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                      '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                      '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                      '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']

   # print ("Register file")
   # print ("================")
    #for i in range(0, 32):
     # print  ("%s \t=> %s (%s)" % (registerNames[i], common.fromUnsignedWordToSignedWord(self.register[i]), hex(long(self.register[i]))[:-1]))
    #print ("================")

  def writeOutput(self):
    regControl = self.controlSignals[self.controlRegwrite]

    assert (isinstance(regControl, int))
    assert (not isinstance(regControl, bool))  # ...  (not bool)
    assert (regControl == 0 or regControl == 1), ("Invalid mux control signal value: ", regControl)

    self.outputValues[self.output_Read1] = self.register[int(self.inputValues[self.input_Register1], 2)]
    self.outputValues[self.output_Read2] = self.register[int(self.inputValues[self.input_Register2], 2)]

    # print(regControl)

    print("REG - t1: ", self.register[9])
    print("REG - t3: ", self.register[11])

    if regControl == 1:
      self.register[int(self.inputValues[self.input_Writeregister], 2)] = self.inputValues[self.input_Writedata]

class TestRegisterFile(unittest.TestCase):
  def setUp(self):
    self.regFile = RegisterFile()
    self.testInput = TestElement()
    self.testOutput = TestElement()

    self.testInput.connect(
      [],
      ["Reg1", "Reg2", "WReg", "WData"],
      [],
      ["RegControl"]
    )

    self.regFile.connect(
      [(self.testInput, "Reg1"), (self.testInput, "Reg2"), (self.testInput, "WReg"), (self.testInput, "WData")],
      ["Data1", "Data2"],
      [(self.testInput, "RegControl")],
      []
    )

    self.testOutput.connect(
      [(self.regFile, "Data1"), (self.regFile, "Data2")],
      [],
      [],
      []
    )

  def test_correct_behavior(self):
    self.regFile.register[0] = 10
    self.regFile.register[1] = 20

    self.testInput.setOutputValue("Reg1", bin(0))
    self.testInput.setOutputValue('Reg2', bin(1))
    self.testInput.setOutputValue("WReg", bin(0))
    self.testInput.setOutputValue('WData', bin(5))

    self.testInput.setOutputControl("RegControl", 0)

    self.regFile.readInput()
    self.regFile.readControlSignals()
    self.regFile.writeOutput()
    self.testOutput.readInput()
    output1 = self.testOutput.inputValues["Data1"]
    output2 = self.testOutput.inputValues["Data2"]

    self.assertEqual(output1, 10)
    self.assertEqual(output2, 20)
    self.assertEqual(self.regFile.register[0], 10)

    self.testInput.setOutputControl('RegControl', 1)

    self.regFile.readInput()
    self.regFile.readControlSignals()
    self.regFile.writeOutput()
    self.testOutput.readInput()
    output1 = self.testOutput.inputValues["Data1"]
    output2 = self.testOutput.inputValues["Data2"]

    self.assertEqual(output1, 10)
    self.assertEqual(output2, 20)
    self.assertEqual(self.regFile.register[0], bin(5))


if __name__ == '__main__':
  unittest.main()
