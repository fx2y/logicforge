import re


class Lexer:
    def __init__(self, rule_dsl):
        self.rule_dsl = rule_dsl
        self.tokens = []

    def tokenize(self):
        # Define regular expressions for different symbols and keywords
        regex = r'\b\w+\b|\(|\)|\d+\.\d+|\d+|[><]=?|=|!=|\&\&|\|\||\'[^\']*\''
        matches = re.findall(regex, self.rule_dsl)
        for match in matches:
            if match.strip():
                self.tokens.append(match.strip())

        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.ast = None

    def parse(self):
        self.advance()
        self.ast = self.rule()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def rule(self):
        # A rule consists of one or more conditions followed by one or more conclusions
        conditions = []
        conclusions = []

        # Parse conditions
        while self.current_token is not None and self.current_token != 'THEN':
            condition = self.expression()
            conditions.append(condition)
            if self.current_token == 'AND':
                self.advance()
            else:
                break   # Exit loop if no more conditions or THEN keyword found

        # Parse conclusions
        if self.current_token == 'THEN':
            self.advance()
            while self.current_token is not None:
                variable = self.variable()
                self.advance()  # Skip '='
                value = self.value()
                conclusion = {
                    'type': 'assignment',
                    'variable': variable,
                    'value': value
                }
                conclusions.append(conclusion)
                if self.current_token == ',':
                    self.advance()

        return {
            'type': 'rule',
            'conditions': conditions,
            'conclusions': conclusions
        }

    def variable(self):
        # A variable is a string of alphanumeric characters
        if self.current_token is not None and re.match(r'^\w+$', self.current_token):
            return {
                'type': 'variable',
                'name': self.current_token
            }
        else:
            raise ValueError(f'Invalid variable name: {self.current_token}')

    def value(self):
        # A value can be a number, string, or boolean
        if self.current_token is not None:
            if re.match(r'^\d+(\.\d+)?$', self.current_token):
                return {
                    'type': 'number',
                    'value': float(self.current_token)
                }
            elif re.match(r"^'.*'$", self.current_token):
                return {
                    'type': 'string',
                    'value': self.current_token[1:-1]
                }
            elif self.current_token == 'true' or self.current_token == 'false':
                return {
                    'type': 'boolean',
                    'value': self.current_token == 'true'
                }
            else:
                raise ValueError(f'Invalid value: {self.current_token}')

    def expression(self):
        # An expression can be a variable, value, or combination of the two with an operator
        left = self.term()
        while self.current_token is not None and self.current_token in ['>', '>=', '=', '!=', '<', '<=']:
            operator = self.current_token
            self.advance()
            right = self.term()
            left = {
                'type': 'expression',
                'operator': operator,
                'left': left,
                'right': right
            }
        return left

    def term(self):
        # A term can be a factor or a combination of factors with an operator
        left = self.factor()
        while self.current_token is not None and self.current_token in ['+', '-']:
            operator = self.current_token
            self.advance()
            right = self.factor()
            left = {
                'type': 'expression',
                'operator': operator,
                'left': left,
                'right': right
            }
        return left

    def factor(self):
        # A factor can be a variable, value, or expression in parentheses
        if self.current_token == '(':
            self.advance()
            expression = self.expression()
            if self.current_token == ')':
                self.advance()
                return expression
            else:
                raise ValueError(f'Expected ")" but found {self.current_token}')
        elif re.match(r'^\w+$', self.current_token):
            return self.variable()
        else:
            return self.value()


class RuleParser:
    def __init__(self, rule_dsl):
        self.rule_dsl = rule_dsl
        self.tokens = []
        self.ast = None

    def parse(self):
        lexer = Lexer(self.rule_dsl)
        self.tokens = lexer.tokenize()
        parser = Parser(self.tokens)
        parser.parse()
        self.ast = parser.ast
