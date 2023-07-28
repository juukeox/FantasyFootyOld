import pandas as pd
import os

def merge_tables():

    # Get the current directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the relative paths to the input files
    value_data_path = os.path.join(script_directory, 'value_data.xlsx')
    form_data_path = os.path.join(script_directory, 'form_data.xlsx')

    df1 = pd.read_excel('value_data.xlsx')

    # Read the second table
    df2 = pd.read_excel('form_data.xlsx')

    # Clean the 'Price' column in df1
    if df1['Price'].dtype == 'object':
        df1['Price'] = df1['Price'].str.replace('£', '').str.replace(' m', '').astype(float)

    # Clean the 'Price' column in df2
    if df2['Price'].dtype == 'object':
        df2['Price'] = df2['Price'].str.replace('£', '').str.replace(' m', '').astype(float)

    # Convert relevant columns to lowercase for both DataFrames
    columns_to_upper = ['Name', 'Team', 'Position']
    df1[columns_to_upper] = df1[columns_to_upper].apply(lambda x: x.str.upper())
    df2[columns_to_upper] = df2[columns_to_upper].apply(lambda x: x.str.upper())

    # Merge the two DataFrames
    merged_df = pd.merge(df1, df2, on=['Name', 'Team', 'Position', 'Price', 'Points'], how='outer')

    # Define the desired columns for the final table
    desired_columns = ['Name', 'Team', 'Position', 'Price', 'PointsperGame', 'PointsperMillion', 'Pick %', 'Last 6', 'Points']

    # Select the desired columns in the merged DataFrame
    merged_df = merged_df[desired_columns]

    # Fill empty cells with 0
    merged_df.fillna(0, inplace=True)

    # Capitalize all strings in the DataFrame
    merged_df = merged_df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

    # Save the merged DataFrame to an Excel file
    file_path = os.path.join(os.getcwd(), 'merged.xlsx')
    merged_df.to_excel(file_path, index=False)
    merged_df = pd.read_excel(file_path) #
    return merged_df

merge_tables()