import pandas as pd
import argparse

"""
This script reads fantasy hockey CSV summary files for forwards, defensemen, and goalies,
and generates an Excel workbook with sparklines for each stat group.

CSV file expectations:
- Each file must have columns: id, name, picked (0/1 flag), followed by stat columns.
- Stat columns are grouped as <stat_name>_<year> (e.g., GP_2022, GP_2023, ...).
- After each stat group, a placeholder column named <stat_name>_spark must exist for sparklines.
- Example column order: id, name, picked, GP_2022, GP_2023, ..., GP_spark, G_2022, ..., G_spark, ...

The script will place sparklines in the <stat_name>_spark columns, showing trends for each stat group.
"""

class ExcelDraftTables:
    def __init__(self, forward_csv_file: str, defense_csv_file: str, goalie_csv_file: str, output_file: str):
        """
        Initialize the ExcelDraftTables object.

        Args:
            forward_csv_file (str): Path to the forwards CSV file.
            defense_csv_file (str): Path to the defensemen CSV file.
            goalie_csv_file (str): Path to the goalies CSV file.
            output_file (str): Path to the output Excel workbook.
        """
        self.forward_csv_file = forward_csv_file
        self.defense_csv_file = defense_csv_file
        self.goalie_csv_file = goalie_csv_file
        self.output_file = output_file

    def execute(self):
        """
        Reads all CSV files and writes their contents to an Excel workbook,
        adding sparklines for each stat group in the appropriate columns.
        """
        # Read all dataframes first
        forward_df = self._read_csv(self.forward_csv_file)
        defense_df = self._read_csv(self.defense_csv_file)
        goalie_df = self._read_csv(self.goalie_csv_file)

        # Create the Excel workbook once, and add all sheets
        with pd.ExcelWriter(self.output_file, engine="xlsxwriter") as writer:
            self.player_sheet(forward_df, "Forwards", writer)
            self.player_sheet(defense_df, "Defense", writer)
            self.player_sheet(goalie_df, "Goalies", writer)

    def _read_csv(self, csv_file: str) -> pd.DataFrame:
        """
        Reads a CSV file into a pandas DataFrame using latin1 encoding.

        Args:
            csv_file (str): Path to the CSV file.

        Returns:
            pd.DataFrame: The loaded DataFrame.
        """
        df = pd.read_csv(csv_file, encoding='latin1')
        return df

    def player_sheet(self, df: pd.DataFrame, sheet_name: str, writer):
        """
        Writes a DataFrame to an Excel sheet and adds sparklines for each stat group.

        Args:
            df (pd.DataFrame): The DataFrame to write.
            sheet_name (str): The name of the Excel sheet.
            writer: The pandas ExcelWriter object.
        """
        stat_groups = self._determine_stat_groups(df)
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0, startcol=0)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        nrows = len(df)

        # Add sparklines for each stat group using the spark column index
        for stat_name, start_col, end_col, spark_col in stat_groups:
            for row in range(2, nrows + 2):  # Excel is 1-based + header row
                worksheet.add_sparkline(row - 1, spark_col, {
                    "range": f"{worksheet.name}!{self._excel_col(start_col)}{row}:{self._excel_col(end_col)}{row}",
                    "type": "line",
                    "markers": False,
                    "show_hidden": False  # Show sparkline even if data is hidden
                })

    def _determine_stat_groups(self, df: pd.DataFrame):
        """
        Determines stat groups in the DataFrame based on column naming pattern.

        Returns:
            list: List of tuples (stat_name, start_col_index, end_col_index, spark_col_index).
                  Each tuple describes a stat group and its sparkline column.

        Assumes columns are named as <stat_name>_<year> and <stat_name>_spark.
        """
        stat_groups = []
        columns = df.columns.tolist()
        col_idx = 3  # Skip 'id', 'name', 'picked'
        while col_idx < len(columns):
            stat_name = '_'.join(columns[col_idx].split('_')[:-1])
            start_idx = col_idx
            # Find the end of this stat group (last <stat>_<year>)
            while col_idx + 1 < len(columns) and columns[col_idx + 1].startswith(stat_name + "_") and not columns[col_idx + 1].endswith("_spark"):
                col_idx += 1
            end_idx = col_idx
            # The next column should be the sparkline column
            spark_col_idx = col_idx + 1 if (col_idx + 1 < len(columns) and columns[col_idx + 1] == f"{stat_name}_spark") else None
            if spark_col_idx is not None:
                stat_groups.append((stat_name, start_idx, end_idx, spark_col_idx))
            else:
                print(f"Warning: Sparkline column for stat '{stat_name}' not found.")
            col_idx = spark_col_idx + 1 if spark_col_idx is not None else col_idx + 1
        return stat_groups

    def _excel_col(self, idx):
        """
        Convert zero-based column index to Excel column letter(s).

        Args:
            idx (int): Zero-based column index.

        Returns:
            str: Excel column letter(s).
        """
        letters = ""
        while idx >= 0:
            letters = chr(idx % 26 + 65) + letters
            idx = idx // 26 - 1
        return letters

def parse_args():
    """
    Parses command-line arguments for league ID.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--league_id", type=str, required=True, help="League ID (_excel.csv files are expected to be in 'espn-data/<league_id>/dumps')")
    return parser.parse_args()

def main(league_id: int):
    """
    Main entry point for generating the Excel workbook.

    Args:
        league_id (int): The league ID used to locate CSV files.
    """
    src_dir = f"espn-data/{league_id}/dumps"
    forward_csv_file = f"{src_dir}/f_summary_excel.csv"
    defense_csv_file = f"{src_dir}/d_summary_excel.csv"
    goalie_csv_file = f"{src_dir}/g_summary_excel.csv"
    output_file = f"{src_dir}/fantasy_output.xlsx"

    tables = ExcelDraftTables(forward_csv_file, defense_csv_file, goalie_csv_file, output_file)
    tables.execute()

if __name__ == "__main__":
    args = parse_args()
    main(args.league_id)
