from rule_engine import Expression, Condition, Action, Rule
from rule_engine_core import RuleEngineCore

condition1 = Condition(Expression('>', 'age', 18))
action1 = Action(Expression('=', 'is_eligible', True))
rule1 = Rule(condition1, action1)
rule1.priority = 1

condition2 = Condition(Expression('==', 'is_eligible', True))
action2 = Action(Expression('=', 'discount', 0.1))
rule2 = Rule(condition2, action2)
rule2.priority = 2

rules = [rule1, rule2]

rule_engine_core = RuleEngineCore(rules)
rule_engine_core.working_memory.add_fact('age', 20)
rule_engine_core.execute()

print(rule_engine_core.working_memory.facts['is_eligible'])  # Output: True
print(rule_engine_core.working_memory.facts['discount'])  # Output: 0.1
