import unittest

from rule_parser import RuleParser, Lexer


class TestRuleParser(unittest.TestCase):
    def test_lexer_tokenize(self):
        rule_dsl = 'IF age > 18 AND gender == "male" THEN is_eligible = true'
        lexer = Lexer(rule_dsl)
        lexer.tokenize()
        expected_tokens = [
            ('IDENTIFIER', 'IF'),
            ('IDENTIFIER', 'age'),
            ('COMPARISON', '>'),
            ('NUMBER', '18'),
            ('AND', 'AND'),
            ('IDENTIFIER', 'gender'),
            ('COMPARISON', '=='),
            ('STRING', '"male"'),
            ('IDENTIFIER', 'THEN'),
            ('IDENTIFIER', 'is_eligible'),
            ('COMPARISON', '='),
            ('IDENTIFIER', 'true')
        ]
        self.assertEqual(lexer.tokens, expected_tokens)

    def test_rule_parser_parse(self):
        rule_dsl = 'IF age > 18 AND gender == "male" THEN is_eligible = true'
        rule_parser = RuleParser(rule_dsl)
        rule_parser.parse()
        # Implement assertions to test the parsed objects
        # ...


if __name__ == '__main__':
    unittest.main()
