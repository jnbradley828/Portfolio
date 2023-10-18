import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')
df.set_index(df['id'], inplace=True)

# Add 'overweight' column

df['overweight'] = ( df['weight'] / ( (df['height']/100) ** 2 ) > 25 ).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = (df['cholesterol']>1).astype(int)
df['gluc'] = (df['gluc']>1).astype(int)

# Draw Categorical Plot
def draw_cat_plot():
  
  # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  
  df_1 = df.drop(columns=['id', 'age', 'sex', 'height', 'weight', 'ap_hi', 'ap_lo'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
  df_cat = df_1.melt(id_vars='cardio', var_name='variable', value_name = 'value')
    
    # Draw the catplot with 'sns.catplot()'

    # Get the figure for the output
  x_order = sorted(df_cat['variable'].unique())
  fig = sns.catplot(data = df_cat, x = 'variable', kind = 'count', hue = 'value', col = 'cardio', order = x_order)
  fig.set_axis_labels('variable', 'total')


    # Do not modify the next two lines
  fig.savefig('catplot.png')
  return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
      (df['ap_lo'] <= df['ap_hi']) & 
      (df['height'] >= df['height'].quantile(0.025)) &
      (df['height'] <= df['height'].quantile(0.975)) &
      (df['weight'] >= df['weight'].quantile(0.025)) &
      (df['weight'] <= df['weight'].quantile(0.975)) ]

    # Calculate the correlation matrix
    corr = df_heat.corr()
  
    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10,8))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True, fmt = '.1f', cmap = 'coolwarm', linewidth = .5, ax = ax)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig