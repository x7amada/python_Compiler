"""
Mahmoud Abo Hamd - 325092708
Ghada Abu Sbetan - 212632129
Muhamed Dahly - 212806996
Osama Shtewe - 211404207
"""

from Math import my_Math
import classes
from classes import Array, MyTuple
from secound import Lexer, Parser, SemanticAnalyzer


class miniLang:
    def __init__(self):
        self.variables = {}
        self.commands = []
        self.current_command_index = 0
        self.functions = {}

    def analize(self,code):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(tokens)

        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer(ast)
        errors = analyzer.analyze()
        print(ast)
        if errors:
            for error in errors:
                print(f"Semantic Error: {error}")
        else:
            print("No semantic errors found.")
        self.commands = ast

    def file_to_code(self,path):
        with open(path, 'r') as file:
            code = file.read().rstrip()
            self.analize(code)

    def read_code(self):
        while self.current_command_index < len(self.commands):
            command = self.commands[self.current_command_index]
            self.execute_command(command)
            self.current_command_index += 1

    def execute_command(self, command):
        if command[0] == 'assign':
            self.execute_assign(command)
        elif command[0] == 'reassign':
            self.execute_reassign(command)
        elif command[0] == 'if':
            self.execute_if()
        elif command[0] == 'for':
            self.execute_for()
        elif command[0] == 'while':
            self.execute_while()
        elif command[0] == 'print':
            self.execute_print()
        elif command[0] == 'call_functionClass':
            self.execute_func()

    def execute_assign(self, command):
        var_type = command[1]
        var_name = command[2]
        if var_name in self.variables:
            raise NameError(f"the var {var_name} already saved change the name:line {self.current_command_index+1}")

        value = self.eval_exprission(command[3], var_type)
        self.variables[var_name] = {"type": var_type, "value": value}

    def execute_reassign(self, command):
        #[('reassign', 'x',expression)]
        var_name = command[1]
        exeprission = command[2]
        if var_name not in self.variables:
            raise (f"unseen varible {var_name}")
        var_type = self.variables[var_name]["type"]
        value = self.eval_exprission(exeprission)
        self.variables[var_name]["value"] = value

    def eval_exprission(self, expression, var_type=None):

        value = None
        if expression[0] == 'call_functionClass':
            return self.execute_func(expression)

        if var_type in ('array', 'Tuple'):
            value = []
            if expression[0] == 'operation':
                value = self.eval_exprission(expression)
            else:
                for v in expression:
                    value.append(self.eval_exprission(v))
            return Array(value) if var_type == 'array' else MyTuple(*value)
        if expression[0] == 's_value':
            if var_type in {'string', None}:
                return expression[1]
            else:
                raise TypeError('unmatched types between value and var')

        if expression[0] == 'math_func':
            return self.execute_math(expression)
        if expression[0] == 'operation':
            left = expression[1]
            v_l = None
            v_r = None
            op = expression[2]
            right = expression[3]
            if left[0] == 'number':
                v_l = left[1]
            elif left[0] == 'id':
                try:
                    v_l = classes.convert_to_boolean(left[1])
                except:
                    try:
                        v_l = self.variables[left[1]]["value"]
                    except:
                        print("false")
            elif left[0] == 'call_functionClass':
                v_l = self.execute_func(left)
            if right[0] == 'number':
                v_r = right[1]
            if right[0] == 'id':
                try:
                    v_r = self.variables[right[1]]['value']
                except:
                    try:
                        v_r = classes.convert_to_boolean(right[1])

                    except:
                        pass
            elif right[0] == 'call_functionClass':
                v_r = self.execute_func(right)
            if op in {'<', '>', '==', '!=', '||', '&&', '>=', '<='}:
                value = self.execute_condition(v_l,op,v_r)
            elif op in '+-*/':
                value = self.execute_arth(v_l,op,v_r)
            return value
        elif expression[0] == 'number':
            if var_type in {None, 'float', 'int'}:
                number = expression[1]
                return number
            else:
                raise TypeError
        elif expression[0] == 'id':
            if expression[1] in self.variables:
                value = self.variables[expression[1]]["value"]
            elif expression[1] == "True":
                value = True
            elif expression[1] == "False":
                value = False
            else:
                value = expression[1]
            return value
        print(expression)
        raise TypeError
    def execute_if(self):
        command = self.commands[self.current_command_index]
        s_condition = command[1]
        block = command[2]
        else_block = command[3]
        condition = self.eval_exprission(s_condition)
        c_map = {
            True: block,
            False: else_block
        }
        self.execute_block(c_map[condition])

    def execute_block(self, block):
        code = self.commands
        pid = self.current_command_index
        variables = self.variables.copy()
        if block is not None:
            self.commands = block[1]
            self.current_command_index = 0
            self.read_code()
            self.commands = code
            self.current_command_index = pid
            self.variables = variables

    def execute_for(self):
        command = self.commands[self.current_command_index]
        self.execute_assign(command[1])
        block = command[4]
        self.loob(command[2], block, command[3])

    def execute_while(self):
        command = self.commands[self.current_command_index]
        self.loob(command[1], command[2])

    def loob(self, condition, block, rs=None):
        if not self.eval_exprission(condition):
            return
        self.execute_block(block)
        if rs is not None:
            self.execute_reassign(rs)
        self.loob(condition, block, rs)

    def execute_condition(self, left, op, right):
        ops = {
            '>' : my_Math.greater,
            '<' : my_Math.smaller,
            '==': my_Math.equal,
            '>=': my_Math.greater_equal,
            '<=': my_Math.smaller_equal,
            '&&': my_Math.A_nd,
            '||': my_Math.o_r
        }
        fun = ops[op]
        return fun(left, right)

    def execute_arth(self, left, op, right):
        ops = {
            '+': my_Math.add,
            '-': my_Math.subtract,
            '*': my_Math.multiply,
            '/': my_Math.divide,
            '**': my_Math.power,
        }
        fun = ops[op]
        return fun(left, right)

    def execute_print (self):
        command = self.commands[self.current_command_index]
        exprission = command[1]
        print(self.eval_exprission(exprission))

    def execute_math(self,exprission):
        map_m = {
            'add': my_Math.add,
            'subtract': my_Math.subtract,
            'multiply': my_Math.multiply,
            'divide': my_Math.divide,
            'power': my_Math.power,
            'sqrt': my_Math.sqrt,
            'equal': my_Math.equal,
            'not_equal': my_Math.not_equal,
            'greater': my_Math.greater,
            'smaller': my_Math.smaller,
            'o_r': my_Math.o_r,
            'A_nd': my_Math.A_nd
        }
        fun = map_m[exprission[1]]
        arg1 = self.eval_exprission(exprission[2])
        arg2 = self.eval_exprission(exprission[3])
        return fun(arg1,arg2)

    def execute_func(self, command=None):
        global fun_map
        var_name = None
        fun = None
        var_type = None
        if command is None:
            command = self.commands[self.current_command_index]
        var_name = command[1]
        fun = command[2]
        val_type = self.variables[var_name]["type"]
        val_lst = self.variables[var_name]['value']
        fun_name = fun[0]
        par = []
        s_par = fun[1]
        for p in s_par:
            par.append(self.eval_exprission(p))
            fun_map=None
        if val_type == 'array':
             fun_map = {
            'add':val_lst.add,

            'append':val_lst.append,
            'index':val_lst.index,
            'get_value':val_lst.get_value,
            'remove':val_lst.remove,
            'length':val_lst.length
            }
        elif val_type == 'Tuple':
            fun_map={
                'getitem': val_lst.getitem,
                'contains': val_lst.contains,
                'add': val_lst.add,
                'count': val_lst.count,
                'index': val_lst.index,
                'sort': val_lst.sort,
                'length': val_lst.length

            }
        elif val_type == 'string':
            par.append(self.variables[var_name]['value'])
            fun_map = {
                'convert_to_int': classes.convert_to_int,
                'convert_to_float': classes.convert_to_float,
                'convert_to_boolean': classes.convert_to_boolean,
                'split': classes.split,
                'replace': classes.replace,
                'isupper': classes.isupper,
                'islower': classes.islower,
                'concat': classes.concat
            }
        act = fun_map[fun_name]
        return act(*par)

# Example code to parse
