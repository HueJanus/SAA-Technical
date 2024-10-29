import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors  #Import mplcursors for hover functionality

#Grab data using pandas from Excel file
df = pd.read_excel("Gantt Chart Data Set.xlsx")

#Separate docking and maintenance into individual DataFrames with their own differentiator 
docking_df = df[["Ship Name", "Docking Start Date", "Docking End Date"]].copy()
docking_df.rename(columns={"Docking Start Date": "Start Date", "Docking End Date": "End Date"}, inplace=True)
docking_df["Type"] = "Docking"

maintenance_df = df[["Ship Name", "Maintenance Start Date", "Maintenance End Date"]].copy()
maintenance_df.rename(columns={"Maintenance Start Date": "Start Date", "Maintenance End Date": "End Date"}, inplace=True)
maintenance_df["Type"] = "Maintenance"

#Concatenate both DataFrames
combined_df = pd.concat([maintenance_df, docking_df], ignore_index=True)

#Create the figure and set up the axes
fig, ax = plt.subplots(figsize=(12, 8))

#Generate a color map for unique ship colors
ship_names = combined_df["Ship Name"].unique()
base_colors = plt.get_cmap("tab20", len(ship_names))  #tab20 are 20 distinct colors chosen by Matplotlib

#Store bar information for hover functionality
bars = []  
hover_data = []  #Store hover text information

#Plot each ship's maintenance and docking periods with unique colors
for i, ship in enumerate(ship_names):
    ship_data = combined_df[combined_df["Ship Name"] == ship]
    ship_base_color = base_colors(i)  #Assign unique base color for each ship
    
    for _, row in ship_data.iterrows():  #Iterate through rows in ship data
        start_date = row["Start Date"]
        end_date = row["End Date"]
        period_type = row["Type"]
        bar_color = ship_base_color
        bar_alpha = 0.7 if period_type == "Docking" else 1.0  #Slightly transparent for docking periods
        
        #Offset docking and maintenance bars 
        y_position = i - 0.125 if period_type == "Docking" else i + 0.125
        
        #Create bar
        bar = ax.barh(y_position, 
                       end_date - start_date, 
                       left=start_date, 
                       height=0.25, 
                       color=bar_color,
                       alpha=bar_alpha,
                       label=ship if period_type == "Maintenance" else "")  #Label each ship only once for the legend
        
        bars.append(bar[0])  #Store the bar artist only
        
        #Prepare hover text data
        duration_days = (end_date - start_date).days
        hover_data.append({
            "ship": row["Ship Name"],
            "type": row["Type"],
            "start": start_date,
            "end": end_date,
            "duration": duration_days
        })
        
        #Calculate duration in days only for maintenance bars
        if period_type == "Maintenance":
            ax.text(start_date + (end_date - start_date) / 2,  #Positioning in the middle of the bar
                    y_position,
                    f"{duration_days} days",  #Text content
                    ha="center",  #Horizontal alignment
                    va="center",  #Vertical alignment
                    color="black",  
                    fontsize=10)  

#Customizing the plot
ax.set_yticks(range(len(ship_names)))
ax.set_yticklabels(ship_names)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  #Show date ticks quarterly
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.xaxis.grid(True, linestyle="--", alpha=0.7)
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Ship Name")
plt.title("Gantt Chart of Ship Maintenance and Docking Periods")

#Adjust the legend position to prevent overlapping with the chart
plt.legend(loc="upper left", bbox_to_anchor=(1, 1), borderaxespad=0.)
plt.tight_layout()  #Improve spacing

#Add hover functionality
cursor = mplcursors.cursor(bars, hover=True)

#Customize the tooltip
@cursor.connect("add")
def on_add(sel):
    index = bars.index(sel.artist)  #Get the index of the bar in the list
    data = hover_data[index]  #Get corresponding hover data
    start_date_str = data["start"].strftime("%m-%d-%Y")  #Change to a more readable format
    end_date_str = data["end"].strftime("%m-%d-%Y")
    duration_text = f"{data['duration']} days"
    
    sel.annotation.set_text(f"Ship: {data['ship']}\n"
                             f"Type: {data['type']}\n"
                             f"Start: {start_date_str}\n"
                             f"End: {end_date_str}\n"
                             f"Duration: {duration_text}")

#Display the chart
plt.show()
