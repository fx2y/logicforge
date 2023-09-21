import unittest

from rule_engine import Condition, Expression, Action, Rule
from rule_engine_core import RuleEngineCore


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


class TestRuleEngineCore(unittest.TestCase):
    def test_execute_single_rule(self):
        condition = Condition(Expression('>', 'age', 18))
        action = Action(Expression('=', 'is_eligible', True))
        rule = Rule(condition, action)
        rules = [rule]
        rule_engine_core = RuleEngineCore(rules)
        rule_engine_core.working_memory.add_fact('age', 20)
        rule_engine_core.execute()
        self.assertEqual(rule_engine_core.working_memory.facts['is_eligible'], True)

    def test_execute_multiple_rules(self):
        condition1 = Condition(Expression('>', 'age', 18))
        action1 = Action(Expression('=', 'is_eligible', True))
        rule1 = Rule(condition1, action1)
        condition2 = Condition(Expression('==', 'gender', 'male'))
        action2 = Action(Expression('=', 'is_male', True))
        rule2 = Rule(condition2, action2)
        rules = [rule1, rule2]
        rule_engine_core = RuleEngineCore(rules)
        rule_engine_core.working_memory.add_fact('age', 20)
        rule_engine_core.working_memory.add_fact('gender', 'male')
        rule_engine_core.execute()
        self.assertEqual(rule_engine_core.working_memory.facts['is_eligible'], True)
        self.assertEqual(rule_engine_core.working_memory.facts['is_male'], True)

    def test_execute_no_rules(self):
        rules = []
        rule_engine_core = RuleEngineCore(rules)
        rule_engine_core.working_memory.add_fact('age', 20)
        rule_engine_core.execute()
        self.assertEqual(rule_engine_core.working_memory.facts, {'age': 20})
