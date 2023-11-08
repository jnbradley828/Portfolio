import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import calendar

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',
                 delimiter=',',
                 index_col='date',
                 parse_dates=['date'])
#print(df.head(), '\n', len(df))

# Clean data
df = df[(df['value'] >= df['value'].quantile(.025))
        & (df['value'] <= df['value'].quantile(.975))]
#print(len(df))


def draw_line_plot():
  # Draw line plot

  fig, ax = plt.subplots(figsize=(16, 8))
  ax.plot(df['value'], color='green')
  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')
  ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.copy(deep=True)
  df_bar['year'] = df_bar.index.year
  df_bar['month'] = df_bar.index.month
  df_bar['month'] = df_bar['month'].apply(lambda x: calendar.month_name[x])
  custom_month_order = [calendar.month_name[i] for i in range(1, 13)]  # January to December
  df_bar = df_bar.groupby(['year', 'month']).mean().unstack().reorder_levels([1, 0], axis=1)[custom_month_order]

  # Draw bar plot

  fig, ax = plt.subplots(figsize=(10, 6))
  df_bar.plot(kind = 'bar', stacked = False, ax=ax)
  plt.xlabel('Years')
  plt.ylabel('Average Page Views')
  ax.get_legend().set_title('Months')
  ax.legend(custom_month_order)
  
  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig

def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]
  
  # Draw box plots (using Seaborn)

  fig, axes = plt.subplots(1,2,figsize=(15,6))
  sns.boxplot(y = 'value', data = df_box, x = 'year', ax = axes[0])
  axes[0].set_xlabel('Year')
  axes[0].set_ylabel('Page Views')
  axes[0].set_title('Year-wise Box Plot (Trend)')

  sns.boxplot(y = 'value', data = df_box, x = 'month', ax = axes[1], order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
  axes[1].set_xlabel('Month')
  axes[1].set_ylabel('Page Views')
  axes[1].set_title('Month-wise Box Plot (Seasonality)')
  
  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
