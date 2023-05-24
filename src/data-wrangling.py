import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib import pyplot

def get_data():
    filename = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"

    headers = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style",
               "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight",
               "engine-type",
               "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower",
               "peak-rpm", "city-mpg", "highway-mpg", "price"]

    df = pd.read_csv(filename, names=headers)
    return df


def calculate_mean_and_replace_NaN(column):
    # Calculate the mean value for the "column" column
    avg_column = df[column].astype("float").mean(axis=0)
    print("Average of ", column, ":", avg_column)
    # replace "NaN" with mean value in "column" column
    df[column].replace(np.NaN, avg_column, inplace=True)
    print("replace NaN with mean value in", column)
    print("")

def deal_with_missing_data(df):
    # Convert "?" to NaN
    df.replace('?', np.NaN, inplace=True)

    # To see what the data set looks like, we'll use the head() method.
    # print(df.head())

    # Evaluating missing data
    missing_data = df.isnull()
    # print(missing_data.head(5)) --> "True" means the value is a missing value while "False" means the value is not a missing value.

    # Count missing values in each column
    """for column in missing_data.columns.values.tolist():
        print(column)
        # func value_counts() will Return a Series containing counts of unique values.
        print(missing_data[column].value_counts())
        print("")"""

    # Deal with missing data
    """ 
    Replace by mean:
        • "normalized-losses": 41 missing data, replace them with mean
        • "stroke": 4 missing data, replace them with mean
        • "bore": 4 missing data, replace them with mean
        • "horsepower": 2 missing data, replace them with mean
        • "peak-rpm": 2 missing data, replace them with mean
    """

    # Calculate the mean value for the "normalized-losses" column & replace "NaN" with mean value
    calculate_mean_and_replace_NaN('normalized-losses')
    # Calculate the mean value for the "bore" column & replace "NaN" with mean value
    calculate_mean_and_replace_NaN('bore')
    calculate_mean_and_replace_NaN('horsepower')
    calculate_mean_and_replace_NaN('peak-rpm')

    # To see which values are present in a particular column, we can use the "value_counts (" method:
    # print(df['num-of-doors'].value_counts().idxmax())
    df["num-of-doors"].replace(np.nan, df['num-of-doors'].value_counts().idxmax(), inplace=True)

    # Finally, let's drop all rows that do not have price data: axis=0 -> delete row, axis = 1 -> delete the column
    # simply drop whole row with NaN in "price" column
    df.dropna(subset=["price"], axis=0, inplace=True)
    # reset index, because we droped two rows
    df.reset_index(drop=True, inplace=True)


def correct_data_format(df):
    # Convert data types to proper format
    df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
    df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
    df[["price"]] = df[["price"]].astype("float")
    df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")


def data_standardization(df):
    # print(df.head())
    # Convert mpg to L/100km by mathematical operation (235 divided by mpg)
    df['city-mpg'] = 235 / df["city-mpg"]
    # transform mpg to L/100km by mathematical operation (235 divided by mpg)
    df["highway-mpg"] = 235 / df["highway-mpg"]
    # rename column name from "highway-mpg" to "highway-L/100km"
    df.rename(columns={"city-mpg": 'city-L/100km'}, inplace=True)
    df.rename(columns={"highway-mpg": 'highway-L/100km'}, inplace=True)
    # check your transformed data
    # print("standardization ....")
    # print(df.head())


def data_normalization(df):
    # print(df[["length", "width", "height"]].head())
    # replace (original value) by (original value)/(maximum value)
    df['length'] = df['length'] / df['length'].max()
    df['width'] = df['width'] / df['width'].max()
    df['height'] = df['height'] / df['height'].max()
    # show the scaled columns
    # print(df[["length", "width", "height"]].head())


def data_bining(df):
    # Convert data to correct format
    df["horsepower"] = df["horsepower"].astype(int, copy=True)

    # plt.pyplot.hist(df["horsepower"])
    # # set x/y labels and plot title
    # plt.pyplot.xlabel("horsepower")
    # plt.pyplot.ylabel("count")
    # plt.pyplot.title("horsepower without bins")
    # plt.pyplot.show()

    """
    We would like 3 bins of equal size bandwidth so we use numpy's linspace(start_value, end_value, numbers_generated) function.
    Since we want to include the minimum value of horsepower, we want to set start_value = min(df["horsepower"]).
    Since we want to include the maximum value of horsepower, we want to set end_value = max(df ["horsepower"])
    Since we are building 3 bins of equal length, there should be 4 dividers, so numbers_generated = 4.
    """
    bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
    # We set group names:
    group_names = ['Low', 'Medium', 'High']
    # We apply the function "cut" to determine what each value of df [ 'horsepower'] belongs to.
    df['horsepower-binned'] = pd.cut(df['horsepower'], bins, labels=group_names, include_lowest=True)
    print(df[['horsepower', 'horsepower-binned']].head(20))
    # # Let's see the number of vehicles in each bin:
    print(df["horsepower-binned"].value_counts())


def bins_visualization(df):
    # Bins Visualization
    # Normally, a histogram is used to visualize the distribution of bins we created above.
    plt.pyplot.hist(df["horsepower"], bins=3)
    # set x/y labels and plot title
    plt.pyplot.xlabel("horsepower")
    plt.pyplot.ylabel("count")
    plt.pyplot.title("horsepower bins")
    plt.pyplot.show()


def label_not_numeric_categories(df, column, col_category_1, col_category_2, new_name_col_category_1,
                                 new_name_col_category_2):
    """
    Why we use indicator variables?
        We use indicator variables so we can use categorical variables for regression analysis in the later modules,
        because categorical variables is not analysierbar, only numeric variable could be analysiert.
    Example
        We see the column "fuel-type" has two unique values: "gas" or "diesel". Regression doesn't understand words, only numbers. To use this attribute in regression analysis, we convert "fuel-type" to indicator
        variables.
        We will use pandas' method 'get_dummies' to assign numerical values to different categories of fuel type.
    """
    # print(df.columns)
    # Get the indicator variables and assign it to data frame "dummy_variable_1": dummy_variable_1 will have then 2 columns
    # "gas" and "diesel". If df["fuel-type"] == gas ==> gas: true, diesel: false
    dummy_variable_1 = pd.get_dummies(df[column])
    # Change the column names for clarity:
    dummy_variable_1.rename(columns={col_category_1: new_name_col_category_1, col_category_2: new_name_col_category_2},
                            inplace=True)
    # In the dataframe, column 'fuel-type' has values for 'gas' and 'diesel' as Os and 1s now.

    # merge data frame "df" and "dummy_variable_1"
    df = pd.concat([df, dummy_variable_1], axis=1)
    # drop original column "fuel-type" from "df"
    df.drop(column, axis=1, inplace=True)
    # print(df.head())


def save_cvs(df, name):
    # this file will be saved in the current working directory by default.
    df.to_csv(name)

    """
    # Instead of just providing the filename like 'clean_df.csv',
    # you can provide the complete file path where you want the file to be saved.
    # Assuming your desired path is '/path/to/save/clean_df.csv'
    file_path = '/path/to/save/clean_df.csv'
    # Save the DataFrame as CSV at the specified path
    df.to_csv(file_path, index=False)
    """


if __name__ == '__main__':
    df = get_data()
    deal_with_missing_data(df)
    correct_data_format(df)
    data_standardization(df)
    data_normalization(df)
    data_bining(df)
    # show histogram of bined columns
    bins_visualization(df)
    label_not_numeric_categories(df, "fuel-type", 'gas', 'diesel', 'fuel-type-gas', 'fuel-type-diesel')
    label_not_numeric_categories(df, "aspiration", 'std', 'turbo', 'aspiration-std', 'aspiration-turbo')
    save_cvs(df, 'clean_df.csv')
