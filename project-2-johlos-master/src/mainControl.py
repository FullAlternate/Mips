import unittest
from testElement import TestElement
from alu import ALU
from cpuElement import CPUElement
import random

class MainControl(CPUElement):
  '''
  Random control unit. It randomly sets it's output signal
  '''
  def connect(self, inputSources, outputValueNames, control, outputSignalNames):
    CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

    assert(len(inputSources) == 1), 'Random control has one input'
    assert(len(outputValueNames) == 0), 'Random control does not have output'
    assert(len(control) == 0), 'Random control does not have any control signals'
    assert(len(outputSignalNames) == 11), 'Random control has eleven control outputs'

    self.input_Instruction = inputSources[0][1]
    self.signal_Regdest = outputSignalNames[0]
    self.signal_Regwrite = outputSignalNames[1]
    self.signal_ALUsrc = outputSignalNames[2]
    self.signal_ALUop = outputSignalNames[3]
    self.signal_Memwrite = outputSignalNames[4]
    self.signal_Memtoreg = outputSignalNames[5]
    self.signal_Memread = outputSignalNames[6]
    self.signal_ALUtype = outputSignalNames[7]
    self.signal_Andgate = outputSignalNames[8]
    self.signal_Jmpctrl = outputSignalNames[9]
    self.signal_Luictrl = outputSignalNames[10]

  def writeOutput(self):
    pass # randomControl has no data output

  def setControlSignals(self):
      self.outputControlSignals[self.signal_Andgate] = 0
      self.outputControlSignals[self.signal_Jmpctrl] = 0
      input = self.inputValues[self.input_Instruction]
      binary = input[2:]
      opcode = binary[:6]
      if opcode == "000000":
          funct = binary[-6:]
          self.outputControlSignals[self.signal_Regdest] = 1
          self.outputControlSignals[self.signal_Regwrite] = 1
          self.outputControlSignals[self.signal_ALUsrc] = 0
          self.outputControlSignals[self.signal_ALUop] = funct
          self.outputControlSignals[self.signal_Memwrite] = 0
          self.outputControlSignals[self.signal_Memtoreg] = 0
          self.outputControlSignals[self.signal_Memread] = 0
          self.outputControlSignals[self.signal_ALUtype] = 0
          self.outputControlSignals[self.signal_Luictrl] = 0
          if funct == "100000":
              print("ADD")
          elif funct == "100001":
              print("ADDU")
          elif funct == "100010":
              print("SUB")
          elif funct == "100011":
              print("SUBU")
          elif funct == "100100":
              print("AND")
          elif funct =="100101":
              print("OR")
          elif funct == "100111":
              print("NOR")
          elif funct == "101010":
              print("SLT")
          elif funct == "001101":
              print("BREAK")
      elif opcode == "000010":
          print("J")
          self.outputControlSignals[self.signal_Regdest] = 0
          self.outputControlSignals[self.signal_Regwrite] = 0
          self.outputControlSignals[self.signal_ALUsrc] = 0
          self.outputControlSignals[self.signal_ALUop] = opcode
          self.outputControlSignals[self.signal_Memwrite] = 0
          self.outputControlSignals[self.signal_Memtoreg] = 0
          self.outputControlSignals[self.signal_Memread] = 0
          self.outputControlSignals[self.signal_ALUtype] = 0
          self.outputControlSignals[self.signal_Andgate] = 0
          self.outputControlSignals[self.signal_Jmpctrl] = 1
          self.outputControlSignals[self.signal_Luictrl] = 0
      elif opcode == "000100":
          print("BEQ")
          self.outputControlSignals[self.signal_Regdest] = 0
          self.outputControlSignals[self.signal_Regwrite] = 0
          self.outputControlSignals[self.signal_ALUsrc] = 1
          self.outputControlSignals[self.signal_ALUop] = opcode
          self.outputControlSignals[self.signal_Memwrite] = 0
          self.outputControlSignals[self.signal_Memtoreg] = 0
          self.outputControlSignals[self.signal_Memread] = 0
          self.outputControlSignals[self.signal_ALUtype] = 1
          self.outputControlSignals[self.signal_Andgate] = 1
          self.outputControlSignals[self.signal_Luictrl] = 0
      elif opcode == "000101":
          print("BNE")
          self.outputControlSignals[self.signal_Regdest] = 0
          self.outputControlSignals[self.signal_Regwrite] = 0
          self.outputControlSignals[self.signal_ALUsrc] = 1
          self.outputControlSignals[self.signal_ALUop] = opcode
          self.outputControlSignals[self.signal_Memwrite] = 0
          self.outputControlSignals[self.signal_Memtoreg] = 0
          self.outputControlSignals[self.signal_Memread] = 0
          self.outputControlSignals[self.signal_ALUtype] = 1
          self.outputControlSignals[self.signal_Andgate] = 1
          self.outputControlSignals[self.signal_Luictrl] = 0
      elif opcode == "001111":
          print("LUI")
          self.outputControlSignals[self.signal_Regdest] = 0
          self.outputControlSignals[self.signal_Regwrite] = 1
          self.outputControlSignals[self.signal_ALUsrc] = 1
          self.outputControlSignals[self.signal_ALUop] = opcode
          self.outputControlSignals[self.signal_Memwrite] = 0
          self.outputControlSignals[self.signal_Memtoreg] = 0
          self.outputControlSignals[self.signal_Memread] = 0
          self.outputControlSignals[self.signal_ALUtype] = 1
          self.outputControlSignals[self.signal_Andgate] = 0
          self.outputControlSignals[self.signal_Luictrl] = 1

      elif opcode == "100011":
          print("LW")
          self.outputControlSignals[self.signal_Regdest] = 1
          self.outputControlSignals[self.signal_Regwrite] = 1
          self.outputControlSignals[self.signal_ALUsrc] = 1
          self.outputControlSignals[self.signal_ALUop] = opcode
          self.outputControlSignals[self.signal_Memwrite] = 0
          self.outputControlSignals[self.signal_Memtoreg] = 1
          self.outputControlSignals[self.signal_Memread] = 1
          self.outputControlSignals[self.signal_ALUtype] = 1
          self.outputControlSignals[self.signal_Luictrl] = 0
      elif opcode == "101011":
          print("SW")
          self.outputControlSignals[self.signal_Regdest] = 1
          self.outputControlSignals[self.signal_Regwrite] = 1
          self.outputControlSignals[self.signal_ALUsrc] = 1
          self.outputControlSignals[self.signal_ALUop] = opcode
          self.outputControlSignals[self.signal_Memwrite] = 1
          self.outputControlSignals[self.signal_Memtoreg] = 1 # ???
          self.outputControlSignals[self.signal_Memread] = 0
          self.outputControlSignals[self.signal_ALUtype] = 1
          self.outputControlSignals[self.signal_Luictrl] = 0
      elif opcode == "001000":
          print("ADDI")
          self.outputControlSignals[self.signal_Regdest] = 0
          self.outputControlSignals[self.signal_Regwrite] = 1
          self.outputControlSignals[self.signal_ALUsrc] = 1
          self.outputControlSignals[self.signal_ALUop] = opcode
          self.outputControlSignals[self.signal_Memwrite] = 0
          self.outputControlSignals[self.signal_Memtoreg] = 0
          self.outputControlSignals[self.signal_Memread] = 0
          self.outputControlSignals[self.signal_ALUtype] = 1
          self.outputControlSignals[self.signal_Luictrl] = 0
      elif opcode == "001001":
          print("ADDIU")
          self.outputControlSignals[self.signal_Regdest] = 0
          self.outputControlSignals[self.signal_Regwrite] = 1
          self.outputControlSignals[self.signal_ALUsrc] = 1
          self.outputControlSignals[self.signal_ALUop] = opcode
          self.outputControlSignals[self.signal_Memwrite] = 0
          self.outputControlSignals[self.signal_Memtoreg] = 0
          self.outputControlSignals[self.signal_Memread] = 0
          self.outputControlSignals[self.signal_ALUtype] = 1
          self.outputControlSignals[self.signal_Luictrl] = 0

class TestDataFile(unittest.TestCase):
  def setUp(self):
    self.controlunit = MainControl()
    self.testInput = TestElement()
    self.testOutput = TestElement()
    self.testALU = ALU()

    self.testInput.connect(
      [],
      ["Instruction"],
      [],
      []
    )

    self.controlunit.connect(
      [(self.testInput, "Instruction")],
      [],
      [],
      ["Regdest", "Regwrite", "ALUsrc", "ALUop", "ALUtype", "Memwrite",
       "Memtoreg", "Memread", "Andgate", "Jmpctr"]
    )

    self.testOutput.connect(
      [],
      [],
      [(self.controlunit, "Regdest"), (self.controlunit, "Regwrite"),
       (self.controlunit, "ALUsrc"), (self.controlunit, "ALUop"),
       (self.controlunit, "Memwrite"), (self.controlunit, "Memtoreg"),
       (self.controlunit, "Memread"), (self.controlunit, "ALUtype"),
       (self.controlunit, "Andgate"), (self.controlunit, "Jmpctrl")],
      []
    )


  def test_correct_behavior(self):
      self.testInput.setOutputValue("Instruction", hex(0x01495020))
      self.controlunit.readInput()
      self.controlunit.setControlSignals()
      self.testOutput.readInput()


if __name__ == '__main__':
  unittest.main()
