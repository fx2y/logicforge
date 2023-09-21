from compiler import Compiler
from rule_engine import RuleEngine
from rule_parser import Lexer, Parser


class DSL:
    def __init__(self, rule_dsl):
        self.rule_dsl = rule_dsl

    def execute(self, facts):
        lexer = Lexer(self.rule_dsl)
        lexer.tokenize()
        parser = Parser(lexer.tokens)
        ast = parser.parse()
        compiler = Compiler(ast)
        rules = [compiler.compile()]
        rule_engine = RuleEngine(rules)
        rule_engine.execute(facts)
