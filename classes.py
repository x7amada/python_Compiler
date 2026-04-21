"""
Mahmoud Abo Hamd - 325092708
Ghada Abu Sbetan - 212632129
Muhamed Dahly - 212806996
Osama Shtewe - 211404207
"""
from Math import my_Math


class Array:

    def __init__(self, ele):
        self.array = ele
        self.count = 0

        for v in self.array:
            if v is not None:
                self.count += 1
            else:
                break

    def get_bigger(self):
        new_array = [None] * (len(self.array) * 2)
        # Copy old elements
        for i in range(len(self.array)):
            new_array[i] = self.array[i]
        self.array = new_array

    def __str__(self):
        return f"{self.array}"

    def length(self):
        return self.count

    def add(self, i, value):
        self.array[i] = value
        if i == self.count:
            self.count += 1

    def append(self, value):
        try:
            self.array[self.count] = value

            self.count += 1
        except IndexError:
            self.get_bigger()
            self.array[self.count] = value
            self.count += 1

    def index(self, value):
        try:
            for i in range(self.count):
                if self.array[i] ==value:
                    return i
        except:
            raise IOError("the value does not exest")

    def get_value(self, i):
        try:
            return self.array[i]
        except:
            raise IndexError("he index out of range")

    def remove(self, value):
        # Custom remove without using list's remove
        if value not in self.array:
            print(f"value {value} not found in the array")
            return
        index = self.index(value)  # This could raise an exception or return None
        self.add(index, None)
        for i in range(index,self.count-1):
            self.array[i] = self.array[i+1]
        self.array[self.count-1] = None
        self.count-=1
class MyTuple:
    def __init__(self, *args):
        self._elements = []
        self.size = 0
        for a in args:
            self._elements.append(a)
            self.size+=1

    def __len__(self):
        # Return the length of the tuple
        return self.size

    def __getitem__(self, index):
        # Return the element at the specified index
        if not isinstance(index, int):
            raise TypeError("Tuple indices must be integers.")
        if index < 0 or index >= len(self._elements):
            raise IndexError("Tuple index out of range.")
        return self._elements[index]

    def getitem(self, index):
        # Return the element at the specified index
        if not isinstance(index, int):
            raise TypeError("Tuple indices must be integers.")
        if index < 0 or index >= len(self._elements):
            raise IndexError("Tuple index out of range.")
        return self._elements[index]

    def __contains__(self, item):
        # Check if the tuple contains the specified item
        return item in self._elements

    def contains(self, item):
        # Check if the tuple contains the specified item
        return item in self._elements

    def __add__(self, other):
        # Concatenate two MyTuple instances to return a new MyTuple
        if not isinstance(other, MyTuple):
            raise TypeError("Can only concatenate with another MyTuple.")
        return MyTuple(*(self._elements + other._elements))

    def __iter__(self):
        # Allow iteration over the tuple elements
        return iter(self._elements)

    def __repr__(self):
        # String representation of the tuple
        return f"MyTuple({', '.join(repr(e) for e in self._elements)})"

    def add(self, other):
        # Concatenate two MyTuple instances to return a new MyTuple
        if not isinstance(other, MyTuple):
            raise TypeError("Can only concatenate with another MyTuple.")
        return MyTuple(*(self._elements + other._elements))

    def count(self, value):
        # Count occurrences of the specified value
        return self._elements.count(value)

    def index(self, value):
        # Get the index of the first occurrence of the specified value
        if value in self._elements:
            return self._elements.index(value)
        else:
            raise ValueError(f"{value} is not in tuple")

    def sort(self):
        # Return a sorted version of the tuple (without modifying the original)
        sorted_ = self._elements
        return sorted_.sort()

    def length(self):
        # Return the length of the tuple
        return self.size


def convert_to_int(s):
    if my_Math.isnumbertic(s):
        if '.' in s:
            raise ValueError("cant convert float to int")
        else:
            num = 0
            for c in s:
                num *= 10
                num = num+(ord(c)-ord('0'))
            return num

    else:
        raise ValueError("the value is not number")


def convert_to_float(s):
    if my_Math.isnumbertic(s):
        lift = 0
        right = 0
        if '.' in s:
            lift, right = s.split('.')
            lift = convert_to_int(lift)
            right = convert_to_int(right)/(10**len(right))
            return lift+right
        else:
            lift = convert_to_int(s)
            return lift+0.0


def convert_to_boolean(s):

    if s in {"True", "1"}:
        return True
    elif s in {"False","0"}:
        return False
    else:
        raise ValueError("cant convert to boolean")


def split(c=' ', stri=None):
    parts = []
    part = ''

    for ch in stri.strip():
        if ch == c:
            parts.append(part)
            part = ''
        else:
            part += ch
    parts.append(part)
    return parts


def replace(unwonted, new, str):
    for i in range(len(str)):
        if str[i] == unwonted[0]:
            found = True
            for j in range(i, len(unwonted)):
                print(j)
                if str[j] != unwonted[j-i]:
                    print(j)
                    found == False
                    j = len(str)
            if found:
                bef = str[:i]
                after = str[len(unwonted)+i:]
                updated = bef+new+after
                return updated
        else:
            raise ValueError(f"there is no {unwonted} in {str}")


def isupper(str):
    ls = "[@_!#$%^&*()<>?}{~:] "
    for c in str:
        if not(c>'A' and c<'Z') and not(c>'0' and c<'9') and c not in ls:
            return False
    return True


def islower(str):
    ls = "[@_!#$%^&*()<>?}{~:] "
    for c in str:
        if not (c >'a' and c <'z') and not (c > '0' and c < '9') and c not in ls:
            return False
    return True


def concat(str2, str1):
    return str1+str2

