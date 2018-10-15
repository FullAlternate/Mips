'''
Code written for inf-2200, University of Tromso
'''

from pc import PC
from add import Add
from mux import Mux
from registerFile import RegisterFile
from instructionMemory import InstructionMemory
from dataMemory import DataMemory
from constant import Constant
from splitter import Splitter
from mainControl import MainControl
from alu import ALU
from signExtender import SignExtender
from AND import AndGate
from leftShiftTwo import LeftShiftTwo
from jmpAddress import JMPAddress
from breaker import Breaker
from branchADD import BranchAdd
from randomControl import RandomControl

class MIPSSimulator():
  '''Main class for MIPS pipeline simulator.
  
  Provides the main method tick(), which runs pipeline
  for one clock cycle.
  
  '''
  def __init__(self, memoryFile):
    self.nCycles = 0 # Used to hold number of clock cycles spent executing instructions
    
    self.dataMemory = DataMemory(memoryFile)
    self.instructionMemory = InstructionMemory(memoryFile)
    self.registerFile = RegisterFile()
    self.alu = ALU()
    self.mainControl = MainControl()
    self.splitter = Splitter()
    self.signExtender = SignExtender()
    self.andGate = AndGate()
    self.breaker = Breaker()

    self.constant4 = Constant(4)
    # self.randomControl = RandomControl()
    self.pcMux1 = Mux()
    self.pcMux2 = Mux()
    self.regMux = Mux()
    self.aluMux = Mux()
    self.resultMux = Mux()
    self.luiMux = Mux()

    self.adder = Add()
    self.branchAdder = Add()

    self.jumpAddress = JMPAddress()
    self.shiftBranch = LeftShiftTwo()
    self.shiftJump = LeftShiftTwo()

    self.pc = PC(hex(0xbfc00000))  # hard coded "boot" address
    
    self.elements = [self.constant4, self.adder, self.instructionMemory, self.breaker, self.splitter,
                     self.shiftJump, self.mainControl, self.regMux, self.signExtender, self.luiMux, self.registerFile,
                     self.jumpAddress, self.shiftBranch, self.branchAdder, self.aluMux, self.alu, self.dataMemory,
                     self.andGate, self.pcMux1, self.pcMux2, self.resultMux, self.registerFile, self.pc]
    
    self._connectCPUElements()
    
  def _connectCPUElements(self):
    
    self.constant4.connect(
      [],
      ['constant'],
      [],
      []
    )
    
    self.adder.connect(
      [(self.pc, 'pcAddress'), (self.constant4, 'constant')],
      ['sum'],
      [],
      []
    )
    
    self.pcMux2.connect(
      [(self.pcMux1, "ResultMux2"), (self.jumpAddress, "Result")],
      ['muxOut'],
      [(self.mainControl, "JmpCtrl")],
      []
    )
    
    self.pc.connect(
      [(self.pcMux2, 'muxOut')],
      ['pcAddress'],
      [],
      []
    )

    self.instructionMemory.connect(
      [(self.pc, "pcAddress")],
      ["instruction"],
      [],
      []
    )

    self.splitter.connect(
      [(self.breaker, "Instruction")],
      ["31-0", "25-21", "20-16", "15-11", "15-0", "25-0"],
      [],
      []
    )

    self.mainControl.connect(
      [(self.splitter, "31-0")],
      [],
      [],
      ["RegDst", "RegWrite", "ALUSrc", "ALUOp", "MemWrite", "MemtoReg", "MemRead", "ALUType", "AndGate", "JmpCtrl",
       "LuiCtrl"]
    )

    self.regMux.connect(
      [(self.splitter, "20-16"), (self.splitter, "15-11")],
      ["WReg"],
      [(self.mainControl, "RegDst")],
      []
    )

    self.registerFile.connect(
      [(self.splitter, "25-21"), (self.splitter, "20-16"), (self.regMux, "WReg"), (self.resultMux, "WriteData")],
      ["Read1", "Read2"],
      [(self.mainControl, "RegWrite")],
      []
    )

    self.signExtender.connect(
      [(self.splitter, "15-0")],
      ["ExtendedValue"],
      [],
      []
    )

    self.aluMux.connect(
      [(self.registerFile, "Read2"), (self.luiMux, "LuiOutput")],
      ["RightOp"],
      [(self.mainControl, "ALUSrc")],
      []
    )

    self.alu.connect(
      [(self.registerFile, "Read1"), (self.aluMux, "RightOp")],
      ["Result"],
      [(self.mainControl, "ALUOp"), (self.mainControl, "ALUSrc")],
      ["Zero"]
    )

    self.dataMemory.connect(
      [(self.alu, "Result"), (self.registerFile, "Read2")],
      ["ReadData"],
      [(self.mainControl, "MemWrite"), (self.mainControl, "MemRead")],
      []
    )

    self.resultMux.connect(
      [(self.alu, "Result"), (self.dataMemory, "ReadData")],
      ["WriteData"],
      [(self.mainControl, "MemtoReg")],
      []
    )

    self.andGate.connect(
      [],
      [],
      [(self.mainControl, "AndGate"), (self.alu, "Zero")],
      ["PCMuxSelect"]
    )

    self.shiftBranch.connect(
      [(self.signExtender, "ExtendedValue")],
      ["ShiftedValue"],
      [],
      []
    )

    self.branchAdder.connect(
      [(self.adder, "sum"), (self.shiftBranch, "ShiftedValue")],
      ["branchSum"],
      [],
      []
    )

    self.pcMux1.connect(
      [(self.adder, "sum"), (self.branchAdder, "branchSum")],
      ["ResultMux2"],
      [(self.andGate, "PCMuxSelect")],
      []
    )

    self.shiftJump.connect(
      [(self.splitter, "25-0")],
      ["ShiftedValue"],
      [],
      []
    )

    self.jumpAddress.connect(
      [(self.shiftJump, "ShiftedValue"), (self.adder, "sum")],
      ["Result"],
      [],
      []
    )

    self.breaker.connect(
      [(self.instructionMemory, "instruction")],
      ["Instruction"],
      [],
      []
    )

    self.luiMux.connect(
      [(self.signExtender, "ExtendedValue"), (self.splitter, "15-0")],
      ["LuiOutput"],
      [(self.mainControl, "LuiCtrl")],
      []
    )
    
  def clockCycles(self):
    '''Returns the number of clock cycles spent executing instructions.'''
    
    return self.nCycles
  
  def dataMemory(self):
    '''Returns dictionary, mapping memory addresses to data, holding
    data memory after instructions have finished executing.'''
    
    return self.dataMemory.memory
  
  def registerFile(self):
    '''Returns dictionary, mapping register numbers to data, holding
    register file after instructions have finished executing.'''
    
    return self.registerFile.register
  
  #def printDataMemory(self):
    #self.dataMemory.printAll()
  
  #def printRegisterFile(self):
    #self.registerFile.printAll()
  
  def tick(self):
    '''Execute one clock cycle of pipeline.'''
    
    self.nCycles += 1
    
    # The following is just a small sample implementation
    
    self.pc.writeOutput()
    
    for elem in self.elements:
      elem.readControlSignals()
      elem.readInput()
      elem.writeOutput()
      elem.setControlSignals()
    
    self.pc.readInput()
