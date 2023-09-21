import unittest

from rule_parser import RuleParser


class TestRuleParser(unittest.TestCase):
    def test_parse_simple_rule(self):
        rule_dsl = "IF age > 18 THEN is_adult = true"
        rule_parser = RuleParser(rule_dsl)
        rule_parser.parse()
        expected_tokens = ["IF", "age", ">", "18", "THEN", "is_adult", "=", "true"]
        self.assertEqual(rule_parser.tokens, expected_tokens)

    def test_parse_complex_rule(self):
        rule_dsl = "IF age > 18 AND gender = 'male' THEN is_adult = true"
        rule_parser = RuleParser(rule_dsl)
        rule_parser.parse()
        expected_tokens = ["IF", "age", ">", "18", "AND", "gender", "=", "'male'", "THEN", "is_adult", "=", "true"]
        self.assertEqual(rule_parser.tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
