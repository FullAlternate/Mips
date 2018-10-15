'''
Implements a simple CPU element for adding two integer operands.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement


class BranchAdd(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 2), 'Adder should have two inputs'
        assert (len(outputValueNames) == 1), 'Adder has only one output'
        assert (len(control) == 0), 'Adder should not have any control signal'
        assert (len(outputSignalNames) == 0), 'Adder should not have any control output'

        self.LeftOp = inputSources[0][1]
        self.RightOp = inputSources[1][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        # print("addLeftOP:", self.inputValues[self.LeftOp])
        sum = int(self.inputValues[self.LeftOp], 2)
        sum += (~self.inputValues[self.RightOp])
        sum = format(sum & 0xffffffff, "#034b") # Convert to 32-bit (ignore overflow)

        self.outputValues[self.outputName] = sum
