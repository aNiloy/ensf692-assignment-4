# calgary_dogs.py
# Ashim Orko
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.


import pandas as pd

def load_data(file_path, indices):
    """
    Load data from an Excel file and set a multi-index.
    Parameters:
    file_path (str): Path to the Excel file.
    indices (list): List of column names to set as the multi-index.

    Returns:
    pd.DataFrame: DataFrame with the specified multi-index.
    """
    df = pd.read_excel(file_path)
    df = df.set_index(indices).sort_index()
    return df

def get_unique_values(df, header):
    """

    Extract unique values from a specified level of the multi-index DataFrame, in this case, one of the column headers

    Parameters:
    df (pd.DataFrame): The DataFrame with a multi-index.
    header (str): The name of the column from which to extract unique values.

    Returns:
    pd.Index: Unique values from the specified column.

    """
    
    return df.index.get_level_values(header).unique()

def get_user_input(valid_options):
    """
    Prompt the user for input and validate.

    Parameters:
    valid_options (iterable): An iterable of valid options.

    Returns:
    str: The validated user input.

    """

    while True:
        try:
            user_input = input("Please enter a dog breed: ").strip().upper()
            if user_input not in valid_options:
                raise KeyError
            return user_input
        except KeyError:
            print("Dog breed not found in the data. Please try again.")


def main():
    """
    Main function to analyze dog breed registrations in Calgary.

    Prompts the user for a dog breed, validates the input, and analyzes
    data for the selected breed.

    """

    # Import data here

    df = load_data("CalgaryDogBreeds.xlsx", ['Year', 'Month', 'Breed'])

    print("ENSF 692 Dogs of Calgary")

    # Extract dog breed from the DataFrame
    dog_breeds = get_unique_values(df, 'Breed')

    # User input stage

    dog_input = get_user_input(dog_breeds)

    # Data anaylsis stage

    # 1. Find and print all years where the selected breed was listed in the top breeds.

    # Extract unique years from the DataFrame index for the selected breed
    top_years = df.loc[pd.IndexSlice[:, :, dog_input], :].index.get_level_values('Year').unique()
    top_years_str = ' '.join(map(str, top_years))
    print(f"The {dog_input} was  found in the top breeds for years: {top_years_str}")


    # 2. Calculate and print the total number of registrations of the selected breed found in the dataset.

    # Sum the total number of registrations for the selected breed across all years and months
    total_reg_input = df.loc[pd.IndexSlice[:, :, dog_input], :]['Total'].sum()
    print(f"There have been {total_reg_input} {dog_input} dogs registered total")


    # 3. Calculate and print the percentage of selected breed registrations out of the total percentage for each year (2021, 2022, 2023).
 
    # Group by year and sum the total registrations for all breeds, 
    total_reg_per_year = df.groupby('Year')['Total'].sum()
    # Calculate the perecentage of the selected breed's registrations out of total registrations and drop NaN values
    percent_reg = (df.loc[pd.IndexSlice[:, :, dog_input], :].groupby('Year')['Total'].sum() / total_reg_per_year).dropna()* 100
    # Print the percentage of the selected breed for each year
    for year, percentage in percent_reg.items():
        print(f"The {dog_input} was {percentage: .6f}% of breeds in {year}")


    # 4. Calculate and print the percentage of selected breed registrations out of the total three-year percentage.
    
    # Sum the total registrations for all breeds across the three years
    total_reg_three_years = total_reg_per_year.sum()
    # Calculate the percentage of the selected breed's registrations out of the total registrations for the three years
    percent_reg_three_years = (total_reg_input / total_reg_three_years) * 100
    print(f"The {dog_input} was {percent_reg_three_years: .6f}% of breeds across all years.")


    # 5. Find and print the months that were most popular for the selected breed registrations. Print all months that tie.

    # Count the number of occurrences of each month for the selected breed
    month_counts = df.loc[pd.IndexSlice[:, :, dog_input], :].index.get_level_values('Month').value_counts()
    # Find the maximum count
    max_count = month_counts.max()
    # Filter months that have the maximum count
    popular_months = month_counts[month_counts == max_count].index.tolist()
    # Print the popular months
    print(f"Most popular month(s) for {dog_input} dogs: {' '.join(popular_months)}")


if __name__ == '__main__':
    main()
