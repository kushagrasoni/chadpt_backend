# utils.py
from typing import Set

import pandas as pd
import io


def read_csv_and_infer_types(file_content: bytes) -> dict:
    df = pd.read_csv(io.StringIO(file_content.decode("utf-8")))
    column_data_types = df.dtypes.to_dict()
    return column_data_types


def create_table_sql(database, table, column_data_types) -> Set[str]:

    # Generate CREATE TABLE SQL statement based on inferred column data types
    table_creation_sql = f"CREATE TABLE {database}.{table} (\n"
    for column_name, data_type in column_data_types.items():
        table_creation_sql += f"    {column_name} {data_type},\n"
    table_creation_sql = table_creation_sql.rstrip(",\n") + "\n);"

    return {table_creation_sql}