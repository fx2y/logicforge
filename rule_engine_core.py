from agenda import Agenda


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
        self.agenda = Agenda()

    def execute(self):
        for rule in self.rules:
            self.agenda.add_rule(rule, rule.priority)

        while True:
            rule = self.agenda.get_next_rule()
            if rule is None:
                break
            if rule.evaluate(self.working_memory.facts):
                rule.execute(self.working_memory.facts)
                for r in self.rules:
                    if r != rule and r.evaluate(self.working_memory.facts):
                        self.agenda.update_rule(r, r.priority)
