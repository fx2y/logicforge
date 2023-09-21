import unittest

from compiler import Compiler
from rule_engine import RuleEngine, Rule, Condition, Action, Expression


class TestRule(unittest.TestCase):
    def test_evaluate_true(self):
        condition = Condition(Expression('>', 'age', 18))
        action = Action(Expression('=', 'is_eligible', True))
        rule = Rule(condition, action)
        facts = {'age': 20, 'is_eligible': False}
        rule.evaluate(facts)
        self.assertEqual(facts['is_eligible'], True)

    def test_evaluate_false(self):
        condition = Condition(Expression('>', 'age', 18))
        action = Action(Expression('=', 'is_eligible', True))
        rule = Rule(condition, action)
        facts = {'age': 16, 'is_eligible': False}
        rule.evaluate(facts)
        self.assertEqual(facts['is_eligible'], False)


class TestCondition(unittest.TestCase):
    def test_evaluate_true(self):
        expression = Expression('>', 'age', 18)
        condition = Condition(expression)
        facts = {'age': 20}
        self.assertEqual(condition.evaluate(facts), True)

    def test_evaluate_false(self):
        expression = Expression('>', 'age', 18)
        condition = Condition(expression)
        facts = {'age': 16}
        self.assertEqual(condition.evaluate(facts), False)


class TestAction(unittest.TestCase):
    def test_execute(self):
        expression = Expression('=', 'is_eligible', True)
        action = Action(expression)
        facts = {'is_eligible': False}
        action.execute(facts)
        self.assertEqual(facts['is_eligible'], True)


class TestRuleEngine(unittest.TestCase):
    def test_execute(self):
        condition1 = Condition(Expression('>', 'age', 18))
        action1 = Action(Expression('=', 'is_eligible', True))
        rule1 = Rule(condition1, action1)

        condition2 = Condition(Expression('==', 'gender', 'male'))
        action2 = Action(Expression('+=', 'male_count', 1))
        rule2 = Rule(condition2, action2)

        condition3 = Condition(Expression('==', 'gender', 'female'))
        action3 = Action(Expression('+=', 'female_count', 1))
        rule3 = Rule(condition3, action3)

        rules = [rule1, rule2, rule3]
        facts = {'age': 20, 'gender': 'male', 'is_eligible': False, 'male_count': 0, 'female_count': 0}
        rule_engine = RuleEngine(rules)
        rule_engine.execute(facts)
        self.assertEqual(facts['is_eligible'], True)
        self.assertEqual(facts['male_count'], 1)
        self.assertEqual(facts['female_count'], 0)


class TestCompiler(unittest.TestCase):
    def test_compile(self):
        ast = (
            'IF',
            ('AND',
             ('>', ('IDENTIFIER', 'age'), ('NUMBER', 18)),
             ('==', ('IDENTIFIER', 'gender'), ('STRING', 'male'))
             ),
            ('=', ('IDENTIFIER', 'is_eligible'), ('IDENTIFIER', 'true'))
        )
        compiler = Compiler(ast)
        rules = [compiler.compile()]
        facts = {'age': 20, 'gender': 'male', 'is_eligible': False}
        rule_engine = RuleEngine(rules)
        rule_engine.execute(facts)
        self.assertEqual(facts['is_eligible'], True)
