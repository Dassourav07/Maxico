# Maxico

![Screenshot 2024-07-01 135926](https://github.com/Dassourav07/Maxico/assets/94233240/142ef1d8-4b82-49b6-a274-3b6ac5e48471)


code analysis Mexico Toy Sales :

The dashboard provides a comprehensive overview of toy sales in Mexico, offering key insights through various visualizations. The primary components of the dashboard include displays of the total revenue generated from toy sales over a specified period. It includes a line graph showing the trend of sales, highlighting peak sales periods. A bar chart lists the top-selling toy categories, showing their respective sales volumes and revenues. This helps in identifying which categories are driving the most sales and which ones might need marketing support.


To create a similar dashboard using Python and Excel, follow these steps:
Data Collection: Gather the toy sales data from various sources such as sales databases,The data should include details like product categories, sales volumes, revenues, customer demographics, and sales regions.


Data Cleaning and Preparation: Use Python libraries like pandas to clean and prepare the data. This involves handling missing values, normalizing data formats, and ensuring consistency across datasets.
import pandas as PD
# Load the sales data
data = pd.read_csv('toy_sales_data.csv')
# Clean the data
data.drop(inplace=True)  # Drop rows with missing values
data['date'] = pd.to_datetime(data['date'])  # Convert date column to DateTime

Creating the Dashboard in Excel: Export the cleaned and analyzed data to Excel and use Excel's built-in features to create the dashboard.
In Excel:
Create a summary sheet with key metrics.
Use pivot tables to aggregate data by product categories, regions, and sales channels.
Insert charts (line, bar, pie) to visualize the insights similar to those described in the dashboard above.
Use Excel's slicers and filters to make the dashboard interactive.
By following these steps, you can effectively replicate a data analysis dashboard for Mexico toy sales using Python and Excel.


Streamlit application that visualizes toy sales data from an Excel file. The data includes sales, stores, products, and inventory. The dashboard provides insights through various metrics and visualizations. Let's break down the code and analyze its functionality step-by-step.

streamlit: Library for creating web apps.
plotly.express Library for creating interactive plots.
pandas: Library for data manipulation.
os: Library for interacting with the operating system.
warnings: Library to control warnings.

streamlit: Library for creating web apps.
plotly.express Library for creating interactive plots.
pandas: Library for data manipulation.
os: Library for interacting with the operating system.
warnings: Library to control warnings 

st.set_page_config: Configures the Streamlit app.
st. title: Sets the title of the app.
st. markdown: Adjusts the padding of the container using custom CSS.

file_path: Specifies the location of the Excel file.
os. path.exists: Checks if the file exists.
pd.read_excel: Reads the specified sheets from the Excel file into DataFrames.

pd.to_datetime: Converts the 'Date' column to datetime format.
PD. merge: Merges the sales and stores DataFrames on 'Store_ID'.
dict(zip(...)): Creates dictionaries to map product and store IDs to names.
df['...'] = df['...'].map(...): Replaces IDs with names in the merged DataFrame.

st. sidebar.date_input: Creates date input widgets in the sidebar for filtering.
st. sidebar.multi-select: Creates multi-select widgets for filtering by city and product.
Filtering: Filters the DataFrame based on the selected dates, cities, and products.

PD. groupby: Aggregates inventory by summing 'Stock_On_Hand' for each 'Product_ID'.
Summing metrics: Calculates total revenue, profit, loss, and inventory.
Out of stock: Determines the number of out-of-stock products.


















![Screenshot 2024-07-01 140011](https://github.com/Dassourav07/Maxico/assets/94233240/42aacd68-9a0f-4ea8-994c-3be8fc1f0043)

![Screenshot 2024-07-01 142122](https://github.com/Dassourav07/Maxico/assets/94233240/0e33e4a9-35db-4f26-8d77-d62b9a93a00c)

![Screenshot 2024-07-01 140103](https://github.com/Dassourav07/Maxico/assets/94233240/e5fd2de7-f69c-48d5-bb4a-edf24be0bc2a)

![Screenshot 2024-07-01 140351](https://github.com/Dassourav07/Maxico/assets/94233240/dec1b0eb-3430-4868-b688-4e8e0a086978)

![Screenshot 2024-07-01 140516](https://github.com/Dassourav07/Maxico/assets/94233240/1819cac3-2a80-4fe5-9230-af7d8b359afd)
