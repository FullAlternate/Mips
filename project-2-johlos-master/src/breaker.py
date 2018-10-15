from cpuElement import CPUElement


class Breaker(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 1), 'Breaker should have one input'
        assert (len(outputValueNames) == 1), 'Breaker has only one output'
        assert (len(control) == 0), 'Breaker should not have any control signal'
        assert (len(outputSignalNames) == 0), 'Breaker should not have any control output'

        self.Input = inputSources[0][1]
        self.Output = outputValueNames[0]

    def writeOutput(self):
        # print("addLeftOP:", self.inputValues[self.LeftOp])
        if self.inputValues[self.Input][-6:] == "001101":
            exit()

        else:
            self.outputValues[self.Output] = self.inputValues[self.Input]