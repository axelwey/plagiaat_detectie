# 📄 Plagiaat Detectie – Python Project

Dit project voert automatische **plagiaatdetectie** uit op Python-bestanden van meerdere studenten.  
De vergelijking gebeurt op verschillende niveaus (raw code, CST, AST, comments en spelfouten), waardoor zowel letterlijke als structurele gelijkenissen worden gedetecteerd.

---


## 🚀 Hoe werkt het programma?

Het script **app.py** vergelijkt alle Python-bestanden in de submappen van de directory `studenten/`.  
Elke studentmap moet exact 1 `.py`-bestand bevatten.

Het project gebruikt deze libraries:

- **ast** → Abstract Syntax Tree analyse  
- **libcst** → Concrete Syntax Tree (code zonder comments, whitespace)  
- **pyspellchecker** → Spelfoutvergelijking  
- **jinja2** → HTML output via template  

---

## 🧠 Detectiemethoden

De vergelijking tussen studenten gebeurt op meerdere niveaus:

### **1. Identieke bestanden**
Controle of twee `.py`-files exact dezelfde raw inhoud hebben.

