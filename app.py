#dict[str, dict[str, list[str]]]
from jinja2 import Environment,FileSystemLoader
from pathlib import Path
import ast
from spellchecker import SpellChecker
import libcst
from libcst import RemoveFromParent

pad=input("Geef het path dat ik moet doorzoeken?\n>")
pad=Path(pad)
spell=SpellChecker()
if not pad.exists():
    print("pad bestaat niet.")
    exit()
if not pad.is_dir():
    print("pad moet een dir zijn.")
    exit()

studenten_mappen=[d for d in pad.iterdir() if d.is_dir()]
if not studenten_mappen:
    print("geen data in map gevonden.")
    exit()
student_files={}
for d in studenten_mappen:
    py_files=list(d.glob("*.py"))
    student_files[d.name]=py_files

students = sorted(student_files.keys(), key=lambda x: int(x[1:]))
comments={a1: {a2: [] for a2 in students if a2!=a1} for a1 in students}

class GetComment(libcst.CSTVisitor):
    def __init__(self):
        self.totaal=[]
    def visit_Comment(self, node):
        self.totaal.append(node.value.strip())
def get_comments(content):
    module=libcst.parse_module(content)
    visitor=GetComment()
    module.visit(visitor)
    return visitor.totaal

class LexiconCollector(libcst.CSTVisitor):
    def __init__(self):
        self.words= set()
    def visit_Name(self, node):
        text=node.value
        for piece in text.replace("_"," ").split():
            cleaned="".join(ch for ch in piece if ch.isalpha())
            if cleaned:
                self.words.add(cleaned.lower())
    def visit_SimpleString(self, node):
        raw=node.value
        try:
            real_string = ast.literal_eval(raw)
        except Exception:
            real_string=raw
        for piece in real_string.split():
            cleaned= "".join(ch for ch in piece if ch.isalpha())
            if cleaned:
                self.words.add(cleaned.lower())

def get_misspelled_words(content):
    module = libcst.parse_module(content)
    visitor=LexiconCollector()
    module.visit(visitor)
    words=visitor.words
    misspelled=spell.unknown(words)
    return misspelled

class CSTTranformer(libcst.CSTTransformer):
    def leave_Comment(self, original_node, updated_node):
        return RemoveFromParent()
    def leave_EmptyLine(self, original_node, updated_node):
        return RemoveFromParent()

    def leave_TrailingWhitespace(self, original_node, updated_node):
        return updated_node.with_changes(whitespace=libcst.SimpleWhitespace(""))
def get_without_comments(content):
    module = libcst.parse_module(content)
    transformer=CSTTranformer()
    new_tree = module.visit(transformer)
    return new_tree

            
for i,s1 in enumerate(students):
    files1=student_files[s1]
    # if len(files1)!=1:
    #     for s2 in students[i+1:]:
    #         comments[s1][s2].append("foutieve bestandsstructuur")
    #     continue
    for s2 in students[i+1:]:
        files2=student_files[s2]
        if len(files1)!=len(files2):
            comments[s1][s2].append("Niet evenveel files")
            continue
        for idx in range(len(files1)):
            f1 = files1[idx]
            f2 = files2[idx]
            content1 = f1.read_text(encoding="utf-8")
            content2 = f2.read_text(encoding="utf-8")
            if content1==content2:
                comments[s1][s2].append("identieke file")
            else:
                comments_1=get_comments(content1)
                comments_2=get_comments(content2)
                without_comments_1=get_without_comments(content1)
                without_comments_2=get_without_comments(content2)
                if without_comments_1.deep_equals(without_comments_2):
                    comments[s1][s2].append(f"identieke file zonder comments")
                else:
                    for com in comments_1:
                        if com in comments_2:
                            comments[s1][s2].append(f"identieke comment: '{com}'")
                    misspelled_1=get_misspelled_words(content1)
                    misspelled_2=get_misspelled_words(content2)
                    common_misspelled= misspelled_1 & misspelled_2
                    for word in common_misspelled:
                        comments[s1][s2].append(f"gemeenschappelijke spelfout: '{word}'")
            


env = Environment(loader=FileSystemLoader("."))
template=env.get_template("template.html")
html_output=template.render(students=students,comments=comments,student_files=student_files)
with open("output.html","w",encoding="utf-8") as b:
    b.write(html_output)
