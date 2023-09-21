import unittest

from rule_parser import Lexer


class TestLexer(unittest.TestCase):
    def test_tokenize_simple_rule(self):
        rule_dsl = "IF age > 18 THEN is_adult = true"
        lexer = Lexer(rule_dsl)
        tokens = lexer.tokenize()
        expected_tokens = ["IF", "age", ">", "18", "THEN", "is_adult", "=", "true"]
        self.assertEqual(expected_tokens, tokens)

    def test_tokenize_complex_rule(self):
        rule_dsl = "IF age > 18 AND gender = 'male' THEN is_adult = true"
        lexer = Lexer(rule_dsl)
        tokens = lexer.tokenize()
        expected_tokens = ["IF", "age", ">", "18", "AND", "gender", "=", "'male'", "THEN", "is_adult", "=", "true"]
        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
