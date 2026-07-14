# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import io
from typing import Any, Optional

import pandas as pd

from superset.utils.core import GenericDataType


def column_number_to_letter(column_number: int) -> str:
    start_index = 0
    letter = ""
    while column_number > 25 + start_index:
        letter += chr(65 + int((column_number - start_index) / 26) - 1)
        column_number = column_number - (int((column_number - start_index) / 26)) * 26
    letter += chr(65 - start_index + (int(column_number)))
    return letter


def get_function_num(
    aggregate: Optional[str], ignore_hidden_rows: bool = True
) -> Optional[int]:
    function_num = None
    # COUNT_DISTINCT not possible for subtotal
    if aggregate == "SUM":
        function_num = 9 + (0, 100)[ignore_hidden_rows]
    elif aggregate == "AVG":
        function_num = 1 + (0, 100)[ignore_hidden_rows]
    elif aggregate == "COUNT":
        function_num = 2 + (0, 100)[ignore_hidden_rows]
    elif aggregate == "MAX":
        function_num = 4 + (0, 100)[ignore_hidden_rows]
    elif aggregate == "MIN":
        function_num = 5 + (0, 100)[ignore_hidden_rows]
    return function_num


def write_summary_formula(
    worksheet: Any, spec: dict[str, str], df: pd.DataFrame, summary_row: int
) -> None:
    aggregate = spec.get("aggregate")
    label = spec.get("label")
    column_index = df.columns.get_loc(label) + 1
    column_letter = column_number_to_letter(column_index)
    if function_num := get_function_num(aggregate, True):
        formula = (
            f"=SUBTOTAL({function_num},{column_letter}2:{column_letter}{summary_row})"
        )
        worksheet.write_formula(summary_row, column_index, formula)


def df_to_excel(
    df: pd.DataFrame,
    summary_specs: Optional[list[dict[str, str]]] = None,
    **kwargs: Any,
) -> Any:
    output = io.BytesIO()

    # pylint: disable=abstract-class-instantiated
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, **kwargs)

        if summary_specs:
            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            rows, _ = df.shape
            summary_row = rows + 1

            index_format = workbook.add_format(
                {
                    "bold": True,
                    "align": "center",
                    "valign": "top",
                    "top": 1,
                    "bottom": 1,
                    "left": 1,
                    "right": 1,
                }
            )
            worksheet.write(summary_row, 0, "Summary", index_format)
            for spec in summary_specs:
                write_summary_formula(worksheet, spec, df, summary_row)
    return output.getvalue()


def apply_column_types(
    df: pd.DataFrame, column_types: list[GenericDataType]
) -> pd.DataFrame:
    for column, column_type in zip(df.columns, column_types):
        if column_type == GenericDataType.NUMERIC:
            try:
                df[column] = pd.to_numeric(df[column])
            except ValueError:
                df[column] = df[column].astype(str)
        elif pd.api.types.is_datetime64tz_dtype(df[column]):
            # timezones are not supported
            df[column] = df[column].astype(str)
    return df
