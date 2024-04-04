from expr import *

def calc(text: str):

    try:
         stack = rpn_parse(text)
         if len(stack) == 0:
              print("Must provide expression")
         else:
              for exp in stack:
                   print(f"{exp} => {exp.eval()}")

    except Exception:
         pass
    
def rpn_calc():
    text = input("Expression (return to exit):")
    while len(text.strip()) > 0:
          text = input("Expression (return to exit):")
    print("Bye! Thanks for the math!")

def rpn_parse(text: str):
     stack = []
     s = text.split()

     for i in s:
        if i.isnumeric:
               stack.append(IntConst(int(i)))
        elif is_binop(i):
            right = stack.pop()
            left = stack.pop()
            oper = binop_class(i)
            stack.append(oper, left, right)

        elif is_unop(i):
             left = stack.pop()
             oper = unop_class(i)
             stack.append(oper(left))

        elif is_var(i):
             stack.append(Var(i))

        elif i == "=":
             right = stack.pop()
             left = stack.pop()
             stack.append(left, right)

def is_binop(op):
     operators = ["*", "+", "-", "/"]
     return op in operators

def is_unop(op):
     operators = ["~", "@"]
     return op in operators

def is_var(op):
     return op.isalpha()

def binop_class(op):
     binop = {"+" : Plus, "-": Minus, "/": Div, "*": Times}
     return binop[op]

def unop_class(op):
     unop = {"@": Abs, "~": Neg}
     return unop[op]



rpn_calc()   