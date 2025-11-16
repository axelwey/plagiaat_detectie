import ast
#ast.parse
#ast.dump
#ast.NodeVisitor

data="""# Deze comments zijn weer anders
# Maar de code is verder identiek

title = "Hello world"  # andere spaties
value = 5  # andere spacing

def calculate_total(n):  # comment
    return n + value  # andere comment
"""
ast_data=ast.parse(data)
data_omvorm=ast.unparse(ast_data)
print(data_omvorm)
