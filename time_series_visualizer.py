import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index('date')

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 5), dpi=100)  # Adjusted figure size
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    sns.lineplot(data=df, x=df.index, y="value", legend=False)  # Specified x and y
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Year"] = df_bar.index.year
    df_bar["Month"] = df_bar.index.strftime('%B')  # Use full month names
    
    # Pivot table to calculate mean values for each month and year
    df_bar = df_bar.groupby(["Year", "Month"])["value"].mean().reset_index()

    # Ensure months are in correct order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(14, 8), dpi=100)
    ax.set_title("Monthly Average freeCodeCamp Forum Page Views")

    # Plot the bar chart with the correct order of months
    chart = sns.barplot(data=df_bar, x="Year", y="value", hue="Month", hue_order=month_order, palette="tab10")
    chart.set_xticks(chart.get_xticks())  # Set fixed ticks
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90, horizontalalignment='center')
    ax.set_ylabel("Average Page Views")
    ax.set_xlabel("Years")  # Corrected to match the expected test label
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = df_box['date'].dt.year
    df_box['Month'] = df_box['date'].dt.strftime('%b')  # Abbreviated month name

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(16, 5), dpi=100)  # Adjusted figure size
    
    # Yearly boxplot
    sns.boxplot(data=df_box, x="Year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Monthly boxplot with ordered months
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="Month", y="value", order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig