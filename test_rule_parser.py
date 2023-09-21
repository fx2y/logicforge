import unittest

from rule_parser import Lexer, Parser, RuleParser


class TestLexer(unittest.TestCase):
    def test_tokenize(self):
        rule_dsl = 'IF age > 18 AND gender == "male" THEN is_eligible = true'
        lexer = Lexer(rule_dsl)
        lexer.tokenize()
        expected_tokens = [
            ('IF', 'IF'),
            ('IDENTIFIER', 'age'),
            ('>', '>'),
            ('NUMBER', '18'),
            ('AND', 'AND'),
            ('IDENTIFIER', 'gender'),
            ('==', '=='),
            ('STRING', '"male"'),
            ('THEN', 'THEN'),
            ('IDENTIFIER', 'is_eligible'),
            ('=', '='),
            ('IDENTIFIER', 'true')
        ]
        self.assertEqual(lexer.tokens, expected_tokens)


class TestParser(unittest.TestCase):
    def test_parse_expression(self):
        tokens = [
            ('IDENTIFIER', 'age'),
            ('>', '>'),
            ('NUMBER', '18'),
            ('AND', 'AND'),
            ('IDENTIFIER', 'gender'),
            ('==', '=='),
            ('STRING', '"male"')
        ]
        parser = Parser(tokens)
        ast = parser.parse_expression()
        expected_ast = (
            'AND',
            ('>', ('IDENTIFIER', 'age'), ('NUMBER', 18)),
            ('==', ('IDENTIFIER', 'gender'), ('STRING', 'male'))
        )
        self.assertEqual(ast, expected_ast)

    def test_parse_term(self):
        tokens = [
            ('IDENTIFIER', 'age'),
            ('>', '>'),
            ('NUMBER', '18')
        ]
        parser = Parser(tokens)
        ast = parser.parse_term()
        expected_ast = ('>', ('IDENTIFIER', 'age'), ('NUMBER', 18))
        self.assertEqual(ast, expected_ast)

    def test_parse(self):
        tokens = [
            ('IF', 'IF'),
            ('IDENTIFIER', 'age'),
            ('>', '>'),
            ('NUMBER', '18'),
            ('AND', 'AND'),
            ('IDENTIFIER', 'gender'),
            ('==', '=='),
            ('STRING', '"male"'),
            ('THEN', 'THEN'),
            ('IDENTIFIER', 'is_eligible'),
            ('=', '='),
            ('IDENTIFIER', 'true')
        ]
        parser = Parser(tokens)
        ast = parser.parse()
        expected_ast = (
            'IF',
            ('AND',
             ('>', ('IDENTIFIER', 'age'), ('NUMBER', 18)),
             ('==', ('IDENTIFIER', 'gender'), ('STRING', 'male'))
             ),
            ('=', ('IDENTIFIER', 'is_eligible'), ('IDENTIFIER', 'true'))
        )
        self.assertEqual(ast, expected_ast)


class TestRuleParser(unittest.TestCase):
    def test_parse(self):
        rule_dsl = 'IF age > 18 AND gender == "male" THEN is_eligible = true'
        rule_parser = RuleParser(rule_dsl)
        rule_parser.parse()
        expected_ast = (
            'IF',
            ('AND',
             ('>', ('IDENTIFIER', 'age'), ('NUMBER', 18)),
             ('==', ('IDENTIFIER', 'gender'), ('STRING', 'male'))
             ),
            ('=', ('IDENTIFIER', 'is_eligible'), ('IDENTIFIER', 'true'))
        )
        self.assertEqual(rule_parser.ast, expected_ast)


if __name__ == '__main__':
    unittest.main()
