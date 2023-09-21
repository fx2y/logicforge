import unittest

from rule_parser import Parser


class TestParser(unittest.TestCase):
    def test_parse_expression(self):
        parser = Parser(['age', '>', '18'])
        parser.parse()
        ast = parser.ast
        self.assertEqual(ast['type'], 'expression')
        self.assertEqual(ast['operator'], '>')
        self.assertEqual(ast['left']['type'], 'variable')
        self.assertEqual(ast['left']['name'], 'age')
        self.assertEqual(ast['right']['type'], 'number')
        self.assertEqual(ast['right']['value'], 18)

    def test_parse_rule_single_condition(self):
        parser = Parser(['IF', 'age', '>', '18', 'THEN', 'is_adult', '=', 'true'])
        parser.parse()
        ast = parser.ast
        self.assertEqual(ast['type'], 'rule')
        self.assertEqual(ast['conditions'][0]['type'], 'expression')
        self.assertEqual(ast['conditions'][0]['operator'], '>')
        self.assertEqual(ast['conditions'][0]['left']['type'], 'variable')
        self.assertEqual(ast['conditions'][0]['left']['name'], 'age')
        self.assertEqual(ast['conditions'][0]['right']['type'], 'number')
        self.assertEqual(ast['conditions'][0]['right']['value'], 18)
        self.assertEqual(ast['conclusions'][0]['type'], 'assignment')
        self.assertEqual(ast['conclusions'][0]['variable']['type'], 'variable')
        self.assertEqual(ast['conclusions'][0]['variable']['name'], 'is_adult')
        self.assertEqual(ast['conclusions'][0]['value']['type'], 'boolean')
        self.assertEqual(ast['conclusions'][0]['value']['value'], True)

    def test_parse_rule_multiple_conditions(self):
        parser = Parser(['IF', 'age', '>', '18', 'AND', 'gender', '=', "'male'", 'THEN', 'is_adult', '=', 'true'])
        parser.parse()
        ast = parser.ast
        self.assertEqual(ast['type'], 'rule')
        self.assertEqual(len(ast['conditions']), 2)
        self.assertEqual(ast['conditions'][0]['type'], 'expression')
        self.assertEqual(ast['conditions'][0]['operator'], '>')
        self.assertEqual(ast['conditions'][0]['left']['type'], 'variable')
        self.assertEqual(ast['conditions'][0]['left']['name'], 'age')
        self.assertEqual(ast['conditions'][0]['right']['type'], 'number')
        self.assertEqual(ast['conditions'][0]['right']['value'], 18)
        self.assertEqual(ast['conditions'][1]['type'], 'expression')
        self.assertEqual(ast['conditions'][1]['operator'], '=')
        self.assertEqual(ast['conditions'][1]['left']['type'], 'variable')
        self.assertEqual(ast['conditions'][1]['left']['name'], 'gender')
        self.assertEqual(ast['conditions'][1]['right']['type'], 'string')
        self.assertEqual(ast['conditions'][1]['right']['value'], 'male')
        self.assertEqual(ast['conclusions'][0]['type'], 'assignment')
        self.assertEqual(ast['conclusions'][0]['variable']['type'], 'variable')
        self.assertEqual(ast['conclusions'][0]['variable']['name'], 'is_adult')
        self.assertEqual(ast['conclusions'][0]['value']['type'], 'boolean')
        self.assertEqual(ast['conclusions'][0]['value']['value'], True)


if __name__ == '__main__':
    unittest.main()
