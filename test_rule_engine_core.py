import unittest

from agenda import Agenda
from rule_engine import Condition, Expression, Action, Rule
from rule_engine_core import RuleEngineCore, WorkingMemory


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


class TestAgenda(unittest.TestCase):
    def test_add_rule(self):
        rule1 = Rule(None, None)
        rule2 = Rule(None, None)
        agenda = Agenda()
        agenda.add_rule(rule1, 1)
        agenda.add_rule(rule2, 2)
        expected_rules = [(1, rule1), (2, rule2)]
        self.assertEqual(agenda.rules, expected_rules)

    def test_remove_rule(self):
        rule1 = Rule(None, None)
        rule2 = Rule(None, None)
        agenda = Agenda()
        agenda.add_rule(rule1, 1)
        agenda.add_rule(rule2, 2)
        agenda.remove_rule(rule1)
        expected_rules = [(2, rule2)]
        self.assertEqual(agenda.rules, expected_rules)

    def test_update_rule(self):
        rule1 = Rule(None, None)
        rule2 = Rule(None, None)
        agenda = Agenda()
        agenda.add_rule(rule1, 1)
        agenda.add_rule(rule2, 2)
        agenda.update_rule(rule1, 3)
        expected_rules = [(2, rule2), (3, rule1)]
        self.assertEqual(agenda.rules, expected_rules)

    def test_get_next_rule(self):
        rule1 = Rule(None, None)
        rule2 = Rule(None, None)
        agenda = Agenda()
        agenda.add_rule(rule1, 1)
        agenda.add_rule(rule2, 2)
        next_rule = agenda.get_next_rule()
        self.assertEqual(next_rule, rule1)
        next_rule = agenda.get_next_rule()
        self.assertEqual(next_rule, rule2)
        next_rule = agenda.get_next_rule()
        self.assertEqual(next_rule, None)


class TestRuleEngineCore(unittest.TestCase):
    def test_execute(self):
        condition1 = Condition(Expression('>', 'age', 18))
        action1 = Action(Expression('=', 'is_eligible', True))
        rule1 = Rule(condition1, action1)
        rule1.priority = 1

        condition2 = Condition(Expression('==', 'is_eligible', True))
        action2 = Action(Expression('=', 'discount', 0.1))
        rule2 = Rule(condition2, action2)
        rule2.priority = 2

        rules = [rule1, rule2]

        working_memory = WorkingMemory({'age': 20})
        rule_engine_core = RuleEngineCore(rules)
        rule_engine_core.working_memory = working_memory
        rule_engine_core.execute()

        expected_facts = {'age': 20, 'is_eligible': True, 'discount': 0.1}
        self.assertEqual(rule_engine_core.working_memory.facts, expected_facts)
