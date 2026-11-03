import sys
import argparse
from pathlib import Path
try:
    from .core import convert_pdf_to_excel
    from . import __version__
except (ImportError, ValueError):
    from pdfjin_pdf_to_excel.core import convert_pdf_to_excel
    from pdfjin_pdf_to_excel import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="pdfjin-pdf-to-excel",
        description="Extract tables from PDF files into Microsoft Excel (.xlsx).",
        epilog="Online web version available at https://pdfjin.com/pages/pdf-to-excel.html",
    )
    parser.add_argument("input", metavar="INPUT_PDF", help="Path to the PDF file")
    parser.add_argument("-o", "--output", required=True, metavar="OUTPUT_XLSX", help="Path for output .xlsx file")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    try:
        out = convert_pdf_to_excel(args.input, output_excel=args.output)
        print(f"📊 Successfully extracted tables to Excel -> {out}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
