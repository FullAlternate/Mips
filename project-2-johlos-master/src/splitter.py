import unittest
from testElement import TestElement
from cpuElement import CPUElement


class Splitter(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 1), 'Splitter has one input'
        assert (len(outputValueNames) == 6), 'Splitter has six outputs'
        assert (len(control) == 0), 'Splitter has no control signals'
        assert (len(outputSignalNames) == 0), 'Splitter does not have any control output'

        self.inputData = inputSources[0][1]
        self.outputControl = outputValueNames[0]
        self.outputR1 = outputValueNames[1]
        self.outputR2 = outputValueNames[2]
        self.outputWR = outputValueNames[3]
        self.outputSE = outputValueNames[4]
        self.outputJMP = outputValueNames[5]

    def writeOutput(self):
        instruction = self.inputValues[self.inputData]

        self.outputValues[self.outputControl] = instruction
        self.outputValues[self.outputR1] = "0b" + instruction[8:13]
        self.outputValues[self.outputR2] = "0b" + instruction[13:18]
        self.outputValues[self.outputWR] = "0b" + instruction[18:23]
        self.outputValues[self.outputSE] = "0b" + instruction[18:]
        self.outputValues[self.outputJMP] = "0b" + instruction[8:]


class TestSplit(unittest.TestCase):
    def setUp(self):
        self.splitter = Splitter()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ["instruction"],
            [],
            []
        )

        self.splitter.connect(
            [(self.testInput, "instruction")],
            ["mControl", "R1", "R2", "WR", "SE", "JMP"],
            [],
            []
        )

        self.testOutput.connect(
            [(self.splitter, "mControl"), (self.splitter, "R1"), (self.splitter, "R2"), (self.splitter, "WR"),
             (self.splitter, "SE"), (self.splitter, "JMP")],
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue("instruction", format(int(hex(0x01495020), 16), "#034b"))

        self.splitter.readInput()
        self.splitter.readControlSignals()
        self.splitter.writeOutput()
        self.testOutput.readInput()
        outputC = self.testOutput.inputValues["mControl"]
        outputR1 = self.testOutput.inputValues["R1"]
        outputR2 = self.testOutput.inputValues["R2"]
        outputWR = self.testOutput.inputValues["WR"]
        outputSE = self.testOutput.inputValues["SE"]
        outputJMP = self.testOutput.inputValues["JMP"]

        self.assertEqual(outputC, "0b00000001010010010101000000100000")
        self.assertEqual(outputR1, "0b01010")
        self.assertEqual(outputR2, "0b01001")
        self.assertEqual(outputWR, "0b01010")
        self.assertEqual(outputSE, "0b0101000000100000")
        self.assertEqual(outputJMP, "0b01010010010101000000100000")


if __name__ == '__main__':
  unittest.main()