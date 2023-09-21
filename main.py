from rule_parser import RuleParser

rule_dsl = 'IF age > 18 AND gender == "male" THEN is_eligible = true'
rule_parser = RuleParser(rule_dsl)
rule_parser.parse()
print(rule_parser.ast)