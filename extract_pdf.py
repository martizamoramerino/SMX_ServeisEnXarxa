import pypdf, sys
path = sys.argv[1]
out = sys.argv[2]
r = pypdf.PdfReader(path)
with open(out, "w", encoding="utf-8") as f:
    for i, page in enumerate(r.pages):
        f.write(f"\n=== PAGE {i+1} ===\n")
        f.write(page.extract_text() or "")
print("pages:", len(r.pages))
