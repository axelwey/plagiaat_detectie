import libcst as cst

expressie_1="1 + 2 / 4 + 7 * 3"
expressie_2="(1 + 2) * 4 + 9 + 7 * (2 + 1)"
expressie_1_tree = cst.parse_expression(expressie_1)
expressie_2_tree= cst.parse_expression(expressie_2)
print(f"expressie 1 :{expressie_1_tree}")
print(type(expressie_1_tree))
print(f"expressie 2 :{expressie_2_tree}")
print(type(expressie_2_tree))



class  MultiplicationOperandVisualizer(cst.CSTVisitor):
    def __init__(self):
        self.mul_depth=0
        self.totaal=[]
    def visit_Integer(self, node):
        if self.mul_depth>0:
            print(f"getal gevonden: {node.value}")
            waarde=int(node.value)
            self.totaal.append(waarde)
    def visit_BinaryOperation(self, node):
        if isinstance(node.operator, cst.Multiply):
            self.mul_depth +=1
    def leave_BinaryOperation(self, node):
        if isinstance(node.operator,cst.Multiply):
            self.mul_depth-=1

visitor= MultiplicationOperandVisualizer()
visitor2=MultiplicationOperandVisualizer()
expressie_1_tree.visit(visitor)
expressie_2_tree.visit(visitor2)
print(f"totaal expressie 1: {visitor.totaal}")
print(f"totaal expressie 2: {visitor2.totaal}")