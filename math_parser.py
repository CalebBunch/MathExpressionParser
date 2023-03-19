import math
import re
import sys


class Parser():

    def __init__(self):
        self.unwanted = [" ", ""]
        self.operators = ["+", "-", "*", "/", "^", "%", "|", "rad"]
        self.comparisons = ["==", "!=", ">", ">=", "<", "<="]

    def parse(self, expression: str) -> float:

        try:
            tokens = re.split(
                "(J|I|j|i|gamma|phi|M|m|pi|e|rad|cbrt|log|ln|sqrt|[- + * / ^ % ! /| /( /)])", expression)
        except TypeError:
            print("Invalid expression. Input must be a string.")
            sys.exit(1)

        tokens = [t for t in tokens if t not in self.unwanted]

        if tokens == []:
            return

        # handle complex numbers

        for token in range(len(tokens)):

            if tokens[token].lower() == "i" or tokens[token].lower() == "j":
                print(
                    "Cannot do operations on complex numbers.")
                sys.exit(0)

        # checking for potential negative numbers and combining the number with its sign

        if tokens[0] == "-":
            del tokens[0]
            tokens[0] = "-" + tokens[0]

        if tokens[0] == "+":
            del tokens[0]

        prev = -1
        curr = 0

        # 2 - - 2
        while curr < len(tokens) - 1:
            curr += 1
            prev += 1
            # check if 2 operators are next to each other if they are then combine the second of the two with the number which follows it
            if tokens[curr] in self.operators and tokens[prev] in self.operators:
                tokens[curr + 1] = tokens[curr] + tokens[curr + 1]
                del tokens[curr]

        # handles mathmatical constants by replacing their letter representations with their corresponding numbers to the 10 decimal

        for token in range(len(tokens)):

            if tokens[token] == "pi":

                tokens[token] = "3.1415926536"

            elif tokens[token] == "e":

                tokens[token] = "2.7182818285"

            elif tokens[token].upper() == "M":  # supports both m and M input

                tokens[token] = "0.2614972128"

            elif tokens[token] == "phi":

                tokens[token] = "1.6180339887"

            elif tokens[token] == "gamma":

                tokens[token] = "0.5772156649"

        i = -1

        try:

            while len(tokens) != 1:
                i += 1

                if tokens[i] == "+":

                    if "rad" in tokens or "|" in tokens or "ln" in tokens or "log" in tokens or "sqrt" in tokens or "cbrt" in tokens or "/" in tokens or "*" in tokens or "^" in tokens or "%" in tokens or "(" in tokens:
                        pass

                    else:

                        # get num before operator
                        num1 = float(tokens[i - 1])

                        # get num after operator
                        num2 = float(tokens[i + 1])

                        # call function on the nums and get the result
                        res = self.add(num1, num2)

                        # set x + y = result in the list so replace 3 items with one
                        tokens[i - 1:i + 2] = [res]

                        # RESTART LOOP
                        i = -1

                elif tokens[i] == "-":

                    if "rad" in tokens or "|" in tokens or "ln" in tokens or "log" in tokens or "sqrt" in tokens or "cbrt" in tokens or "/" in tokens or "*" in tokens or "^" in tokens or "%" in tokens or "(" in tokens:
                        pass

                    else:
                        num1 = float(tokens[i - 1])

                        num2 = float(tokens[i + 1])

                        res = self.sub(num1, num2)

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                elif tokens[i] == "*":

                    if "rad" in tokens or "|" in tokens or "ln" in tokens or "log" in tokens or "sqrt" in tokens or "cbrt" in tokens or "^" in tokens or "%" in tokens or "(" in tokens:
                        pass

                    else:
                        num1 = float(tokens[i - 1])

                        num2 = float(tokens[i + 1])

                        res = self.multiply(num1, num2)

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                elif tokens[i] == "/":

                    if "rad" in tokens or "|" in tokens or "ln" in tokens or "log" in tokens or "sqrt" in tokens or "cbrt" in tokens or "^" in tokens or "%" in tokens or "(" in tokens:
                        pass

                    else:
                        num1 = float(tokens[i - 1])

                        num2 = float(tokens[i + 1])

                        res = self.divide(num1, num2)

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                elif tokens[i] == "^":

                    if "rad" in tokens or "|" in tokens or "ln" in tokens or "log" in tokens or "sqrt" in tokens or "cbrt" in tokens in tokens:
                        pass

                    else:
                        num1 = float(tokens[i - 1])

                        num2 = float(tokens[i + 1])

                        res = self.raise_power(num1, num2)

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                elif tokens[i] == "%":

                    if "rad" in tokens or "|" in tokens or "ln" in tokens or "log" in tokens or "sqrt" in tokens or "cbrt" in tokens in tokens:
                        pass

                    else:
                        num1 = float(tokens[i - 1])

                        num2 = float(tokens[i + 1])

                        res = self.mod(num1, num2)

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                elif tokens[i] == "!":

                    if "rad" in tokens or "(" in tokens or "sqrt" in tokens or "cbrt" in tokens or "ln" in tokens or "log" in tokens:
                        pass

                    else:

                        num = int(tokens[i - 1])

                        res = self.factorial(num)

                        tokens[i - 1:i + 1] = [res]

                        i = -1

                elif tokens[i] == "|":

                    if "rad" in tokens or "(" in tokens or "sqrt" in tokens or "cbrt" in tokens or "ln" in tokens or "log" in tokens:
                        pass

                    else:

                        if tokens[i + 2] == "|":

                            num = float(tokens[i + 1])

                            res = self.abs(num)

                            tokens[i:i + 3] = [res]

                            i = -1

                        elif tokens[i + 4] == "|":

                            block = "".join(tokens[i + 1:i + 4])

                            block = self.parse(block)

                            res = self.abs(block)

                            tokens[i + 1:i + 4] = [res]

                            i = -1

                        else:
                            print("Must have matching | | chars.")
                            break

                elif tokens[i] == "ln":

                    if tokens[i + 1] == "(":

                        if tokens[i + 3] != ")":
                            print("Must have matching parenthesis.")
                            break

                        else:

                            num = float(tokens[i + 2])

                            res = self.ln(num)

                            tokens[i:i + 4] = [res]

                            i = -1
                    else:

                        num = float(tokens[i + 1])

                        res = self.ln(num)

                        tokens[i:i + 2] = [res]

                        i = -1

                elif tokens[i] == "log":

                    try:

                        if tokens[i + 2] == "(":

                            if tokens[i + 4] != ")":
                                print("Must have matching parenthesis.")
                                break

                            else:

                                base = float(tokens[i + 1])

                                num = float(tokens[i + 3])

                                res = self.log(num, base)

                                tokens[i:i + 5] = [res]

                                i = -1

                        elif tokens[i + 1] == "(":

                            if tokens[i + 3] != ")":
                                print("Must have matching parenthesis.")
                                break

                            else:

                                num = float(tokens[i + 2])

                                res = self.log10(num)

                                tokens[i:i + 4] = [res]

                                i = -1

                    except IndexError:

                        num = float(tokens[i + 1])

                        res = self.log10(num)

                        tokens[i:i + 2] = [res]

                        i = -1

                elif tokens[i] == "sqrt":

                    if tokens[i + 1] == "(" and tokens[i + 3] in self.operators:
                        pass

                    else:

                        if tokens[i + 1] == "(":

                            if tokens[i + 3] != ")":
                                print("Must have matching parenthesis.")
                                break

                            else:
                                num = float(tokens[i + 2])

                                res = self.sqrt(num)

                                tokens[i:i + 4] = [res]

                                i = -1

                        elif tokens[i - 1] == "(":

                            if tokens[i + 2] != ")":
                                print("Must have matching parenthesis.")
                                break

                            else:
                                num = float(tokens[i + 1])

                                res = self.sqrt(num)

                                tokens[i - 1:i + 3] = [res]

                                i = -1

                        else:

                            num = float(tokens[i + 1])

                            res = self.sqrt(num)

                            tokens[i:i + 2] = [res]

                            i = -1

                elif tokens[i] == "cbrt":
                    
                    if tokens[i + 1] == "(" and tokens[i + 3] in self.operators:
                        pass

                    else:

                        if tokens[i + 1] == "(":

                            if tokens[i + 3] != ")":
                                print("Must have matching parenthesis.")
                                break

                            else:
                                num = float(tokens[i + 2])

                                res = self.cbrt(num)

                                tokens[i:i + 4] = [res]

                                i = -1

                        elif tokens[i - 1] == "(":

                            if tokens[i + 2] != ")":
                                print("Must have matching parenthesis.")
                                break

                            else:
                                num = float(tokens[i + 1])

                                res = self.cbrt(num)

                                tokens[i - 1:i + 3] = [res]

                                i = -1

                        else:

                            num = float(tokens[i + 1])

                            res = self.cbrt(num)

                            tokens[i:i + 2] = [res]

                            i = -1

                # rad idx (randicand)

                # rad5(32) 5th root of 32 should return 2
                elif tokens[i] == "rad":

                    if tokens[i + 3].isdigit() and tokens[i + 4] in self.operators:
                        pass

                    else:

                        if tokens[i + 3] == "-":

                            if tokens[i + 2] == "(":

                                if tokens[i + 5] != ")":
                                    print("Must have matching parenthesis.")
                                    break

                                else:

                                    tokens[i + 3:i +
                                           5] = [str(float(tokens[i + 4]) * -1)]

                                    index = float(tokens[i + 1])

                                    randicand = float(tokens[i + 3])

                                    res = self.radical(index, randicand)

                                    tokens[i:i + 5] = [res]

                                    i = -1

                        elif tokens[i + 2] == "(":

                            if tokens[i + 4] != ")":
                                print("Must have matching parenthesis.")
                                break

                            else:

                                index = float(tokens[i + 1])

                                randicand = float(tokens[i + 3])

                                res = self.radical(index, randicand)

                                tokens[i:i + 5] = [res]

                                i = -1

                elif tokens[i] == "(":

                    if tokens[i + 1] == "sqrt" or tokens[i + 1] == "cbrt":
                        pass

                    else:

                        if tokens[i + 4] != ")":
                            print("Must have matching parenthesis.")
                            break

                        else:
                            # grab the operation to be passed back into the function
                            block = "".join(tokens[i + 1:i + 4])

                            # get result from parsing the block in parenthesis
                            res = self.parse(block)

                            # set entire block including parenthesis in orginal expression to the result
                            tokens[i:i + 5] = [res]

                            i = -1

        except (IndexError, ValueError):
            print("Could not parse expression.")
            sys.exit(1)

        result = tokens[0]

        return result


    def add(self, num1: int, num2: int):
        return num1 + num2

    def sub(self, num1: int, num2: int):
        return num1 - num2

    def multiply(self, num1: int, num2: int):
        return num1 * num2

    def divide(self, num1: int, num2: int):
        return num1 / num2

    def raise_power(self, num1: int, num2: int):
        return num1 ** num2

    def mod(self, num1: int, num2: int):
        return num1 % num2

    # advanced operations

    def sqrt(self, num1: int):
        return math.sqrt(num1)

    def cbrt(self, num1: int):
        return num1**(1/3)

    def radical(self, index: int, randicand: int):

        if randicand < 0 and index > 0:
            return -1 * ((-1 * randicand)**(1/index))

        elif randicand > 0 and index < 0:
            return 1 / (randicand**(1 / (-1 * index)))

        elif randicand < 0 and index < 0:
            return 1 / (-1 * (((-1 * randicand)**(1 / (-1 * index)))))

        else:
            return randicand**(1/index)

    def abs(self, num1: int):
        return math.fabs(num1)

    def ln(self, num1: int):
        return math.log(num1)

    def log2(self, num1: int):
        return math.log2(num1)

    def log(self, num: int, base: int):
        return math.log(num, base)

    def log10(self, num1: int):
        return math.log10(num1)

    def factorial(self, num1: int):
        return math.factorial(num1)
