'''
Implements base class for memory elements.

Note that since both DataMemory and InstructionMemory are subclasses of the Memory
class, they will read the same memory file containing both instructions and data
memory initially, but the two memory elements are treated separately, each with its
own, isolated copy of the data from the memory file.

Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
import common

class Memory(CPUElement):
  def __init__(self, filename):
  
    # Dictionary mapping memory addresses to data
    # Both key and value must be of type 'long'
    self.memory = {}
    
    self.initializeMemory(filename)
  
  def initializeMemory(self, filename):
    '''
    Helper function that reads initializes the data memory by reading input
    data from a file.
    '''

    with open("fafasf.mem", "r") as f:
      data = f.read()
    # Remove this and replace with your implementation!
    # Implementation MUST populate the dictionary in self.memory!
    raise AssertionError("initializeMemory not implemented in class Memory!");
    
  def printAll(self):
    for key in sorted(self.memory.iterkeys()):
      print "%s\t=> %s\t(%s)" % (hex(long(key))[:-1], common.fromUnsignedWordToSignedWord(self.memory[key]), hex(long(self.memory[key]))[:-1])


class TestMemory(unittest.TestCase):
  def setUp(self):
    self.memory = Memory("add.mem")

  def test_correct_behavior:
    with open("fafasf.mem", "r") as f:
      data = f.readline()
      f.close()

    q = data.split(" ")


