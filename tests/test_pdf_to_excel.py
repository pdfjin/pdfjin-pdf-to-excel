import pytest
from pathlib import Path
import pikepdf
from pdfjin_pdf_to_excel.core import convert_pdf_to_excel


def test_pdf_to_excel(tmp_path: Path):
    pdf_path = tmp_path / "test.pdf"
    excel_path = tmp_path / "test.xlsx"

    pdf = pikepdf.new()
    pdf.add_blank_page()
    pdf.save(str(pdf_path))

    res = convert_pdf_to_excel(pdf_path, output_excel=excel_path)
    assert res == excel_path
    assert excel_path.exists()
