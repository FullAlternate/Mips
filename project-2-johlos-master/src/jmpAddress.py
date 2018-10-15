from cpuElement import CPUElement


class JMPAddress(CPUElement):
  def connect(self, inputSources, outputValueNames, control, outputSignalNames):
    CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

    assert(len(inputSources) == 2), 'Adder should have two inputs'
    assert(len(outputValueNames) == 1), 'Adder has only one output'
    assert(len(control) == 0), 'Adder should not have any control signal'
    assert(len(outputSignalNames) == 0), 'Adder should not have any control output'

    self.LeftOp = inputSources[0][1]
    self.RightOp = inputSources[1][1]
    self.outputName = outputValueNames[0]

  def writeOutput(self):

    # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))
    self.outputValues[self.outputName] = self.inputValues[self.RightOp][2:6] + bin(self.inputValues[self.LeftOp])[2:]
    # print(self.outputValues[self.outputName])

