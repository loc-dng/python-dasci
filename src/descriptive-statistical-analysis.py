import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def show_correlation_regplot(x_achse, y_achse, df):
    """ regplot can be used to show the scatterplot diagram for 2 numerical variables! """
    sns.regplot(x=x_achse, y=y_achse, data=df)
    # lets the lower limit to 0, but leaves the upper limit unspecified (blank) -> auto determined based on the data
    plt.ylim(0, )
    plt.title('RegPlot between ' + x_achse + ' and ' + y_achse)
    plt.show()


def show_correlation_boxplot(x_achse, y_achse, df):
    """These are variables that describe a 'characteristic' of a data unit, and are selected from
    a small group of categories. The categorical variables can have the type "object" or "int64".
    A good way to visualize categorical variables is by using boxplots."""
    sns.boxplot(x=x_achse, y=y_achse, data=df)
    plt.title('BoxPlot between ' + x_achse + ' and ' + y_achse)
    plt.show()


def analyzing_feature_using_visualization(df):
    """
    Analyzing Individual Feature Patterns Using Visualization
    """
    # When visualizing individual variables, it is important to first understand what type of variable you are dealing with.
    # This will help us find the right visualization method for that variable.
    # print(df.dtypes)
    # print('PEAK-rpm type: ', df['peak-rpm'].dtypes)

    # For example, we can calculate the correlation between variables  of type "int64" or "float64" using the method "corr"
    # --> Correlation of all numeric variables in df!!
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    correlation_matrix = df[numeric_columns].corr()
    # print(correlation_matrix)
    # Find correlation btw. columns: bore, stroke, compression-ratio, and horsepower.
    # print(df[['bore', 'stroke', 'compression-ratio', 'horsepower']].corr())

    # --------------------- REGPLOT --> 2 NUMERIC VARIABLES --------------------------------------
    """In order to start understanding the (linear) relationship between an individual variable and the price, 
    we can use "regplot" which plots the scatterplot plus the fitted regression line for the data. 
    This will be useful later on for visualizing the fit of the simple linear regression model as well."""
    # # Positive Linear Relationship
    show_correlation_regplot(x_achse="engine-size", y_achse="price", df=df)
    # # Negative Linear Relationship
    # show_correlation_regplot("highway-mpg", "price", df)
    # # Weak LR
    # show_correlation_regplot("peak-rpm", "price", df)

    # --------------------- BOXPLOT --> (1 CATEGORICAL + 1 NUMERIC) VARIABLES --------------------------------------
    """These are variables that describe a 'characteristic' of a data unit, and are selected from
        a small group of categories. The categorical variables can have the type "object" or "int64".
        A good way to visualize categorical variables is by using boxplots."""
    show_correlation_boxplot(x_achse="body-style", y_achse="price", df=df)
    # We see that the distributions of price between the different body-style categories have a significant overlap,
    # so body-style would not be a good predictor of price.

    # Let's examine engine "engine-location" and "price"
    show_correlation_boxplot(x_achse="engine-location", y_achse="price", df=df)
    # Here we see that the distribution of price between these two engine-location categories, front and rear,
    # are distinct enough to take engine-location as a potential good predictor of price!!!


def count_values_and_convert_to_frame(dataframe, series):
    """
    # Value counts is a good way of understanding how many units of each characteristic/variable we have
    # Notes: --> only works on pandas series (column), not pandas dataframes
    """
    # print(df['drive-wheels'].value_counts())
    # convert the series to a dataframe
    drive_wheels_counts = dataframe[series].value_counts().to_frame()
    # rename the column  'drive-wheels' to 'value_counts'
    drive_wheels_counts.rename(columns={series: 'value_counts'}, inplace=True)
    # Now let's rename the index to 'drive-wheels':
    drive_wheels_counts.index.name = series
    print(drive_wheels_counts.head(10))


def descriptive_analyse(dataframe):
    """ The describe() automatically computes basic statistics for all continuous variables.
    Any NaN values are automatically skipped in these statistics.
    This will show:
        the count of that variable
        the mean
        the standard deviation (std)
        the minimum value
        the IQR (Interquartile Range: 25%, 50% and 75%)
        the maximum value
    """
    # print(df.describe())
    # print(df.describe(include=['object']))
    count_values_and_convert_to_frame(dataframe, series='drive-wheels')
    count_values_and_convert_to_frame(dataframe, series='engine-location')
    # After examining the value counts of the engine location, we see that engine location
    # would not be a good predictor variable for the price.
    # This is bcs we only have 3cars with a rear engine and 198 with an engine in the front, so this result is skewed.
    # Thus, we are not able to draw any conclusion's about the engine location.


def group_by_then_show_pivot_and_heatmap(dataframe, should_show_pivot, should_show_heatmap):
    """
    The "groupby" method groups data by different categories. The data is grouped based on one or several variables,
    and analysis is performed on the individual groups.
    """
    # let's group by both 'drive-wheels' and 'body-style'. This groups the dataframe by the unique
    # combination of 'drive-wheels' and 'body-style'
    df_gptest = dataframe[['drive-wheels', 'body-style', 'price']]
    grouped_test1 = df_gptest.groupby(['drive-wheels', 'body-style'], as_index=False).mean()
    # print(grouped_test1)

    # --> This grouped data is much easier to visualize when it is made into a PIVOT table
    grouped_pivot = grouped_test1.pivot(index='drive-wheels', columns='body-style')
    # Often, we won't have data for some of the pivot cells. We can fill these missing cells with the value 0
    grouped_pivot = grouped_pivot.fillna(0)  # fill missing values with 0
    if should_show_pivot:
        print(grouped_pivot)

    if should_show_heatmap:
        # Let's use a heat map to visualize the relationship between Body Style vs Price.
        plt.pcolor(grouped_pivot, cmap='RdBu')
        row_labels = grouped_pivot.columns.levels[1]
        col_labels = grouped_pivot.index
        # Add x-axis and y-axis labels
        plt.xticks(np.arange(len(row_labels)) + 0.5, row_labels, rotation='vertical')
        plt.yticks(np.arange(len(col_labels)) + 0.5, col_labels)

        plt.colorbar()
        plt.show()


def cal_pearson_correlation(dataframe, series_1, series_2):
    """The Pearson Correlation measures the linear dependence between two variables X and Y.
    The resulting coefficient is a value between -1 and 1 inclusive, where:
        1: Perfect positive linear correlation.
        0: No linear correlation, the two variables most likely do not affect each other.
        -1: Perfect negative linear correlation.
    """
    # print(dataframe.corr())
    
    # P-Value
    """
    The P-value is the probability value that the correlation between these two variables 
    is statistically significant.Normally, we choose a significance level of 0.05, which means that 
    we are 95% confident that the correlation between the variables is significant.
    By convention, when the
         p-value < 0.001: strong evidence that the correlation is significant.
         p-value < 0.05: moderate evidence that the correlation is significant.
         p-value < 0.1: weak evidence that the correlation is significant.
         p-value > 0.1: no evidence that the correlation is significant.
    
    ---> using  "stats" module in the "scipy"  library.
    """
    # calculate the  Pearson Correlation Coefficient and P-value of 'wheel-base' and 'price'.
    pearson_coef, p_value = stats.pearsonr(dataframe[series_1], dataframe[series_2])
    print("The Pearson Correlation Coefficient is", pearson_coef, " with a P-value of P =", p_value)


def cal_anova(dataframe):
    """
    The Analysis of Variance (ANOVA) is a statistical method used to test whether there are significant differences between the,
    means of two or more groups.
    ANOVA returns two parameters:
        F-test score: ANOVA assumes the means of all groups are the same, calculates how much the actual means deviate from
    the assumption, and reports it as the F-test score. A larger score means there is a larger difference between the means.
        P-value: P-value tells how statistically significant our calculated score value is.
    -> If our price variable is strongly correlated with the variable we are analyzing, we expect ANOVA to return a sizeable F-test
    score and a small p-value.
    """

    # Since ANOVA analyzes the difference between different groups of the same variable, the groupby func() is needed.
    # Because the ANOVA algorithm averages the data automatically, we do not need to take the average before hand.
    df_gptest = df[['drive-wheels', 'body-style', 'price']]
    grouped_test2 = df_gptest[['drive-wheels', 'price']].groupby(['drive-wheels'])

    # We can obtain the values of the method group using the method "get_group".
    # grouped_test2.get_group('4wd')['price']

    # We can use the function 'f_oneway' in the module 'stats' to obtain the F-test score and P-value.
    # ANOVA
    f_val, p_val = stats.f_oneway(grouped_test2.get_group('fwd')['price'], grouped_test2.get_group('rwd')['price'],
                                  grouped_test2.get_group('4wd')['price'])
    print("Total ---> ANOVA results: F=", f_val, ", P =", p_val)
    # This is a great result with a large F-test score showing a strong correlation and a P-value of almost 0 implying
    # almost certain statistical significance. But does this mean all three tested groups are  this highly correlated?

    # Let's examine them separately.
    # fwd and rwd
    f_val, p_val = stats.f_oneway(grouped_test2.get_group('fwd')['price'], grouped_test2.get_group('rwd')['price'])
    print("ANOVA results: F=", f_val, ", P =", p_val)
    # 4wd and rwd
    f_val, p_val = stats.f_oneway(grouped_test2.get_group('4wd')['price'], grouped_test2.get_group('rwd')['price'])
    print("ANOVA results: F=", f_val, ", P =", p_val)
    # 4wd and fwd
    f_val, p_val = stats.f_oneway(grouped_test2.get_group('4wd')['price'], grouped_test2.get_group('fwd')['price'])
    print("ANOVA results: F=", f_val, ", P =", p_val)
    """We notice that ANOVA for the categories `4wd` and `fwd` yields a high p-value > 0.1, so the calculated 
    F-test score is not very statistically significant. 
    This suggests we can't reject the assumption that the means of these two groups are the same, or, in other words, 
    we can't conclude the difference in correlation to be significant."""


if __name__ == '__main__':
    path = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/automobileEDA.csv'
    df = pd.read_csv(path)
    # analyzing_feature_using_visualization(df)
    # descriptive_analyse(df)

    # group_by_then_show_pivot_and_heatmap(df, should_show_pivot=False, should_show_heatmap=True)
    cal_pearson_correlation(df, 'wheel-base', 'price')
    cal_anova(df)