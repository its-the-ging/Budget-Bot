from idlelib.pyparse import trans
from pathlib import Path
from datetime import datetime
import pandas as pd
import sys
import csv

class Vanguard:
    def __init__(self, activity_csv_path):
        self.activity_csv_path = Path(activity_csv_path)
        self.summary_df, self.transaction_df = self._parse_activity_csv()

    def _parse_activity_csv(self):

        # Check file exists and is CSV
        if not self.activity_csv_path.exists():
            print(f'ERROR: Vanguard CSV not located at {self.activity_csv_path}')
            sys.exit()
        elif not self.activity_csv_path.suffix == '.csv':
            print(f'ERROR: {self.activity_csv_path} is not a CSV file')
            sys.exit()

        # Open file and parse header
        transaction_start_index = 0
        with open(self.activity_csv_path, 'r') as f:
            rows = csv.reader(f, delimiter=',')

            for index, contents in enumerate(rows):
                transaction_start_index = index if 'Trade Date' in contents else transaction_start_index
            summary_stop_index = transaction_start_index - 4

        # Dataframe for summary of account values
        summary_df = pd.read_csv(self.activity_csv_path, nrows=summary_stop_index)
        summary_df = summary_df.iloc[:,:6]

        # Summary of transactions for time period on sheet
        transaction_df = pd.read_csv(self.activity_csv_path, skiprows=transaction_start_index)
        transaction_df = transaction_df.iloc[:,:14]

        return summary_df, transaction_df

    def get_transactions_by_month(self):
        print(self.transaction_df['Trade Date'])
        self.transaction_df['Trade Date'] = self.transaction_df['Trade Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
        print(self.transaction_df['Trade Date'])

if __name__ == '__main__':
    vanguard = Vanguard('/home/ze-flyer/Downloads/vanguard_activity_18mo.csv')
    vanguard.get_transactions_by_month()