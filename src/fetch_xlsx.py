import pandas as pd

from sqlalchemy.orm import Session

from .crud import create_swift_code

def parse_and_load_xlsx(db: Session, xlsx_path: str) -> None:
    """
    Function to parse and load an XLSX file into a database.
    """
    df = pd.read_excel(xlsx_path, engine="openpyxl")

    for _, row in df.iterrows():
        data_dict = {
            "swift_code": row["SWIFT CODE"],
            "bank_name": row["NAME"],
            "address": row["ADDRESS"],
            "country_iso2": str(row["COUNTRY ISO2 CODE"]).upper(),
            "country_name": str(row["COUNTRY NAME"]).upper(),
            "is_headquarter": row["SWIFT CODE"].endswith("XXX")
        }
        create_swift_code(db, data_dict)

    print("Załadowano dane z XLSX do bazy")