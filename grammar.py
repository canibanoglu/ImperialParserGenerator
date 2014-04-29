class NonTerminal(object):
    def __init__(self, grammar, name):
        self.name = name
        self.grammar = grammar
        self.production = None
        self.appears_in = list()

    def __repr__(self):
        return '<NonTerminal "%s">' % self.name

    def first(self, caller=None):
        first_set = set()
        for sp in self.production.sub_productions:
            for nt in sp:
                if nt == self:
                    continue
                elif isinstance(nt, Terminal) or not nt.production.has_epsilon_move:
                    first_set.update(nt.first())
                    break
                elif nt.production.has_epsilon_move:
                    continue
                else:
                    first_set.update(nt.first())
                    continue
        if self.production.has_epsilon_move:
            first_set.add('eps')
        return first_set

class Terminal(object):
    def __init__(self, grammar, name):
        self.name = name
        self.grammar = grammar

    def __repr__(self):
        return '<Terminal "%s">' % self.name

    def first(self):
        return set([self])

class Production(object):
    def __init__(self, grammar, t, has_epsilon):
        self.grammar = grammar
        self.non_terminal = t[0]
        self.sub_productions = t[1:]
        self.has_epsilon_move = has_epsilon

    def __repr__(self):
        j = list()
        j.extend([self.non_terminal.name, '->'])
        for sp in self.sub_productions:
            for item in sp:
                j.append(item.name)
            j.append('|')
        j.pop()
        return ' '.join(j)


class Grammar(object):
    def __init__(self, prodList):
        self._str_productions = prodList
        self._str_non_terminals = set()
        self._str_terminals = set()
        self.non_terminals = dict()
        self.terminals = dict()
        self.productions = list()
        self.__create_objects()
        self.__productions()

    def __extract_symbols(self):
        rhs_stuff = set()
        for production in self._str_productions:
            lhs = production.split('->')[0].strip()
            if lhs != lhs.upper():
                raise Exception("All non-terminals must be uppercase")
            self._str_non_terminals.add(lhs)
        for production in self._str_productions:
            rhs = production.split('->')[1].strip()
            rhs_elements = set(rhs.split())
            rhs_stuff.update(rhs_elements)
        rhs_stuff.discard('|')
        rhs_stuff -= self._str_non_terminals
        self._str_terminals = rhs_stuff

    def __create_objects(self):
        self.__extract_symbols()
        for t in self._str_terminals:
            obj = Terminal(self, t)
            self.terminals[t] = obj
        for nt in self._str_non_terminals:
            obj = NonTerminal(self, nt)
            self.non_terminals[nt] = obj

    def __productions(self):
        for p in self._str_productions:
            production = []
            has_epsilon = False
            lhs, rhs = p.split('->')
            production.append(self.non_terminals[lhs.strip()])
            for sp in rhs.strip().split('|'):
                sub_production = []
                for item in sp.split():
                    if item in self.non_terminals:
                        # This is a non-terminal
                        sub_production.append(self.non_terminals[item.strip()])
                    else:
                        # This is a terminal
                        sub_production.append(self.terminals[item.strip()])
                        if item.strip() == 'eps':
                            has_epsilon = True
                production.append(tuple(sub_production))
            P = Production(self, tuple(production), has_epsilon)
            self.productions.append(P)
            for item in P.sub_productions:
                if isinstance(item, NonTerminal):
                    item.appears_in.append(P)
            self.non_terminals[lhs.strip()].production = P

    @property
    def left_recursive(self):
        overall_bool = False
        def __recursion_check(obj, new_obj=None, last_obj=None):
            nonlocal overall_bool
            nonlocal checked
            new_obj = new_obj or obj
            if isinstance(new_obj, Terminal):
                overall_bool = overall_bool or False
                return
            else:
                p = self.non_terminals[new_obj.name].production
                for sp in p.sub_productions:
                    if sp[0] == obj:
                        overall_bool = overall_bool or True
                        return
                    elif isinstance(new_obj, Terminal) or isinstance(sp[0], Terminal):
                        continue
                    else:
                        new_obj = sp[0]
                        if sp in checked[new_obj]:
                            continue
                        else:
                            checked[new_obj].append(sp)
                            __recursion_check(obj, new_obj, last_obj)
        for nt in self.non_terminals.values():
            checked = {nt:[] for nt in self.non_terminals.values()}
            __recursion_check(nt)
        return overall_bool

