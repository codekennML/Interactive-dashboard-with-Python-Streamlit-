"""
-- This is an interactive dashboard built with Python , Pandas , Plotly_Express and Streamlit 


"""
# Importing dependencies and libraries

from enum import unique
from string import whitespace
from matplotlib import pyplot as plt
import pandas as pd            #Pandas is a dataframe manipulation tool - pip install pandas 
import plotly_express as px
from pyparsing import White    #Plotly is a data visualization tool  -  pip install plotly_express
import streamlit as st         # Stramlit is a package for quickly bootstrapping  ml web apps  -  pip install streamlit



#set up the streamlit basic frontend config 
st.set_page_config(page_title =  "Interactive Sales Dashboard", # webpage title 
                   page_icon=":slot_machine:" , #page favicon from webfx.com/tools/emoji-cheat-sheet
                   layout= "wide" )             #change the default page centering to full width


# Read the excel sheet into a pandas dataframe using the openpyxl engine with a sheet name  of sales and displaying 1000 rows 
@st.cache
def read_file():
        df =  pd.read_excel(io = 'supermarkt_sales.xlsx',
                            engine='openpyxl' , 
                            nrows = 1000, 
                            sheet_name='Sales', 
                            usecols='B : R',
                            skiprows= 3 )

        #--Creating a new column in the dataframe that takes the time column and extracts the hour from it 
        df['Hour'] =pd.to_datetime(df['Time'], format = "%H:%M:%S").dt.hour
        return df 
df = read_file()



# --- Creating the search filter sidebar 

st.sidebar.header('Search Filter : ')    #title of search sidebar

City =  st.sidebar.multiselect(           #City Filter 
    "Select City :",
    options =  df['City'].unique(),
    default= df['City'].unique()
                              )
                    
Gender =  st.sidebar.multiselect(          
    "Gender :",
    options =  df['Gender'].unique(),
    default= df['Gender'].unique()
                              )

Customer_type =  st.sidebar.multiselect(          
    "Customer Type :",
    options =  df['Customer_type'].unique(),
    default= df['Customer_type'].unique()
                              )


df_search =  df.query(
    "City == @City & Customer_type ==  @Customer_type & Gender ==  @Gender"
)




# ---- Coding up the KPI Section
st.title(':bar_chart: Interactive Sales Dashboard')
st.markdown("##") 

total_sales =  int(df_search['Total'].sum()) #Calculate the total sales 
average_ratings  =  round(df_search['Rating'].mean(), 1) #Find the average Sale rating 
star_rating =  ":star:"     #Set ratings as stars 
average_sales= round(df_search['Total'].mean() , 2) # Get avaeage sale by transaction

left_column , middle_column , right_column =  st.columns(3)

with left_column : 
    st.subheader('Total Sales : ')
    st.subheader(' ${:,}'.format(total_sales))


with middle_column:
    st.subheader('Average Rating : ')
    st.subheader('{star_rating}{average_rating} '.format(average_rating = average_ratings, star_rating = star_rating))

with right_column:
    st.subheader('Average Sales')
    st.subheader('{}'.format(average_sales))

st.markdown("---")

# ---Creating the KPI Section using the sales by product line column using the pandas groupby function and plotly 

sales_by_product_line  = df_search.groupby(by = ["Product line"]).sum()[['Total']].sort_values(by="Total")


product_line_bar_chart  =  px.bar(sales_by_product_line , 
                     x =  "Total",
                     y =  sales_by_product_line.index ,
                     title="<b>Sales by Product Line</b>",
                     orientation="h",
                     color_discrete_sequence= ["#2596be"] * len(sales_by_product_line),
                     template= "plotly_white",
 

)

product_line_bar_chart.update_layout(
    plot_bgcolor =  "rgba(0,0,0,0)",
    xaxis =(dict(showgrid = False))
)

st.plotly_chart(product_line_bar_chart)


#--Creating the sales by hour chart
sales_by_hour =  df_search.groupby(by = ["Hour"]).sum()[['Total']]

#plot the hourly sales chart
sales_by_hour_bar_chart = px.bar(sales_by_hour , 
                     x =  sales_by_hour.index ,
                     y =  "Total",      
                     title="<b>Sales by Hour</b>",
                     color_discrete_sequence= ["#eab676"] * len(sales_by_product_line),
                     template= "plotly_white",
)

#Customize the hourly sales chart 
sales_by_hour_bar_chart.update_layout(
xaxis =  dict(tickmode = "linear"),
yaxis  = dict(showgrid =  False),
plot_bgcolor = "rgba(0,0,0,0)"
) 



st.plotly_chart(sales_by_hour_bar_chart)

##---Print a preview of the data table 
st.title(':chart_with_upwards_trend:  Sales Datatable')
st.markdown("##") 

st.dataframe(df_search) #Print a preview of our dataframe on the index page 
