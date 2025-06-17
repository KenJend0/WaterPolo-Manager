import os

IGNORED_DIRS = {"venv", "__pycache__", ".git"}

output = []

for root, dirs, files in os.walk("."):
    # Supprimer les dossiers ignorés de la recherche
    dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("def "):
                        output.append(f"{path}: {line.strip()}")

with open("fonctions.txt", "w", encoding="utf-8") as f:
    for line in output:
        f.write(line + "\n")

print(f"✅ Fonctions extraites dans fonctions.txt ({len(output)} lignes)")
