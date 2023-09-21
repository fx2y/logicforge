import heapq


class Agenda:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule, priority):
        heapq.heappush(self.rules, (priority, rule))

    def remove_rule(self, rule):
        self.rules = [(p, r) for p, r in self.rules if r != rule]
        heapq.heapify(self.rules)

    def update_rule(self, rule, priority):
        self.remove_rule(rule)
        self.add_rule(rule, priority)

    def get_next_rule(self):
        if self.rules:
            return heapq.heappop(self.rules)[1]
        else:
            return None
