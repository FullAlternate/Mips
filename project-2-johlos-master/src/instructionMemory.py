'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
from memory import Memory

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
    # Remove this and replace with your implementation!
    raise AssertionError("writeOutput not implemented in class InstructionMemory!");
