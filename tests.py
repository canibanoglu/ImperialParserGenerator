from grammar import *
import pytest, unittest


prod1 = "E -> T E'"
prod2 = "E' -> + T E' | eps"
prod3 = "T -> F T'"
prod4 = "T' -> * F T' | eps"
prod5 = "F -> ( E ) | id"

test_grammar = Grammar([prod1, prod2, prod3, prod4, prod5])

class GrammarTest(unittest.TestCase):
    def test_extract_symbols(self):
        non_terminals = set(["E", "E'", "T", "T'", "F"])
        terminals = set(['+', 'eps', '*', '(', ')', 'id'])

        assert test_grammar._str_non_terminals == non_terminals
        assert test_grammar._str_terminals == terminals

    def test_productions(self):
        #print test_grammar.productions
        #print test_grammar.left_recursive
        pass

    def test_left_recursive(self):
        prod1 = "S -> S a | b"
        G = Grammar([prod1])
        assert G.left_recursive == True
        prod1 = "S -> A a | b"
        prod2 = "A -> S c"
        G = Grammar([prod1, prod2])
        assert G.left_recursive == True
        assert test_grammar.left_recursive == False
        prod1 = "E -> E + T | T"
        prod2 = "T -> T * F | F"
        prod3 = "F -> ( E ) | id"
        G = Grammar([prod1, prod2, prod3])
        assert G.left_recursive == True
        prod1 = "S -> A"
        prod2 = "A -> B | C"
        prod3 = "B -> ( C )"
        prod4 = "C -> B + C | D"
        prod5 = "D -> 1 | 0"
        base_list = [prod1, prod2, prod3, prod4, prod5]
        G = Grammar(base_list)
        assert G.left_recursive == False

    def test_first(self):
        for nt in test_grammar.non_terminals.values():
            print(nt)
            print(nt.first())
        print('\n\n')
        prod1 = "S -> A ( S ) B"
        prod2 = "A -> S | S B | x"
        prod3 = "B -> S B | y"
        G = Grammar([prod1, prod2, prod3])
        for nt in G.non_terminals.values():
            print(nt, nt.first())
        print(G.non_terminals)
        print(G.productions)
        print(G.left_recursive)

if __name__ == "__main__":
    unittest.main()
