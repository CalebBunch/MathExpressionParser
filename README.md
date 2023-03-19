# MathExpressionParser

This program is designed to parse a math expression represented as a string.

The program should be used like this:

```python
from math_parser import Parser

parser = Parser()

print(parser.parse("2*4")
```
The parser can understand most basic math operations as well as some mathematical constants.
It can also work with both positive and negative numbers, as well as understand operator precedence.
The parser ignores whitespaces so they are optional in the string expression, passed as an argument to the parser function.

Here are examples of different expressions it could parse.

```python
from math_parser import Parser

parser = Parser()

# Addition
print(parser.parse("2.5 + 4.0"))

# Subtraction

print(parser.parse("-5 - 10"))

# Multiplication

print(parser.parse("4 * -3"))

# Division

print(parser.parse("85 / 3"))

# Parenthesis 

print(parser.parse("(1 + 1) * 5"))

# Exponentiation

print(parser.parse("2 ^ 3"))

# Modulo Operator (Remainder of Division)

print(parser.parse("57 % 2"))

# Factorial

print(parser.parse("4! + 3"))

# Absolute Value

print(parser.parse("|-3|"))

# Natural Logarithm

print(parser.parse("ln(2.7182818)")) # very close to 1

# Logarithm

print(parser.parse("log2(32)*(5+2)"))

# Square Roots

print(parser.parse("sqrt(4)"))

# Cube Roots

print(parser.parse("cbrt(27)"))

# Radicals

print(parser.parse("rad4(16)")) # 4th root of 16

# Mathematical Constants

print(parser.parse("pi * 2 * 5"))

print(parser.parse("e"))

print(parser.parse("M"))

print(parser.parse("phi"))

print(parser.parse("gamma"))

```



