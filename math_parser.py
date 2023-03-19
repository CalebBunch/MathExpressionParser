import math
import re
import sys


class Parser():

    def __init__(self):
        self.unwanted = [" ", ""]
        self.operators = ["+", "-", "*", "/", "^", "%", "|", "rad"]
        self.comparisons = ["==", "!=", ">", ">=", "<", "<="]

#

    def evaluate(self, expression: str) -> float:
        res = self.parse(expression)

        print(res)

#

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
                    "Use 'parser.complex_num()' for basic operations on complex numbers.")
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

#

    """
    IMPORTANT:

    I do not advise using parser.complex_num() as it is full of bugs.

    I can say with a fair amount of certainty that subtraction works as it should.

    There seems to be a problem with pythons built-in complex() function...

    When using it to convert a string in the for a+bi to a complex number,

    and then using that number in operations it yields different results than both

    evaluating the complex number in number form with pythons print statement,

    and by using a complex number calculator online.

    It is safe to say that my approach of using the complex() func. to convert

    a string to a python complex number does not work for doing subsequent operations

    with the number.

    So I repeat myself, I STRONGLY advise AGAINST using this following function,

    given the unpredictable nature of the complex() function.

    """
    # 1 + 1j + 1 + 1j = 2 + 2j

    def complex_num(self, expression: str) -> complex:

        try:
            tokens = re.split(
                "(gamma|phi|M|m|pi|e|[- + * / ^])", expression)
        except TypeError:
            print("Invalid expression. Input must be a string.")
            sys.exit(1)

        tokens = [t for t in tokens if t not in self.unwanted]

        if tokens == []:
            return

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

                tokens[token] = "3.14"

            elif tokens[token] == "e":

                tokens[token] = "2.718"

            elif tokens[token].upper() == "M":  # supports both m and M input

                tokens[token] = "0.261"

            elif tokens[token] == "phi":

                tokens[token] = "1.618"

            elif tokens[token] == "gamma":

                tokens[token] = "0.577"

        # joins complex numbers

        prev = 0

        curr = 3

        temp = []

        while curr < len(tokens):

            if tokens[curr] in ["+", "-", "*", "/", "^"]:

                temp.append("".join(tokens[prev:curr]))

                temp.append(tokens[curr])

                prev = curr + 1

                if curr + 4 == len(tokens):

                    temp.append("".join(tokens[prev:curr + 4]))

                    break

                curr += 4

        tokens = temp

        # replaces i, I, and J with j

        for i, token in enumerate(tokens):

            tokens[i] = re.sub(r"[iIJ]", "j", token, flags=re.IGNORECASE)

        # parses the complex number

        i = -1

        try:

            while len(tokens) != 1:

                i += 1

                if tokens[i] == "+":

                    if "*" in tokens or "/" in tokens or "^" in tokens:
                        pass

                    else:

                        num1 = complex(tokens[i - 1])

                        num2 = complex(tokens[i + 1])

                        res = num1 + num2

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                if tokens[i] == "-":

                    if "*" in tokens or "/" in tokens or "^" in tokens:
                        pass

                    else:

                        num1 = complex(tokens[i - 1])

                        num2 = (tokens[i + 1])

                        # get complex conjugate of num2 because just calling the complex function on it is resulting in the wrong answer

                        num2 = re.split("([- +])", num2)

                        num2 = [i for i in num2 if i not in self.unwanted]

                        if len(num2) % 2 == 1:

                            mid = len(num2)//2

                            if num2[mid] == "+":

                                num2[mid] = "-"

                            elif num2[mid] == "-":

                                num2[mid] = "+"

                        else:

                            if num2[0] == "+" or num2[0] == "-":

                                mid = len(num2) // 2

                            else:

                                mid = len(num2) // 2 - 1

                            if num2[mid] == "+":

                                num2[mid] = "-"

                            elif num2[mid] == "-":

                                num2[mid] = "+"

                        prev = -1

                        curr = 0

                        while curr < len(num2):

                            prev += 1

                            curr += 1

                            if num2[prev] == "-" and num2[curr] == "-":

                                num2[prev:curr + 1] = "+"

                        num2 = complex("".join(num2))

                        res = num1 - num2

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                if tokens[i] == "*":

                    if "^" in tokens:
                        pass

                    else:

                        num1 = complex(tokens[i - 1])

                        num2 = complex(tokens[i + 1])

                        res = num1 * num2

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                if tokens[i] == "/":

                    if "^" in tokens:
                        pass

                    else:

                        num1 = complex(tokens[i - 1])

                        num2 = complex(tokens[i + 1])

                        res = num1 / num2

                        tokens[i - 1:i + 2] = [res]

                        i = -1

                if tokens[i] == "^":

                    num1 = complex(tokens[i - 1])

                    num2 = complex(tokens[i + 1])

                    res = num1 ** num2

                    tokens[i - 1:i + 2] = [res]

                    i = -1

        except (IndexError, ValueError):
            print("Could not parse expression.")
            sys.exit(1)

        result = tokens[0]

        return result


#


    def test(self, expression: str, variables: dict) -> float:

        split_expression = re.split("([- + * / ^ % /( /)])", expression)

        if len(split_expression) < 0 or split_expression[0] == "" or split_expression[0] == " ":
            print("Must have a valid expression.")
            return

        if len(variables) < 1:
            print(
                "Variable, Value pairs should be in a dictionary in the format {'var': value, 'var2': value2, etc.} where var is a string and value is an integer or float.")
            return

        for k in variables.keys():
            if str(k) not in split_expression:
                print(
                    f"variable {str(k)} must occur in expression {expression}.")
                return

        try:
            for i in range(len(split_expression)):
                if split_expression[i] in variables:
                    val = variables[split_expression[i]]
                    split_expression[i] = str(val)

        except (IndexError, ValueError, KeyError):
            print(
                "An error occured. Variable, Value pairs should be in a dictionary like this: {'var1': val1, 'var2': val2}")
            return

        expression = "".join(split_expression)

        return self.evaluate(expression)

#

    def compare(self, expression: str) -> bool:

        try:
            tokens = re.split("(<=|>=|!=|==|[^a-zA-Z0-9])", expression)
        except TypeError:
            print("Invalid expression. Input must be a string.")
            sys.exit(1)

        tokens = [t for t in tokens if t not in self.unwanted]

        # checking for potential negative numbers and combining the number with its sign

        if tokens[0] == "-":
            del tokens[0]
            tokens[0] = "-" + tokens[0]

        if tokens[0] == "+":
            del tokens[0]

        prev = -1
        curr = 0

        while curr < len(tokens) - 1:
            curr += 1
            prev += 1
            # check if comparison and operators are next to each other if they are then combine the operator with the number which follows it
            # 2 > - 2
            if tokens[curr] in self.operators and tokens[prev] in self.comparisons:
                tokens[curr + 1] = tokens[curr] + tokens[curr + 1]
                del tokens[curr]

        if len(tokens) != 3:
            print("Expression must be in the form 'x>y' where x and y are real numbers and > is the desired comparison operator.")
            return

        i = -1

        try:

            while len(tokens) != 1:
                i += 1

                if tokens[i] == "==":
                    num1 = float(tokens[i - 1])

                    num2 = float(tokens[i + 1])

                    res = self.isequal(num1, num2)

                    return res

                elif tokens[i] == "!=":
                    num1 = float(tokens[i - 1])

                    num2 = float(tokens[i + i])

                    res = self.isnotequal(num1, num2)

                    return res

                elif tokens[i] == ">":
                    num1 = float(tokens[i - 1])

                    num2 = float(tokens[i + 1])

                    res = self.isgreater(num1, num2)

                    return res

                elif tokens[i] == "<":
                    num1 = float(tokens[i - 1])

                    num2 = float(tokens[i + 1])

                    res = self.isless(num1, num2)

                    return res

                elif tokens[i] == ">=":
                    num1 = float(tokens[i - 1])

                    num2 = float(tokens[i + 1])

                    res = self.isgreaterorequal(num1, num2)

                    return res

                elif tokens[i] == "<=":
                    num1 = float(tokens[i - 1])

                    num2 = float(tokens[i + 1])

                    res = self.islessorequal(num1, num2)

                    return res

        except (IndexError, ValueError):
            print("Could not parse expression.")
            sys.exit(1)

#

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

    def cos(self, num1: int):
        return math.cos(num1)

    def sin(self, num1: int):
        return math.sin(num1)

    def tan(self, num1: int):
        return math.tan(num1)

    def acos(self, num1: int):
        return math.acos(num1)

    def asin(self, num1: int):
        return math.asin(num1)

    def atan(self, num1: int):
        return math.asin(num1)

    def degrees(self, num1: int):
        return math.degrees(num1)

    def radians(self, num1: int):
        return math.radians(num1)

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

    # comparison operators

    def isequal(self, num1: int, num2: int):
        return num1 == num2

    def isnotequal(self, num1: int, num2: int):
        return num1 != num2

    def isgreater(self, num1: int, num2: int):
        return num1 > num2

    def isless(self, num1: int, num2: int):
        return num1 < num2

    def isgreaterorequal(self, num1: int, num2: int):
        return num1 >= num2

    def islessorequal(self, num1: int, num2: int):
        return num1 <= num2
