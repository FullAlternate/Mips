import unittest
from testElement import TestElement
from cpuElement import CPUElement

class ALU(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 2), 'ALU should have two inputs'
        assert (len(outputValueNames) == 1), 'ALU has one output'
        assert (len(control) == 2), 'ALU has two control signals'
        assert (len(outputSignalNames) == 1), 'ALU does has one control output'

        self.LeftOp = inputSources[0][1]
        self.RightOp = inputSources[1][1]
        self.outputResult = outputValueNames[0]
        self.ALUOp = control[0][1]
        self.ALUOpT = control[1][1]
        self.outputZero = outputSignalNames[0]

    def writeOutput(self):
        OPCode = self.controlSignals[self.ALUOp]
        OPType = self.controlSignals[self.ALUOpT]

        if isinstance(self.inputValues[self.LeftOp], int) is False:
            self.inputValues[self.LeftOp] = int(self.inputValues[self.LeftOp], 2)

        if isinstance(self.inputValues[self.RightOp], int) is False:
            self.inputValues[self.RightOp] = int(self.inputValues[self.RightOp], 2)

        #  Changes int to signed 2's compliment
        #def two_compliment(x):
           # if (x & (1 << 32 - 1)) != 0:
            #    x = x - (1 << 32)
           # return x

       # self.inputValues[self.LeftOp] = two_compliment(self.inputValues[self.LeftOp])
       # self.inputValues[self.RightOp] = two_compliment(self.inputValues[self.RightOp])

        print("ALU - OPCode: ", OPCode)
        print("ALU - OPType: ", OPType)
        print("ALU - Read Data1: ", bin(self.inputValues[self.LeftOp]))
        print("ALU - AluMuxOut: ", bin(self.inputValues[self.RightOp]))

        # print("ALU - OutputZero: ", self.outputValues[self.outputZero])

        # ADD (10 0000)
        if OPCode == "100000" and OPType == 0:
            sum = self.inputValues[self.LeftOp]
            # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))
            sum += self.inputValues[self.RightOp]

            self.outputValues[self.outputResult] = format(sum, "#034b")

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # ADDU (10 0001)
        elif OPCode == "100001" and OPType == 0:
            sum = self.inputValues[self.LeftOp]
            # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))
            sum += self.inputValues[self.RightOp]

            self.outputValues[self.outputResult] = format(sum & 0xffffffff, "#034b")  # Convert to 32-bit (ignore overflow)

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # SUB (10 0010)
        elif OPCode == "100010" and OPType == 0:
            sum = self.inputValues[self.LeftOp]
            # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))
            sum -= self.inputValues[self.RightOp]

            self.outputValues[self.outputResult] = format(sum, "#034b")

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # SUBU (10 0011)
        elif OPCode == "100011" and OPType == 0:
            sum = self.inputValues[self.LeftOp]
            # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))
            sum -= self.inputValues[self.RightOp]

            self.outputValues[self.outputResult] = format(sum & 0xffffffff, "#034b")  # Convert to 32-bit (ignore overflow)

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # AND (10 0100)
        elif OPCode == "100100" and OPType == 0:
            sum = self.inputValues[self.LeftOp] & self.inputValues[self.RightOp]

            self.outputValues[self.outputResult] = format(sum, "#034b")

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # OR (10 0101)
        elif OPCode == "100101" and OPType == 0:
            sum = self.inputValues[self.LeftOp] | self.inputValues[self.RightOp]

            self.outputValues[self.outputResult] = format(sum, "#034b")

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # NOR (10 0111)
        elif OPCode == "100111" and OPType == 0:
            sum = ~(self.inputValues[self.LeftOp] | self.inputValues[self.RightOp])

            self.outputValues[self.outputResult] = format(sum, "#034b")

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # SLT (10 1010)
        elif OPCode == "101010" and OPType == 0:
            bool = self.inputValues[self.LeftOp] < self.inputValues[self.RightOp]

            if bool is True:
                self.outputValues[self.outputResult] = bin(1)

            else:
                self.outputValues[self.outputResult] = bin(0)

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # BREAK (00 1101)
        # elif OPCode == bin(1101):

        # ADDI (00 1000) or LW (10 0011) or SW (10 1011)
        elif OPCode == "001000" or OPCode == "100011" or OPCode == "101011" and OPType == 1:
            # print("LOADWORD")
            sum = self.inputValues[self.LeftOp]
            # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))
            sum += self.inputValues[self.RightOp]

            self.outputValues[self.outputResult] = format(sum, "#034b")

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # ADDIU (00 1001)
        elif OPCode == "001001" and OPType == 1:
            sum = self.inputValues[self.LeftOp]
            # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))
            sum += self.inputValues[self.RightOp]

            self.outputValues[self.outputResult] = format(sum & 0xffffffff, "#034b")  # Convert to 32-bit (ignore overflow)

            if self.outputValues[self.outputResult] == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0


        # BEQ (00 0100)
        elif OPCode == "000100" and OPType == 1:
            sum = self.inputValues[self.LeftOp]

            # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))

            sum -= self.inputValues[self.RightOp]

            if sum == 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # BNE (00 0101)
        elif OPCode == "000101" and OPType == 1:
            sum = self.inputValues[self.LeftOp]

            # assert (isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))

            sum -= self.inputValues[self.RightOp]

            if sum != 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        # LUI (00 1111)
        elif OPCode == "001111" and OPType == 1:
            sum = self.inputValues[self.RightOp] << 16

            self.outputValues[self.outputResult] = format(sum, "#034b")

            if sum != 0:
                self.outputControlSignals[self.outputZero] = 1
            else:
                self.outputControlSignals[self.outputZero] = 0

        print("ALU - Output: ", self.outputValues[self.outputResult])

class TestALU(unittest.TestCase):
    def setUp(self):
        self.alu = ALU()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ["dataA", "dataB"],
            [],
            ["aluCodeControl", "aluTypeControl"]
        )

        self.alu.connect(
            [(self.testInput, "dataA"), (self.testInput, "dataB")],
            ["aluData"],
            [(self.testInput, "aluCodeControl"), (self.testInput, "aluTypeControl")],
            ["aluZero"]
        )

        self.testOutput.connect(
            [(self.alu, "aluData")],
            [],
            [(self.alu, "aluZero")],
            []
        )

    def test_correct_behavior(self):

        self.testInput.setOutputValue("dataA", bin(20))
        self.testInput.setOutputValue("dataB", bin(10))

        self.testInput.setOutputControl("aluTypeControl", 0)

        # ADD
        self.testInput.setOutputControl("aluCodeControl", bin(100000))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(30))

        # ADDU
        self.testInput.setOutputControl("aluCodeControl", bin(100001))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(30))

        # SUB
        self.testInput.setOutputControl("aluCodeControl", bin(100010))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(10))

        # SUBU
        self.testInput.setOutputControl("aluCodeControl", bin(100011))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(10))

        # AND
        self.testInput.setOutputControl("aluCodeControl", bin(100100))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(0))

        # OR
        self.testInput.setOutputControl("aluCodeControl", bin(100101))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(30))

        # NOR
        self.testInput.setOutputControl("aluCodeControl", bin(100111))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(-31))

        # SLT
        self.testInput.setOutputControl("aluCodeControl", bin(101010))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(0))

        self.testInput.setOutputControl("aluTypeControl", 1)
        # ADDI
        self.testInput.setOutputControl("aluCodeControl", bin(1000))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(30))

        # ADDIU
        self.testInput.setOutputControl("aluCodeControl", bin(1001))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(30))

        # LW
        self.testInput.setOutputControl("aluCodeControl", bin(100011))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(30))

        # SW
        self.testInput.setOutputControl("aluCodeControl", bin(101011))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(30))

        # LUI
        self.testInput.setOutputControl("aluCodeControl", bin(1111))

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues["aluData"]

        self.assertEqual(output, bin(655360))

        self.testInput.setOutputValue("dataA", bin(15))
        self.testInput.setOutputValue("dataB", bin(15))


if __name__ == '__main__':
  unittest.main()
