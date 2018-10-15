import unittest
from testElement import TestElement
from cpuElement import CPUElement


class SignExtender(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 1), 'SignExtender has one input'
        assert (len(outputValueNames) == 1), 'SignExtender has one output'
        assert (len(control) == 0), 'SignExtender has no control signals'
        assert (len(outputSignalNames) == 0), 'SignExtender does not have any control output'

        self.inputData = inputSources[0][1]
        self.outputResult = outputValueNames[0]

    def writeOutput(self):
        original_adress = self.inputValues[self.inputData]
        if original_adress[2] == "1":
            extend = "1111111111111111"
            sum = "0b" + extend + format(int(original_adress, 2), "016b")
        else:
            sum = format(int(original_adress, 2), "#034b")

        self.outputValues[self.outputResult] = sum
        x = 1

        print("SignExtend - Output: ", self.outputValues[self.outputResult])

class TestSignExtend(unittest.TestCase):
    def setUp(self):
        self.signEx = SignExtender()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ["dataA"],
            [],
            []
        )

        self.signEx.connect(
            [(self.testInput, "dataA")],
            ["signExData"],
            [],
            []
        )

        self.testOutput.connect(
            [(self.signEx, "signExData")],
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue("dataA", bin(32768))

        self.signEx.readInput()
        self.signEx.readControlSignals()
        self.signEx.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["signExData"]

        self.assertEqual(output, format(int(bin(32768), 2), "#034b"))


if __name__ == '__main__':
  unittest.main()