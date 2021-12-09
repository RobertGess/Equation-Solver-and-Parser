from bool import *
from se1 import *
from pcomb import *
import z3

"""""
The first task is to implement classes for representing the combined arithmetical and boolean expressions. Feel
free to reuse code we implemented in the course.

<expr> ::= <boolean_expression> | <arithm_expression>


Next, implement parsers for the expressions, using parser combinators.
Implement two functions, one for printing, the other for evaluating the parsed expressions in an environment:
def printExpr(inp):
def evalExpr(inp, env):
"""""


"""""
<expr> ::= <boolean_expression> | <arithm_expression>

<boolean_expression> ::= <disjunct> ’or’ <boolean_expression> | <disjunct>
    <disjunct> ::= <conjunct> ’and’ <disjunct> | <conjunct>
    <conjunct> ::= <arithmetic_expression> <cmp> <arithmetic_expression> | (<boolean_expression>)
    <cmp> ::= ’=’ | ’<’

<arithm_expression> ::= <term> ’+’ <arithm_expression> | <term>
    <term> ::= <factor> ’*’ <term> | <factor>
    <factor> ::= ’(’ <arithm_expression> ’)’ | <int> | <variable>
    <int> ::= INTEGER
    <variable> ::= IDENTIFIER
"""""



def solve(expressions):
    """""
    >>> exprs = ["x + y +z = 10", "x < y", "x < 3", "0 < x"]
    >>> sol = solve(exprs)
    >>> sol                     # doctest: +SKIP
    {'y = 2', 'z = 7', 'x = 1'} # doctest: +SKIP
    >>> exprs = ["x + y +z = 10", "x < y or x = y", "x < 3", "5 < x or 0 < x"]
    >>> sol = solve(exprs)
    >>> sol                     # doctest: +SKIP
    {'z = 7', 'x = 1', 'y = 2'} # doctest: +SKIP
    """""

    s = z3.Solver()

    for expr in expressions:
        s.add(result(ParseExpr().parse(expr)).toZ3())

    s.check()
    if s.check().r == 1:
        a = s.model()
        modelset = set()
        for b in a:
            name = b
            val = a[b]
            modelset.add(f'{name} = {val}')
        return modelset
    else:
        print("No solution!")


def printExpr(inp):
    """""
    >>> printExpr("x = y")
    (x = y)
    >>> printExpr("x + 2 * y")
    (x + (2 * y))
    >>> printExpr("x < 2 and y < 1")
    ((x < 2) and (y < 1))
    >>> printExpr("(x + 2 * y < 15 + x * x) or z = 5")
    (((x + (2 * y)) < (15 + (x * x))) or (z = 5))
    >>> printExpr("x + 2 * y < 15 + x * x or z = 5")
    (((x + (2 * y)) < (15 + (x * x))) or (z = 5))
    """""
    res = ParseExpr().parse(inp)
    print(result(res))


def evalExpr(inp, env):
    """""
    >>> env = {'x': 1, 'y': 2, 'z': 3}
    >>> evalExpr("x = y", env)
    False
    >>> evalExpr("x + 2 * y", env)
    5
    >>> evalExpr("x < 2 and y < 1", env)
    False
    >>> evalExpr("(x + 2*y < 15 + x * x) or z = 5", env)
    True
    >>> evalExpr("x + 2*y < 15 + x * x or z = 5", env)
    True
    >>> evalExpr("x * 2 + 3 < x * (2 + 3)", env)
    False
    >>> evalExpr("y * 2 + 3 < y * (2 + 3)", env)
    True
    """""
    res = ParseExpr().parse(inp)
    a = type(res[0][0].toZ3())
    print(result(res).ev(env))


    # pytest --doctest-modules PStA.py



# pytest --doctest-modules PStA.py


if __name__ == "__main__":
    env = {'x': 1, 'y': 2, 'z': 3}

    # s = z3.Solver()
    # s.add(z3.Int("x") == z3.Int("y"))
    # b = Less(Plus(Var("x"), Con(1)), Var("y")).toZ3()
    # c = result(ParseExpr().parse("(((2+2)*3)+2+x = 5 and 2 < 5) or 0 < x")).toZ3()
    # d = 0
    # # c = b.toZ3()
    # # e = 0
    # # s.add(b)
    # # g = z3.And(5 == 5, z3.Int("x") == 2)
    # s.add(c)
    # print(s.check())
    # print(s.model())

    # evalExpr("  (((2+2)*3)+2 = 5 and 4 < 5) or 1 < 2 ", {})
    # print(result(ParseExpr().parse("2+2")))
    # print(result(ParseEqual().parse("x*x = 2+y+exp(e*2)")))
    # print(result(ParseEqual().parse("x = 3*2" and "x = 2")))

    # a, b = z3.Reals("a b")
    # s.add([a == 2.1, b >= a])
    #
    # print(s.check(), s.model())

    # evalExpr("14 < x and 3 * 1 = 3 + 0 * 2", {'x': 15})
    # printExpr("14 < x and 3 * 1 = 3 + 0 * 2")
    # evalExpr("exp(x)", {'x': 5})


    # exprs = ["x + y + z = 10", "x < y", "x < 3", "0 < x", "1<0"]
    exprs = ["x + y +z = 10", "x < y or x = y", "x < 3", "5 < x or 0 < x"]
    sol = solve(exprs)
    print(sol)


