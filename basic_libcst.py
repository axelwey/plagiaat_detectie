import libcst as cst

expressie="1 + 2 / 4 + 7 * 3"
source_tree = cst.parse_expression(expressie)
print(source_tree)
print(type(source_tree))



class ArithmeticVisualiser(cst.CSTVisitor):
    def __init__(self):
        self.totaal=0
    def visit_Integer(self, node):
        print(f"getal gevonden: {node.value}")
        waarde=int(node.value)
        self.totaal+=waarde

visitor=ArithmeticVisualiser()
source_tree.visit(visitor)
print(f"totaal: {visitor.totaal}")