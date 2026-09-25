import fitz, sys
path = sys.argv[1]
out = sys.argv[2]
doc = fitz.open(path)
with open(out, "w", encoding="utf-8") as f:
    for i, page in enumerate(doc):
        f.write(f"\n=== PAGE {i+1} ===\n")
        f.write(page.get_text())
print("done")
