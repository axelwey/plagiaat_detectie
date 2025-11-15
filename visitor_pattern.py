import json
import xml.etree.ElementTree as ET

class BuildingVisitor:
    def do_something_for_industrial(self, i):
        raise NotImplementedError()

    def do_something_for_residential(self, r):
        raise NotImplementedError()

class Industrial:
    def __init__(self,uitstoot):
        self.uitstoot=uitstoot
    def accept(self,visitor):
        visitor.do_something_for_industrial(self)
class Residential:
    def __init__(self,slaapkamers,oppervlakte):
        self.slaapkamers=slaapkamers
        self.oppervlakte=oppervlakte
    def accept(self,visitor):
        visitor.do_something_for_residential(self)


class XMLExportVisitor(BuildingVisitor):

    def __init__(self):
        self.root = ET.Element("Buildings")
        self.count = 0  # deze visitor telt hoeveel nodes hij bezocht

    def do_something_for_industrial(self, i):
        self.count += 1
        node = ET.SubElement(self.root, "Industrial")
        node.set("CO2", str(i.uitstoot))

    def do_something_for_residential(self, r):
        self.count += 1
        node = ET.SubElement(self.root, "Residential")
        node.set("slaapkamers", str(r.slaapkamers))
        node.set("oppervlakte", str(r.oppervlakte))
    def export(self):
        return ET.tostring(self.root, encoding='unicode')
    
class JSONExportVisitor(BuildingVisitor):

    def __init__(self):
        self.data = []

    def do_something_for_industrial(self, i):
        self.data.append({
            "type": "Industrial",
            "uitstoot": i.uitstoot
        })

    def do_something_for_residential(self, r):
        self.data.append({
            "type": "Residential",
            "slaapkamers": r.slaapkamers,
            "oppervlakte": r.oppervlakte
        })

    def export(self):
        return json.dumps(self.data, indent=4)





residential_1=Residential(slaapkamers=4,oppervlakte=40)
residential_2=Residential(slaapkamers=2,oppervlakte=40)
industrial_1=Industrial(uitstoot=50)
industrial_2=Industrial(uitstoot=100)

buildings=[residential_1,residential_2,industrial_1,industrial_2]

xml_visitor = XMLExportVisitor()
for b in buildings:
    b.accept(xml_visitor)

xml_output = xml_visitor.export()

json_visitor = JSONExportVisitor()
for b in buildings:
    b.accept(json_visitor)

json_output = json_visitor.export()

print("=== XML EXPORT ===")
print(xml_output)
print("\nAantal bezochte nodes (XML Visitor):", xml_visitor.count)

print("\n=== JSON EXPORT ===")
print(json_output)