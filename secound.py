"""
Mahmoud Abo Hamd - 325092708
Ghada Abu Sbetan - 212632129
Muhamed Dahly - 212806996
Osama Shtewe - 211404207
"""
import classes


class Lexer:
    def __init__(self, source_code):
        self.code = source_code
        self.pos = 0
        self.tokens = []
        self.current_char = self.code[self.pos] if self.code else None

    def next(self):
        self.pos += 1
        self.current_char = self.code[self.pos] if self.pos < len(self.code) else None

    def tokenize(self):
        while self.current_char is not None:
            if self.current_char in ' \t\n':
                self.next()
            elif self.current_char.isdigit():
                self.tokens.append(('NUMBER', self.number()))
            elif self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self.identifier_or_keyword())
            elif self.current_char == '=':
                self.next()
                if self.current_char == '=':
                    self.next()
                    self.tokens.append(('OP', '=='))
                else:
                    self.tokens.append(('ASSIGN', '='))
            elif self.current_char == '[':
                self.next()
                self.tokens.append(('LBRACKET', '['))
            elif self.current_char == ']':
                self.tokens.append(('RBRACKET', ']'))
                self.next()
            elif self.current_char == ',':
                self.tokens.append(('COMMA', ','))
                self.next()
            elif self.current_char == '.':
                self.tokens.append(('DOT', '.'))
                self.next()
            elif self.current_char == '!':
                self.next()
                if self.current_char == '=':
                    self.next()
                    self.tokens.append(('OP', '!='))
                else:
                    raise RuntimeError(f'Unexpected character: {self.current_char}')
            elif self.current_char in '+-*/':
                self.tokens.append(('OP', self.current_char))
                self.next()
            elif self.current_char == '>':
                self.next()
                if self.current_char == '=':
                    self.next()
                    self.tokens.append(('OP', '>='))
                else:
                    self.tokens.append(('OP', '>'))

            elif self.current_char == '<':
                self.next()
                if self.current_char == '=':
                    self.next()
                    self.tokens.append(('OP', '<='))
                else:
                    self.tokens.append(('OP', '<'))
            elif self.current_char == '{':
                self.tokens.append(('BRACE', '{'))

                self.next()
            elif self.current_char == '}':
                self.tokens.append(('BRACE', '}'))
                self.next()
            elif self.current_char == '"':
                self.tokens.append(('DITTO', '"'))
                self.next()
                self.tokens.append(('ID',self.string_manege()))
                self.tokens.append(('DITTO','"'))
                self.next()
            elif self.current_char == '(':
                self.tokens.append(('PAREN', '('))
                self.next()
            elif self.current_char == ')':
                self.tokens.append(('PAREN', ')'))
                self.next()
            elif self.current_char == '&':
                self.tokens.append(self.check_and_token())
            elif self.current_char == '|':
                self.tokens.append(self.check_or_token())
            elif self.current_char == ';':
                self.tokens.append(('ENDLINE', ';'))
                self.next()
            else:
                raise RuntimeError(f'Unexpected character: {self.current_char}')
        return self.tokens

    def number(self):
        num_str = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.' and num_str != '' and self.code[self.pos+1].isdigit():
                num_str += self.current_char
            elif self.current_char == '.':
                raise ValueError("unreadable value ")
            else:
                num_str += self.current_char

            self.next()
        return classes.convert_to_float(num_str) if '.' in num_str else classes.convert_to_int(num_str)

    def identifier_or_keyword(self):
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.next()
        keywords = {'if', 'else', 'while', 'for', 'print'}
        if id_str in keywords:
            return (id_str.upper(), id_str)
        types = {"int", "float", "string", "char", "boolean", "array", "Tuple"}
        if id_str in types:
            return (id_str.upper(), id_str)
        if id_str == 'print':
            return (id_str.upper(), id_str)
        if id_str == 'math':
            return ('MATH', 'math')
        if id_str == 'string':
            return ('STRING', 'string')
        if id_str == 'array':
            return ('ARRAY', 'arrays')
        if id_str == 'tuple':
            return ('TUPLE', 'tuple')

        return ('ID', id_str)
    def string_manege(self):
        id_str = ''
        while self.current_char != '"':
            id_str += self.current_char
            self.next()
        return id_str


    def check_and_token(self):
        if self.code[self.pos:self.pos + 2] == "&&":
            self.pos += 2
            self.current_char = self.code[self.pos] if self.pos < len(self.code) else None
            return ('OP', '&&')
        else:
            raise RuntimeError(f'Unexpected character sequence: {self.current_char}')

    def check_or_token(self):
        if self.code[self.pos:self.pos + 2] == "||":
            self.pos += 2
            self.current_char = self.code[self.pos] if self.pos < len(self.code) else None
            return ('OP', '||')
        else:
            raise RuntimeError(f'Unexpected character sequence: {self.current_char}')


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.varibles = {}

    def parse(self):
        return self.statements()

    def statements(self):
        stmts = []
        while self.current_token_index < len(self.tokens):
            stmt = self.statement()
            if stmt:
                stmts.append(stmt)
        return stmts

    def statement(self):
        if self.current_token_index >= len(self.tokens):
            return None
        token_type, token_value = self.tokens[self.current_token_index]
        if token_type == "PRINT":
            return self.print_statement()
        if token_value in {"if", "while", "for"}:
            return self.control_statement(token_value)
        if token_type in {"INT", "FLOAT", "STRING", "CHAR", "BOOLEAN", "ARRAY", "TUPLE"}:
            return self.assignment()

        elif token_type == 'ID':
            return self.reassignment()
        else:
            raise SyntaxError(f"Unexpected token: {token_value}")

    def assignment(self):
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        var_type = self.tokens[self.current_token_index][1]
        self.current_token_index += 1  # Skip type

        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "ID":
            raise SyntaxError("Expected variable name")
        var_name = self.tokens[self.current_token_index][1]
        self.current_token_index += 1  # Skip name
        if var_name in self.varibles:
            raise NameError(f"the var {var_name} already saved change the name")
        self.varibles[var_name] = var_type
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "ASSIGN":
            raise SyntaxError("Expected '=' for assignment")
        self.current_token_index += 1  # Skip '='
        current_token = self.tokens[self.current_token_index]
        if var_type in ('array', 'Tuple', 'string') and current_token[0] == 'ID':
            try:
                expr = self.fun(current_token)
            except:
                self.current_token_index-=1
                expr = self.expression()
        else:
            expr = self.expression()

        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == "ENDLINE":
            self.current_token_index += 1  # Skip end of line

        return ('assign', var_type, var_name, expr)

    def print_statement(self):
        self.current_token_index += 1  # Skip 'print'
        expr = self.expression()
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == "ENDLINE":
            self.current_token_index += 1  # Skip end of line
        return ('print', expr)

    def reassignment(self):
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "ID":
            raise SyntaxError("Expected variable name")
        var_name = self.tokens[self.current_token_index][1]
        self.current_token_index += 1  # Skip ID
        current_token = self.tokens[self.current_token_index]
        if (self.current_token_index >= len(self.tokens) or (self.tokens[self.current_token_index][0] != "ASSIGN" and
                                                             current_token[0] != 'DOT')):
            raise SyntaxError("Expected '=' for reassignment")
        if var_name not in self.varibles:
            raise "the variable is not found"

        var_type = self.varibles[var_name]
        if var_type in ('array', 'Tuple', 'string') and current_token[1] == '.':
            self.current_token_index += 1  # Skip '.'
            current_token = self.tokens[self.current_token_index]
            return ('call_functionClass', var_name, self.fun(current_token))
        else:
            self.current_token_index += 1  # Skip '='/'.'

            expr = self.expression()
            return ('reassign', var_name, expr)

    def fun(self, current_token=None):
        # fun_name(parameters)
        if current_token is None:
            current_token = self.tokens[self.current_token_index]
        if current_token[0] not in ('ID', 'str_fun'):
            raise SyntaxError("unreadble function name")
        name = current_token[1]

        self.current_token_index += 1  # skip
        current_token = self.tokens[self.current_token_index]
        if current_token[0] == 'DOT':
            var_name = name
            self.current_token_index += 1  # skip '.'
            current_token = self.tokens[self.current_token_index]
            return ("call_functionClass", var_name, self.fun(current_token))
        if current_token[0] != 'PAREN' or current_token[1] != '(':
            print(current_token)
            raise SyntaxError("excepted '('")
        self.current_token_index += 1  # skip '('
        current_token = self.tokens[self.current_token_index]
        par = []
        while current_token[1] != ')':
            arg = self.expression()
            par.append(arg)
            current_token = self.tokens[self.current_token_index]
            if current_token[1] == ',':
                self.current_token_index += 1  # skip ','
                current_token = self.tokens[self.current_token_index]
            elif current_token[1] == ')':
                break
        self.current_token_index += 1  # skip')'
        return (name, par)

    def control_statement(self, stmt_type):
        if stmt_type not in {"if", "while", "for"}:
            raise SyntaxError(f"Unsupported control statement: {stmt_type}")
        assi = None
        re_assi = None

        self.current_token_index += 1  # Skip the control statement keyword
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "PAREN" or \
                self.tokens[self.current_token_index][1] != '(':
            raise SyntaxError("Expected '(' after control statement")
        self.current_token_index += 1  # Skip '('
        if stmt_type in ("if", "while"):
            condition = self.expression()
        else:
            assi = self.assignment()
            self.current_token_index += 1  # skip ','
            condition = self.expression()
            self.current_token_index += 1  # skip ','
            re_assi = self.reassignment()
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "PAREN" or \
                self.tokens[self.current_token_index][1] != ')':
            raise SyntaxError("Expected ')' after condition")
        self.current_token_index += 1  # Skip ')'

        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "BRACE" or \
                self.tokens[self.current_token_index][1] != '{':
            raise SyntaxError("Expected '{' after condition")
        self.current_token_index += 1  # Skip '{'

        block = self.block()
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "BRACE" or \
                self.tokens[self.current_token_index][1] != '}':
            raise SyntaxError("Expected '}' at the end of the block")
        self.current_token_index += 1  # Skip '}'
        if self.current_token_index <= len(self.tokens):
            try:
                if self.tokens[self.current_token_index][1] == "else":
                    self.current_token_index += 1  # skip else
                    self.current_token_index += 1
                    block_false = self.block()
                    self.current_token_index += 1  # skip }
                    return (stmt_type, condition, block, block_false)
            except:
                pass
        if stmt_type == 'for':
            return (stmt_type, assi, condition, re_assi, block)
        return (stmt_type, condition, block, None)

    def expression(self):
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")

        token_type, token_value = self.tokens[self.current_token_index]
        if token_type == 'MATH':
            return self.math_expression()
        elif token_type == 'NUMBER':
            self.current_token_index += 1
            left_expr = ('number', token_value)
        elif token_type == 'ID':
            left_expr = self.id_edit()
        elif token_type == 'BOOL':
            left_expr = ('bool', token_value)
        elif token_type == 'PAREN':
            left_expr = self.tuple_handle()
        elif token_type == 'LBRACKET':
            left_expr = self.array_handle()
        elif token_type == 'DITTO':
            self.current_token_index += 1  # skip ditto
            value = self.tokens[self.current_token_index]
            self.current_token_index += 2   # skip string and ditto
            left_expr = ('s_value', value[1])
        elif token_type == 'TUPLE':
            left_expr = ('tuple', token_value)
        elif token_type == 'str_fun':
            left_expr = self.fun(self.tokens[self.current_token_index])
        else:
            raise SyntaxError(f"Unexpected token in expression: {token_value}")
        if self.current_token_index < len(self.tokens):
            token_type, token_value = self.tokens[self.current_token_index]
            if token_type == 'OP':
                operator = token_value
                self.current_token_index += 1
                right_expr = self.expression()
                return ('operation', left_expr, operator, right_expr)
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == "ENDLINE":
            self.current_token_index += 1  # Skip end of line
        return left_expr

    def id_edit(self):
        current_token = self.tokens[self.current_token_index]
        name = current_token[1]
        if name in self.varibles:
            self.current_token_index += 1

            if self.current_token_index < len(self.tokens):
                current_token = self.tokens[self.current_token_index]
                if current_token[1] == '.':

                    self.current_token_index -= 1
                    return self.fun()
                else:
                    return ('id', name)
            else:
                return ('id', name)
        else:
            self.current_token_index += 1
            return ('id', name)

    def math_expression(self):
        # Handling "math.add(2, 3)" type expressions
        self.current_token_index += 1  # Skip 'math'
        current_token = self.tokens[self.current_token_index]

        if current_token[0] == 'DOT':
            self.current_token_index += 1

            current_token = self.tokens[self.current_token_index]

            if current_token[0] == 'ID':  # Function name (e.g., add)

                func_name = current_token[1]
                self.current_token_index += 1
                current_token = self.tokens[self.current_token_index]
                if current_token[0] == 'PAREN' and current_token[1] == '(':

                    self.current_token_index += 1  # Skip '('

                    arg1 = self.expression()
                    current_token = self.tokens[self.current_token_index]
                    if current_token[0] == 'COMMA':
                        self.current_token_index += 1  # Skip ','
                        arg2 = self.expression()
                        current_token = self.tokens[self.current_token_index]
                        if current_token[0] == 'PAREN' and current_token[1] == ')':
                            self.current_token_index += 1  # Skip ','p

                        return ('math_func', func_name, arg1, arg2)

    def block(self):
        statements = []
        while self.current_token_index < len(self.tokens) and not (
             self.tokens[self.current_token_index][0] == "BRACE" and self.tokens[self.current_token_index][1] == '}'):
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] == "BRACE" or \
                self.tokens[self.current_token_index][1] == '}':
            return ('block', statements)

    def array_handle(self):
        self.match('LBRACKET')
        elements = []
        current_token = self.tokens[self.current_token_index]
        if current_token[0] != 'RBRACKET':

            elements.append(self.expression())
            current_token = self.tokens[self.current_token_index]
            while current_token[0] == 'COMMA':
                self.current_token_index += 1
                elements.append(self.expression())

                current_token = self.tokens[self.current_token_index]

        self.match('RBRACKET')
        return (elements)

    def tuple_handle(self):
        self.match('PAREN')
        elements = []
        current_token = self.tokens[self.current_token_index]
        if current_token[0] != 'PAREN':

            elements.append(self.expression())
            current_token = self.tokens[self.current_token_index]
            while current_token[0] == 'COMMA':
                self.current_token_index += 1
                elements.append(self.expression())

                current_token = self.tokens[self.current_token_index]

        self.match('PAREN')
        return (elements)

    def match(self, expected_type, expected_value=None):
        current_token = self.tokens[self.current_token_index]
        if current_token[0] == expected_type and (
                expected_value is None or current_token[1] == expected_value):
            self.current_token_index += 1
        else:
            raise SyntaxError(f"Expected {expected_type} {expected_value}, found {current_token}")


class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.declared_variables = {}
        self.errors = []

    def analyze(self):
        self.visit(self.ast)
        return self.errors

    def visit(self, node):
        if node is None:
            return
        method_name = f"visit_{node[0]}"
        visit_method = getattr(self, method_name, self.generic_visit)
        return visit_method(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for child in node:
                self.visit(child)

    def visit_assign(self, node):
            # node: ('assign', var_type, var_name, expr)
            var_type, var_name, expr = node[1], node[2], node[3]

            # Check if the variable is already declared
            if var_name in self.declared_variables:
                self.errors.append(f"Variable '{var_name}' already declared.")
            else:
                self.declared_variables[var_name] = var_type

            # Check if the right-hand side (expr) is a valid and declared variable or expression
            if var_type == 'id' and var_name not in self.declared_variables and var_type not in ('string', 'char', 'boolean', 'array', 'tuple'):
                self.errors.append(f"Variable '{expr[1]}' used before declaration.")
            if len(expr) > 0:
                self.visit(expr)

    def get_expression_type(self, expr):
            if expr[0] == 'number':
                return 'int' if isinstance(expr[1], int) else 'float'
            elif expr[0] == 'boolean':
                return 'boolean'
            elif expr[0] == 'array':
                return 'array'
            elif expr[0] == 'tuple':
                return 'tuple'
            elif expr[0] == 'id':
                return self.declared_variables.get(expr[1])
            # Add more cases as needed for different expression types.
            elif expr[0] == 's_value':
                return 'string'
            return None

    def visit_reassign(self, node):
        # node: ('reassign', var_name, expr)
        var_name, expr = node[1], node[2]
        if var_name not in self.declared_variables:
            self.errors.append(f"Variable '{var_name}' used before declaration.")
        var_type = self.declared_variables[var_name]

        self.visit(expr)

    def visit_operation(self, node):
        # node: ('operation', left_expr, operator, right_expr)
        left_expr, operator, right_expr = node[1], node[2], node[3]
        self.visit(left_expr)
        self.visit(right_expr)

    def visit_number(self, node):
        # node: ('number', value)
        pass

    def visit_print(self, node):
        # node: ('print', expr)
        expr = node[1]
        expr_type = self.get_expression_type(expr)
        if expr_type is None:
            self.errors.append("Cannot print value of unknown type.")
        self.visit(expr)

    def visit_id(self, node):
        # node: ('id', var_name)
        pass

    def visit_block(self, node):
        # node: ('block', statements)
        self.visit(node[1])

    def visit_if(self, node):
        # node: ('if', condition, block_true, block_false)
        self.visit(node[1])
        self.visit(node[2])
        if node[3] is not None:
            self.visit(node[3])

    def visit_while(self, node):
        # node: ('while', condition, block)
        self.visit(node[1])
        self.visit(node[2])

    def visit_for(self, node):
        # node: ('for', initialization, condition, increment, )
        self.visit(node[1])
        self.visit(node[2])
        self.visit(node[3])
        self.visit(node[4])
# Example code to parse


