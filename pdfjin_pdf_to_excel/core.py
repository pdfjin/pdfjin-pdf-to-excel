import io
from pathlib import Path
from typing import Union, BinaryIO, Optional
import pdfplumber
import pandas as pd


def convert_pdf_to_excel(
    input_pdf: Union[str, Path, bytes, BinaryIO],
    output_excel: Optional[Union[str, Path]] = None,
) -> Union[bytes, Path]:
    """
    Extract tables from a PDF document and export into Excel worksheets.
    """
    if isinstance(input_pdf, (str, Path)):
        pdf_stream = open(input_pdf, "rb")
    elif isinstance(input_pdf, bytes):
        pdf_stream = io.BytesIO(input_pdf)
    else:
        pdf_stream = input_pdf

    all_tables = []
    with pdfplumber.open(pdf_stream) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table_idx, raw_table in enumerate(tables):
                if not raw_table:
                    continue
                df = pd.DataFrame(raw_table)
                sheet_name = f"Page{i+1}_Table{table_idx+1}"[:31]
                all_tables.append((sheet_name, df))

    if not all_tables:
        # Fallback: create empty table if no explicit table lines found
        all_tables.append(("Extracted", pd.DataFrame([["No structured tables detected"]])))

    output_io = io.BytesIO()
    with pd.ExcelWriter(output_io, engine="openpyxl") as writer:
        for sheet_name, df in all_tables:
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

    excel_bytes = output_io.getvalue()

    if output_excel is None:
        return excel_bytes

    out_path = Path(output_excel)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(excel_bytes)
    return out_path
