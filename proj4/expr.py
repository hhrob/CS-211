

class Expr():
    """Abstract base class of all expressions."""
    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError(
            f"'eval' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define 'eval'")
    
    def __str__(self) -> str:
        """Implementations of __str__ should return the expression
        in algebraic notation"""
        raise NotImplementedError(
            f"'__str__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__str__'")
    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that
        looks like the constructor,
        e.g., Plus(IntConst(5), IntConst(4))
        """
        raise NotImplementedError(
            f"'__repr__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__repr__'")
    
class IntConst(Expr):
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: Expr):
        return isinstance(other, IntConst) and self.value == other.value
    
    def eval(self) -> "IntConst":
        return IntConst(self.value)
    
    def __str__(self):
        return f"{self.value}"
    
    def __repr__(self):
        return f"IntConst({self.value})"
    
class BinOp(Expr):
    """Abstract base class for binary operations"""
    def __init__(self, left: Expr, right: Expr, \
                 symbol: str="?Operation symbol undefined"):
        self.left = left
        self.right = right
        self.symbol = symbol

    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(self._apply(left_val.value, right_val.value))
    
    def _apply(self, left_val: int, right_val: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(
        f"'_apply' not implemented in {self.__class__.__name__}\n"
        "Each concrete BinOp class must define '_apply'")
    
    def __str__(self):
        return f"({self.left} {self.symbol} {self.right})"
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.left.__repr__()}, {self.right.__repr__()})"
    

class Plus(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right, symbol="+")

    def _apply(self, left, right):
        return left + right
    

class Times(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right, symbol="*")

    def _apply(self, left, right):
        return left * right
    
    
    def __str__(self):
        return super.__str__()
    
    def __repr__(self):
        return super.__repr__()
    
class Minus(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right, symbol="-")

    def _apply(self, left, right):
        return left - right
    
    
class Div(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right, symbol="/")

    def _apply(self, left, right):
        return left / right
    
class UnOp(Expr):
    def __init__(self, left, symbol: str="?Operation symbol"):
        self.left = left
        self.symbol = symbol

    def _apply(self, left):
        raise NotImplementedError("Apply not implemented for abstract class")

    def eval(self):
        left_val = self.left.eval()
        return IntConst(self._apply(left_val.value))

    def __str__(self):
        return f"({self.symbol} {self.left})"

    def __repr__(self):
        return f"{self.__class__.__name__}(IntConst({self.left}))"

class Neg(UnOp):
    def __init__(self, left):
        super().__init__(left,symbol="~")

    def _apply(self, left):
        return left * -1



class Abs(UnOp):
    def __init__(self, left):
        super().__init__(left, symbol="@")

    def _apply(self, left):
        if left > 0:
            return left
        else:
            return left * -1

ENV = {}

class Var(Expr):
    def __init__(self, name: str):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"Var({self.name})"
    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been \
            assigned a value")

    def assign(self, value):
        global ENV
        ENV[self.name] = value

class UndefinedVariable(Exception):
    "Raised when expression tries to use a variable that is not in ENV"
    pass

class Assign(Expr):
    """Assignment: x = E represented as Assign(x, E)"""
    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var) # Can only assign to variables!
        self.left = left
        self.right = right

    def eval(self) -> IntConst:
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val

    def __str__(self):
        return f"({self.left} = {self.right})"

    def __repr__(self):
        return f"Assign({self.left.__repr__()}, {self.right.__repr__()})"

    




    
    
    

    

    