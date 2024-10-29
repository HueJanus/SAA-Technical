import plotly.express as px
import pandas as pd

#Grab data using pandas from Excel file
df = pd.read_excel("Gantt Chart Data Set.xlsx")

#Separate docking and maintenance into individual DataFrames with their own differentiator 
docking_df = df[['Ship Name', 'Docking Start Date', 'Docking End Date']].copy()
docking_df.rename(columns={'Docking Start Date': 'Start Date', 'Docking End Date': 'End Date'}, inplace=True)
docking_df['Type'] = 'Docking' 

maintenance_df = df[["Ship Name", "Maintenance Start Date", "Maintenance End Date"]].copy()
maintenance_df.rename(columns={'Maintenance Start Date': 'Start Date', 'Maintenance End Date': 'End Date'}, inplace=True)
maintenance_df['Type'] = 'Maintenance' 

#Concatenate both DataFrames
combined_df = pd.concat([maintenance_df, docking_df], ignore_index=True)

#Create the figure using plotly 
fig = px.timeline(combined_df,
                   x_start="Start Date", 
                   x_end="End Date",    
                   y="Ship Name",   #y-axis label
                   hover_name= "Type",  #Main text when hovered, also used to offset bars 
                   color_discrete_sequence=px.colors.qualitative.Dark2,
                   template="seaborn",
                   opacity=.7,
                   color= "Type",   #Can't use names, otherwise there'd be no way of stacking the bars
                   pattern_shape= "Ship Name",  #Use patterns to differentiate between ships (max of 8)
                   pattern_shape_sequence=["", "/", "\\", "|", "-", "x", "+", "."],
                   hover_data= {    #Data shown when hovering over bar
                      "Ship Name": True,
                      "Type": False,
                      "Start Date": "|%m-%d-%Y",  #Format dates as Month-Day-Year
                      "End Date": "|%m-%d-%Y", 
                      
                    }
                  
                 )

#Offset docking and maintenance bars 
for obj in fig.data:
    period = obj.hovertext[0]
    if (period == "Maintenance"):
        obj.width = 0.3
        obj.offset = 0.15
    elif (period == "Docking"):
        obj.width = 0.3
        obj.offset = -0.15

fig.show()

