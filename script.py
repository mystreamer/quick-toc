# #!/usr/bin/env python3
# coding: utf-8

import openai
from pikepdf import Pdf, OutlineItem

def add_outline():
    pdf = Pdf.open("test/input/book1.pdf")
    
    with pdf.open_outline() as outline:
        outline.root.extend([
            OutlineItem("Section 1", 0),
            OutlineItem("Section 2", 5),
            ])

    pdf.save("test/output/book1_outlined.pdf")


if __name__ == "__main__":
    add_outline()
    print("Outline added!")

