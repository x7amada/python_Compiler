"""
Mahmoud Abo Hamd - 325092708
Ghada Abu Sbetan - 212632129
Muhamed Dahly - 212806996
Osama Shtewe - 211404207
"""

class my_Math:
    def add(a, b):
        try:
            return a+b
        except ValueError:
            raise ValueError(f"{a}+{b}")

    def subtract(a, b):
        return a - b


    def multiply(a, b):
       return a*b

    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


    def power(a, b):
        result=1
        for i in range(b):
            result*=a
        return result

    def sqrt(value, epsilon=1e-10):
        if value < 0:
            raise ValueError("Cannot compute the square root of a negative number")
        guess = value
        while abs(guess * guess - value) > epsilon:
            guess = (guess + value / guess) / 2
        return guess
    def equal(a,b):
        return a==b
    def not_equal(a,b):
        return not a!=b
    def greater(a,b):
        return a>b
    def smaller(a,b):
        return a<b
    def o_r(a,b):
        return a or b
    def A_nd(a,b):
        return a and b

    def greater_equal(a, b):
        return my_Math.greater(a, b) or my_Math.equal(a, b)

    def smaller_equal(a, b):
        return my_Math.smaller(a, b) or my_Math.equal(a, b)
    def isnumbertic(str):
        for c in str:
            if not((c<='9' and c>='0') or c=='.'):
                return False
        return True
