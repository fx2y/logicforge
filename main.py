from dsl import DSL

rule_dsl = 'IF age > 18 AND gender == "male" THEN is_eligible = true'
dsl = DSL(rule_dsl)
facts = {'age': 20, 'gender': 'male', 'is_eligible': False}
dsl.execute(facts)
print(facts['is_eligible'])  # Output: True
