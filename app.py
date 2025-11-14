#dict[str, dict[str, list[str]]]
from jinja2 import Environment,FileSystemLoader
from pathlib import Path
import re 

pad=input("Geef het path dat ik moet doorzoeken?\n>")
pad=Path(pad)
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

students=list(student_files.keys())
comments={a1: {a2: [] for a2 in students if a2!=a1} for a1 in students}

for i,s1 in enumerate(students):
    files1=student_files[s1]
    if len(files1)!=1:
        for s2 in students[i+1:]:
            comments[s1][s2].append("foutieve bestandsstructuur")
        continue
    content1=files1[0].read_text(encoding="utf-8")
    for s2 in students[i+1:]:
        files2=student_files[s2]
        if len(files2)!=1:
            comments[s1][s2].append("foutieve bestandsstructuur")
            continue
        content2=files2[0].read_text(encoding="utf-8")
        if content1==content2:
            comments[s1][s2].append("identieke file")
        else:
            comments_file1=[c.strip() for c in re.findall(r"#\s*.*",content1)]
            comments_file2=[c.strip() for c in re.findall(r"#\s*.*",content2)]
            for com in comments_file1:
                if com in comments_file2:
                    comments[s1][s2].append(f"identieke comment: '{com}'")


env = Environment(loader=FileSystemLoader("."))
template=env.get_template("template.html")
html_output=template.render(students=students,comments=comments)
with open("output.html","w",encoding="utf-8") as b:
    b.write(html_output)
