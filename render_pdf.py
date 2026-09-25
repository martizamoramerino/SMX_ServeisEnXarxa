import fitz, sys
path = sys.argv[1]
outdir = sys.argv[2]
doc = fitz.open(path)
mat = fitz.Matrix(2.0, 2.0)
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=mat)
    pix.save(f"{outdir}/page_{i+1:02d}.png")
print("rendered", len(doc))
