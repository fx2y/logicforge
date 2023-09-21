class WorkingMemory:
    def __init__(self, facts):
        self.facts = facts

    def add_fact(self, name, value):
        self.facts[name] = value

    def remove_fact(self, name):
        del self.facts[name]

    def update_fact(self, name, value):
        self.facts[name] = value


class RuleEngineCore:
    def __init__(self, rules):
        self.rules = rules
        self.working_memory = WorkingMemory({})

    def execute(self):
        while True:
            fired = False
            for rule in self.rules:
                if rule.evaluate(self.working_memory.facts):
                    rule.execute(self.working_memory.facts)
                    fired = True
            if not fired:
                break
