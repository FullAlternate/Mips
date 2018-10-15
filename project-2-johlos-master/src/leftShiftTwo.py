import unittest
from testElement import TestElement
from cpuElement import CPUElement

class LeftShiftTwo(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 1), 'LeftShiftTwo has one input'
        assert (len(outputValueNames) == 1), 'LeftShiftTwo has one output'
        assert (len(control) == 0), 'leftShiftTwo has no control signals'
        assert (len(outputSignalNames) == 0), 'LeftShiftTwo does not have any control output'

        self.inputData = inputSources[0][1]
        self.outputResult = outputValueNames[0]

    def writeOutput(self):
        sum = int(self.inputValues[self.inputData], 2) << 2
        self.outputValues[self.outputResult] = sum
        x = 2

class TestLeftShiftTwo(unittest.TestCase):
    def setUp(self):
        self.leftTwo = LeftShiftTwo()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ["dataA"],
            [],
            []
        )

        self.leftTwo.connect(
            [(self.testInput, "dataA")],
            ["leftTwoData"],
            [],
            []
        )

        self.testOutput.connect(
            [(self.leftTwo, "leftTwoData")],
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue("dataA", bin(5))

        self.leftTwo.readInput()
        self.leftTwo.readControlSignals()
        self.leftTwo.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["leftTwoData"]

        self.assertEqual(output, 20)


if __name__ == '__main__':
  unittest.main()