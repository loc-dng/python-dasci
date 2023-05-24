# how to download data and use directly (no need to download locally)

# #you are running the lab in your  browser, so we will install the libraries using ``piplite``
# import piplite
# import micropip
# await piplite.install(['pandas'])
# await piplite.install(['matplotlib'])
# await piplite.install(['scipy'])
# await piplite.install(['seaborn'])
# await micropip.install(['ipywidgets'],keep_going=True)
# await micropip.install(['tqdm'],keep_going=True)


# import pandas library
import pandas as pd
import numpy as np

#This function will download the dataset into your browser 

from pyodide.http import pyfetch

async def download(url, filename):
    response = await pyfetch(url)
    if response.status == 200:
        with open(filename, "wb") as f:
        	# write the fetched results into the file
            f.write(await response.bytes())


path = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"

#you will need to download the dataset; if you are running locally, please comment out the following 
await download(path, "auto.csv")

path="auto.csv"

# Read the online file by the URL provides above, and assign it to variable "df"
df = pd.read_csv(path, header=None)


# --------------- --------------- --------------- --------------- --------------- ---------------
# if data has no headers --> add headers
# create headers list
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
print("headers\n", headers)
# change the data frame
df.columns = headers
# or just need to see the headers only
# df = pd.read_csv(filename, names = headers)


#We need to replace the "?" symbol with NaN so the dropna() can remove the missing values:
df1=df.replace('?',np.NaN)

#We can drop missing values along the column "price" as follows:
df=df1.dropna(subset=["price"], axis=0)
df.head(20)


# show the first 5 rows using dataframe.head() method
print("The first 5 rows of the dataframe") 
df.head(5)

# --------------- --------------- --------------- --------------- --------------- ---------------
# Describe
df.describe(include = "all")

# describe statistisch only these 2 columns
df[['length', 'compression-ratio']].describe()


# --------------- --------------- --------------- --------------- --------------- ---------------
# save dataset
# save the dataframe df as automobile.csv to your local machine, where index = False means the row names will not be written
df.to_csv("automobile.csv", index=False)