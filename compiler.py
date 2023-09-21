from rule_engine import Rule, Action, Expression


class Compiler:
    def __init__(self, ast):
        self.ast = ast

    def compile(self):
        return self.visit(self.ast)

    def visit(self, node):
        node_type = node[0]
        if node_type == 'IF':
            condition = self.visit(node[1])
            action = self.visit(node[2])
            return Rule(condition, action)
        elif node_type in ('AND', 'OR'):
            left = self.visit(node[1])
            right = self.visit(node[2])
            return Expression(node_type, left, right)
        elif node_type == 'NOT':
            expression = self.visit(node[1])
            return Expression(node_type, expression)
        elif node_type in ('>', '<', '==', '!=', '>=', '<='):
            left = self.visit(node[1])
            right = self.visit(node[2])
            return Expression(node_type, left, right)
        elif node_type == 'IDENTIFIER':
            return node[1]
        elif node_type == 'NUMBER':
            return int(node[1])
        elif node_type == 'STRING':
            return node[1]
        elif node_type == 'FUNCTION':
            function_name = node[1]
            args = [self.visit(arg) for arg in node[2]]
            return function_name, args
        elif node_type == '=':
            left = self.visit(node[1])
            right = self.visit(node[2])
            return Action(Expression(node_type, left, right))
        elif node_type in ('+=', '-=', '*=', '/='):
            left = self.visit(node[1])
            right = self.visit(node[2])
            return Action(Expression(node_type, left, right))
        else:
            raise Exception('Invalid node type')
