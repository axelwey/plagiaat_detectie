from pathlib import Path
pad=input("Geef het path dat ik moet doorzoeken?\n>")
pad=Path(pad)
print(f"bestaat: {pad.exists()}")
if pad.is_dir():
    for bestand in pad.iterdir():
        if bestand.suffix==".py":
            print(bestand)