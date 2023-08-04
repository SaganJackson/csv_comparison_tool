import sys
import pandas as pd


def delete_duplicates(csv_file_path: str, output_file_path: str):
    file = pd.read_csv(csv_file_path)
    # Deletes the duplicates based on the 'LocationId' column -> keeps only the last occurrence
    file_no_duplicates = file.drop_duplicates(subset='LocationId', keep='last')
    file_no_duplicates.to_csv(output_file_path, index=False)
    print("Duplicates removed and new CSV file created successfully!")


def swap_columns(input_file_path: str, output_file_path: str, column2_name='CustomerId', column3_name='ContractId'):
    file = pd.read_csv(input_file_path)

    # Gets a copy of the data from column 2 and column 3
    column2_data = file[column2_name].copy()
    column3_data = file[column3_name].copy()

    # Swaps the columns and its data
    file[column2_name] = column3_data
    file[column3_name] = column2_data

    # Swap the column names
    file.rename(columns={column2_name: column3_name,
                column3_name: column2_name}, inplace=True)

    file.to_csv(output_file_path, index=False)
    print("CustomerId and ContractId columns have been swapped successfully!")


def compare_csv(file1_path: str, file2_path: str):
    file1 = pd.read_csv(file1_path)
    file2 = pd.read_csv(file2_path)

    if file2.equals(file1):
        print("The two files have the same data after swapping columns and removing duplicates.")
    else:
        print("The two files have different data.")

        # Find different rows
        different_rows = []
        for index, row in file1.iterrows():
            if not row.equals(file2.iloc[index]):
                different_rows.append(index)

        # Print different rows
        if different_rows:
            print("Rows that are different between the two files:")
            print(file2.iloc[different_rows])


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python your_script.py <csv_file_path> <output_file_path> <input_file_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    input_file_path = sys.argv[3]

    if 'beta' in csv_file_path:
        delete_duplicates(csv_file_path, output_file_path)
    swap_columns(output_file_path,
                 '/Users/saganj/workplace/Compare_csv/columns_swapped.csv')
    compare_csv(
        '/Users/saganj/workplace/Compare_csv/columns_swapped.csv', input_file_path)
