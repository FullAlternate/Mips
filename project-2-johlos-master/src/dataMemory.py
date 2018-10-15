'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''
import unittest
from testElement import TestElement
from cpuElement import CPUElement
from memory import Memory
import common

class DataMemory(Memory):
  def __init__(self, filename):
    Memory.__init__(self, filename)

  def connect(self, inputSources, outputValueNames, control, outputSignalNames):
    CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

    # Remove this and replace with your implementation!
    #raise AssertionError("connect not implemented in class DataMemory!");

    assert (len(inputSources) == 2), 'Data memory should have two inputs'
    assert (len(outputValueNames) == 1), 'Data memory has only one output'
    assert (len(control) == 2), 'Data memory has two control signal inputs'
    assert (len(outputSignalNames) == 0), 'Data memory does not have any control output'

    self.input_Adress = inputSources[0][1]
    self.input_Data = inputSources[1][1]
    self.controlMemwrite = control[0][1]
    self.controlMemread = control[1][1]
    self.output_Data = outputValueNames[0]

  def writeOutput(self):
      memRead = self.controlSignals[self.controlMemread]

      assert (isinstance(memRead, int))
      assert (not isinstance(memRead, bool))  # ...  (not bool)
      assert (memRead == 0 or memRead == 1), ("Invalid mux control signal value: ", memRead)
      if memRead == 1:
          self.outputValues[self.output_Data] = self.memory[hex(int(self.inputValues[self.input_Adress], 2))]

      memWrite = self.controlSignals[self.controlMemwrite]
      assert (isinstance(memWrite, int))
      assert (not isinstance(memWrite, bool))  # ...  (not bool)
      assert (memWrite == 0 or memWrite == 1), ("Invalid mux control signal value: ", memWrite)
      if memWrite == 1:
          self.memory[hex(int(self.inputValues[self.input_Adress], 2))] = self.inputValues[self.input_Data]

      vxasdasf = 1
    #self.outputValues[self.output_Data] = self.memory[self.inputValues[self.input_Data]]
    #Remove this and replace with your implementation!
    #raise AssertionError("writeOutput not implemented in class DataMemory!");

class TestDataFile(unittest.TestCase):
  def setUp(self):
    self.dataMem = DataMemory("add.mem")
    self.testInput = TestElement()
    self.testOutput = TestElement()

    self.testInput.connect(
      [],
      ["Adress", "WData"],
      [],
      ["MemWrite", "MemRead"]
    )

    self.dataMem.connect(
      [(self.testInput, "Adress"), (self.testInput, "WData")],
      ["RData"],
      [(self.testInput, "MemWrite"), (self.testInput, "MemRead")],
      []
    )

    self.testOutput.connect(
      [(self.dataMem, "RData")],
      [],
      [],
      []
    )

  def test_correct_behavior(self):
      self.testInput.setOutputValue("Adress", hex(0xbfc0020c))
      self.testInput.setOutputValue("WData", hex(5))
      self.testInput.setOutputControl("MemWrite", 0)
      self.testInput.setOutputControl("MemRead", 1)

      self.dataMem.readInput()
      self.dataMem.readControlSignals()
      self.dataMem.writeOutput()
      self.testOutput.readInput()
      output = self.testOutput.inputValues["RData"]
      self.assertEqual(output, hex(0x8d6b0008))

      self.testInput.setOutputControl("MemWrite", 1)
      self.testInput.setOutputControl("MemRead", 0)

      self.dataMem.readInput()
      self.dataMem.readControlSignals()
      self.dataMem.writeOutput()
      self.testOutput.readInput()
      newdata = self.dataMem.memory[hex(0xbfc0020c)]
      self.assertEqual(newdata, hex(5))


if __name__ == '__main__':
  unittest.main()