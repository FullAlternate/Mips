from cpuElement import CPUElement


class AndGate(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 0), 'AndGate has no inputs'
        assert (len(outputValueNames) == 0), 'AndGate has no outputs'
        assert (len(control) == 2), 'AndGate has two control signals'
        assert (len(outputSignalNames) == 1), 'AndGate has one control output'

        self.signalOne = control[0][1]
        self.signalTwo = control[1][1]
        self.result = outputSignalNames[0]

    def writeOutput(self):
        pass  # randomControl has no data output

    def setControlSignals(self):
        result = self.controlSignals[self.signalOne] and self.controlSignals[self.signalTwo]

        if result == 1:
            self.outputControlSignals[self.result] = 1

        else:
            self.outputControlSignals[self.result] = 0