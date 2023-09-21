from rule_parser import RuleParser

rule_dsl = "IF age > 18 AND gender = 'male' THEN is_adult = true"
rule_parser = RuleParser(rule_dsl)
rule_parser.parse()
