import re
email=input("Geef een email:")

split=re.match(r"^(?P<naam>[a-zA-Z]+)(?P<type>@[a-zA-Z]+)\.(?P<end>[a-zA-Z]{2,})$",email)
if not split:
    print("Geen geldig email-adress.")
    exit()
print(f"email: {email}\nnaam: {split.group("naam")}\ntype: {split.group("type")}\nend: {split.group("end")}")