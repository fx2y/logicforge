import re


class Lexer:
    def __init__(self, rule_dsl):
        self.rule_dsl = rule_dsl
        self.tokens = []

    def tokenize(self):
        # Define regular expressions for different symbols and keywords
        regex = r'(?P<IF>IF)|(?P<ELSE>ELSE)|(?P<THEN>THEN)|(?P<AND>AND)|(?P<OR>OR)|(?P<NOT>NOT)|(?P<LPAREN>\()|(?P<RPAREN>\))|(?P<IDENTIFIER>[a-zA-Z_]\w*)|(?P<NUMBER>\d+)|(?P<STRING>"[^"]*")|(?P<WHITESPACE>\s+)|(?P<COMPARISON>[<>!=]=?)'
        pattern = re.compile(regex)
        for match in pattern.finditer(self.rule_dsl):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            if token_type == 'WHITESPACE':
                continue
            if token_type == 'COMPARISON':
                token_type = token_value
            self.tokens.append((token_type, token_value))


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        ast = self.parse_if_statement()
        if self.current_token_index < len(self.tokens):
            raise Exception('Unexpected token')
        return ast

    def parse_if_statement(self):
        if_token = self.get_next_token()
        if if_token[0] != 'IF':
            return self.parse_expression()
        condition = self.parse_expression()
        then_token = self.get_next_token()
        if then_token[0] != 'THEN':
            raise Exception('Expected THEN')
        then_expression = self.parse_expression()
        return ('IF', condition, then_expression)

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token[0] in ('AND', 'OR'):
                self.current_token_index += 1
                right = self.parse_term()
                left = (token[0], left, right)
            else:
                break
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token[0] in ('>', '<', '==', '!=', '>=', '<=', '='):
                self.current_token_index += 1
                right = self.parse_factor()
                left = (token[0], left, right)
            else:
                break
        return left

    def parse_factor(self):
        token = self.tokens[self.current_token_index]
        if token[0] == 'IDENTIFIER':
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == 'LPAREN':
                self.current_token_index += 1
                args = self.parse_argument_list()
                if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != 'RPAREN':
                    raise Exception('Expected )')
                self.current_token_index += 1
                return ('FUNCTION', token[1], args)
            else:
                return ('IDENTIFIER', token[1])
        elif token[0] == 'NOT':
            self.current_token_index += 1
            factor = self.parse_factor()
            return ('NOT', factor)
        elif token[0] == 'LPAREN':
            self.current_token_index += 1
            expression = self.parse_expression()
            if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != 'RPAREN':
                raise Exception('Expected )')
            self.current_token_index += 1
            return expression
        elif token[0] == 'NUMBER':
            self.current_token_index += 1
            return ('NUMBER', int(token[1]))
        elif token[0] == 'STRING':
            self.current_token_index += 1
            return ('STRING', token[1][1:-1])
        else:
            raise Exception('Unexpected token')

    def parse_argument_list(self):
        args = []
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] != 'RPAREN':
            args.append(self.parse_expression())
            while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == 'COMMA':
                self.current_token_index += 1
                args.append(self.parse_expression())
        return args

    def get_next_token(self):
        if self.current_token_index >= len(self.tokens):
            return None
        token = self.tokens[self.current_token_index]
        self.current_token_index += 1
        return token


class RuleParser:
    def __init__(self, rule_dsl):
        self.rule_dsl = rule_dsl
        self.tokens = []
        self.ast = None

    def parse(self):
        lexer = Lexer(self.rule_dsl)
        lexer.tokenize()
        self.tokens = lexer.tokens
        parser = Parser(self.tokens)
        self.ast = parser.parse()
