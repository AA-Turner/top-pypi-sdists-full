import pymupdf

pymupdf.TOOLS.set_aa_level(0)

def analyze_pdf(path):
    doc = pymupdf.open(path)
    results = []
    for i, page in enumerate(doc):
        pix=page.get_pixmap(colorspace=pymupdf.csGRAY)
        bw = pix.is_monochrome
        print(bw)

        results.append(bw)
        label = "black & white" if bw==0 else "has color"
        print(f"Page {i + 1}/{len(doc)}: {label}")

    doc.close()
    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_bw_pages.py <file.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    analyze_pdf(pdf_path)
