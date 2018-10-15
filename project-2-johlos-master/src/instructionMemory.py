'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
from memory import Memory
from testElement import TestElement


class InstructionMemory(Memory):
  def __init__(self, filename):
    Memory.__init__(self, filename)
  
  def connect(self, inputSources, outputValueNames, control, outputSignalNames):
    CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

    # Remove this and replace with your implementation!
    # raise AssertionError("connect not implemented in class InstructionMemory!");
    assert (len(inputSources) == 1), 'Instruction memory should have one input'
    assert (len(outputValueNames) == 1), 'Instruction memory has only one output'
    assert (len(control) == 0), 'Instruction memory has no control signal'
    assert (len(outputSignalNames) == 0), 'Instruction memory does not have any control output'

    self.input_pcAdress = inputSources[0][1]
    self.output_Instruction = outputValueNames[0]

  def writeOutput(self):

    adress = hex(int(self.inputValues[self.input_pcAdress], 2))

    # print("Adress: ", self.inputValues)
    self.outputValues[self.output_Instruction] = format(int(self.memory[adress], 16)
                                                        , "#034b")
    # print("BiCode: ", self.outputValues)
    # Remove this and replace with your implementation.
    #raise AssertionError("writeOutput not implemented in class InstructionMemory!");


class TestInstructionMemory(unittest.TestCase):
  def setUp(self):
    self.IM = InstructionMemory("add.mem")
    self.testInput = TestElement()
    self.testOutput = TestElement()

    self.testInput.connect(
      [],
      ["Adress"],
      [],
      []
    )

    self.IM.connect(
      [(self.testInput, "Adress")],
      ["Instruction"],
      [],
      []
    )

    self.testOutput.connect(
      [(self.IM, "Instruction")],
      [],
      [],
      []
    )

  def test_correct_behavior(self):
    self.testInput.setOutputValue("Adress", "0b0000000010111111110000000000001000001100")

    self.IM.readInput()
    self.IM.writeOutput()
    self.testOutput.readInput()
    output = self.testOutput.inputValues["Instruction"]

    print(output)

    self.assertEqual(output, format(int(hex(0x8d6b0008), 16), "#034b"))


if __name__ == '__main__':
  unittest.main()
