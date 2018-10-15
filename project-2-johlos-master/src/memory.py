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

    f = open(filename, "r")

    current_address = "0x0"
    for line in f:
      file_data = line.split("\t")
      if file_data[0][0] != "\n":
        # print(file_data)
        if file_data[0][0] != "#":
          self.memory[file_data[0]] = file_data[1]

        self.endAddress = file_data[0]
    f.close()

    for i in range(10000):
      if current_address in self.memory.keys():
        pass

      else:
        self.memory[current_address] = 0

      current_address = hex(int(current_address, 16) + 4)
      #print(current_address)


    #print(self.memory)


    # Remove this and replace with your implementation!
    # Implementation MUST populate the dictionary in self.memory!
    #raise AssertionError("initializeMemory not implemented in class Memory!");
    
  #def printAll(self):
    #for key in sorted(self.memory):
      #print((hex(int(key))[:-1] + "\t" + common.fromUnsignedWordToSignedWord(self.memory[key]) + "\t" + "(", hex(int(self.memory[key]))[:-1]) + ")")


class TestMemory(unittest.TestCase):
  def setUp(self):
    self.memory = Memory("add.mem")
    self.file = open("add.mem", "r")
    self.mem_adr = None
    self.bi_code = None

  def test_correct_behavior(self):
    for line in self.file:
      current_data = line.split("\t")

      if current_data[0][0] != "#":
        self.mem_adr = current_data[0]
        self.bi_code = current_data[1]

        # print("mem: ", self.mem_adr)
        # print("binary: ", self.bi_code)
    test_case = self.memory.memory[self.mem_adr]
    self.assertEqual(test_case, self.bi_code)

    self.file.close()


if __name__ == '__main__':
  unittest.main()

