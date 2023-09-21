class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def execute(self, facts):
        for rule in self.rules:
            rule.evaluate(facts)


class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def evaluate(self, facts):
        if self.condition.evaluate(facts):
            self.action.execute(facts)


class Condition:
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, facts):
        return self.expression.evaluate(facts)


class Action:
    def __init__(self, expression):
        self.expression = expression

    def execute(self, facts):
        self.expression.execute(facts)


class Expression:
    def __init__(self, operator, left, right=None):
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self, facts):
        if isinstance(self.left, Expression):
            left_value = self.left.evaluate(facts)
        elif isinstance(self.left, str):
            left_value = facts.get(self.left)
            if left_value is None:
                left_value = self.left
        else:
            left_value = self.left

        if isinstance(self.right, Expression):
            right_value = self.right.evaluate(facts)
        elif isinstance(self.right, str):
            right_value = facts.get(self.right)
            if right_value is None:
                right_value = self.right
        else:
            right_value = self.right

        if self.operator == 'AND':
            return left_value and right_value
        elif self.operator == 'OR':
            return left_value or right_value
        elif self.operator == 'NOT':
            return not left_value
        elif self.operator == '>':
            return left_value > right_value
        elif self.operator == '<':
            return left_value < right_value
        elif self.operator == '==':
            return left_value == right_value
        elif self.operator == '!=':
            return left_value != right_value
        elif self.operator == '>=':
            return left_value >= right_value
        elif self.operator == '<=':
            return left_value <= right_value
        else:
            raise Exception('Invalid operator')

    def execute(self, facts):
        if isinstance(self.right, Expression):
            right_value = self.right.evaluate(facts)
        elif isinstance(self.right, str):
            if self.right.lower() == 'true':
                right_value = True
            elif self.right.lower() == 'false':
                right_value = False
            else:
                right_value = facts.get(self.right)
                if right_value is None:
                    right_value = self.right
        else:
            right_value = self.right

        if self.operator == '=':
            facts[self.left] = right_value
        elif self.operator == '+=':
            facts[self.left] += right_value
        elif self.operator == '-=':
            facts[self.left] -= right_value
        elif self.operator == '*=':
            facts[self.left] *= right_value
        elif self.operator == '/=':
            facts[self.left] /= right_value
        else:
            raise Exception('Invalid operator')
