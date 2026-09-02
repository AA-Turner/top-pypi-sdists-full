"""
┏┓┓ ┏┓┏┓┏┓┳┓┳┓┏┓┳┓ 
┣┫┃ ┣┫┃ ┃┃┣┫┃┃┣ ┣┫ 
┛┗┗┛┛┗┗┛┗┛┛┗┻┛┗┛┛┗ 
(c) 2023 Sam Robson

Alacorder collects case detail PDFs from Alacourt.com and 
processes them into data tables suitable for research purposes.

Dependencies:   python: 3.10+
                brotli: 1.1.0+
                bs4: 0.0.1+
                docxtpl: 0.16.7+
                polars: 0.19.3+
                pymupdf: 1.22.5+
                rich: 13.5.2+
                selenium: 4.10.0+
                typer: 0.9.0+
                xlsxwriter: 3.1.2+
                xlsx2csv: 0.8.1+
                Google Chrome: v75+
"""

from .alac import app

if __name__ == "__main__":
    app()
