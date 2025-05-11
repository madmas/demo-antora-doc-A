import re
import sys

def parse_uml_to_asciidoc(uml_file_path, output_file_path):
    with open(uml_file_path, 'r') as file:
        uml_content = file.read()

    classes = re.findall(r"class\s+(\w+)\s*\{(?:\s*/' adoc ([^\n]*) '/)?([\s\S]*?)\}", uml_content)
    relations = re.findall(r'(\w+)(?:\s*"([^"]*)"\s*)?\s*(<\|--|\*--|o--|--)(?:\s*"([^"]*)"\s*)?\s*(\w+)(?:\s*/\' adoc-relation (.*?) \'/)?', uml_content)

    with open(output_file_path, 'w') as file:
        for class_name, class_comment, class_body in classes:
            file.write(f"== {class_name}\n")
            if class_comment:
                file.write(f"\n{class_comment}\n\n")
            properties = re.findall(r'([+-]) (\w+): (\w+)(?: /\' adoc-property (.*?) \'/)?', class_body or '')
            methods = re.findall(r'([+-]) (\w+)\(\)(?: : (\w+))?(?: /\' adoc-method (.*?) \'/)?', class_body or '')

            if properties:
                file.write("=== Eigenschaften\n\n")
                file.write("[stripes=odd,options=header]\n")
                file.write("|===\n| *Sichtbarkeit* | *Name* | *Typ* | *Beschreibung*\n")
                for visibility, name, type_, description in properties:
                    visibility_word = "öffentlich" if visibility == "+" else "privat"
                    file.write(f"| {visibility_word}\n| {name}\n| {type_}\n| {description or ''}\n\n")
                file.write("|===\n\n")

            if methods:
                file.write("=== Methoden\n\n")
                file.write("[stripes=odd,options=header]\n")
                file.write("|===\n| *Sichtbarkeit* | *Name* | *Rückgabetyp* | *Beschreibung*\n")
                for visibility, name, return_type, description in methods:
                    visibility_word = "öffentlich" if visibility == "+" else "privat"
                    file.write(f"| {visibility_word}\n| {name}\n| {return_type or ''}\n| {description or ''}\n\n")
                file.write("|===\n\n")

            class_relations = [rel for rel in relations if class_name == rel[0] or class_name == rel[4]]
            if class_relations:
                file.write("=== Beziehungen\n\n")
                file.write("[stripes=odd,options=header]\n")
                file.write("|===\n| *Von* | *Kardinalität* | *Typ* | *Kardinalität* | *Zu* | *Beschreibung*\n")
                for from_class, from_card, rel_type, to_card, to_class, description in class_relations:
                    rel_type_word = {
                        "--": "Assoziation",
                        "<|--": "Vererbung",
                        "*--": "Komposition",
                        "o--": "Aggregation"
                    }.get(rel_type, rel_type)
                    file.write(f"| {from_class}\n| {from_card or ''}\n| {rel_type_word}\n| {to_card or ''}\n| {to_class}\n| {description or ''}\n\n")
                file.write("|===\n\n")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        parse_uml_to_asciidoc(sys.argv[1], sys.argv[2])
    else:
        parse_uml_to_asciidoc('webshop.puml', 'documentation.adoc')
