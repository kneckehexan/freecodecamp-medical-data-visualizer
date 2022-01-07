import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

df['id'] = pd.to_numeric(df['id'], downcast='unsigned')
df['age'] = pd.to_numeric(df['age'], downcast='unsigned')
df['gender'] = pd.to_numeric(df['gender'], downcast='unsigned')
df['height'] = pd.to_numeric(df['height'], downcast='unsigned')
df['weight'] = pd.to_numeric(df['weight'], downcast='float')
df['ap_hi'] = pd.to_numeric(df['ap_hi'], downcast='unsigned')
df['ap_lo'] = pd.to_numeric(df['ap_lo'], downcast='unsigned')
df['cholesterol'] = pd.to_numeric(df['cholesterol'], downcast='unsigned')
df['gluc'] = pd.to_numeric(df['gluc'], downcast='unsigned')
df['smoke'] = pd.to_numeric(df['smoke'], downcast='unsigned')
df['alco'] = pd.to_numeric(df['alco'], downcast='unsigned')
df['active'] = pd.to_numeric(df['active'], downcast='unsigned')
df['cardio'] = pd.to_numeric(df['cardio'], downcast='unsigned')

dtypes = df.dtypes
colnames = dtypes.index
types = [i.name for i in dtypes.values]
column_types = dict(zip(colnames, types))

df = pd.read_csv('medical_examination.csv', dtype=column_types)

df.set_index('id')

# Add 'overweight' column
tmp = df['weight'].div(((df['height'])/100)**2)
df['overweight'] = [0 if x <= 25 else 1 for x in tmp]

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = [0 if x == 1 else 1 for x in df['cholesterol']]
df['gluc'] = [0 if x == 1 else 1 for x in df['gluc']]


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    # This part doesn't work correctly. Solution valid with next part though.
    #df_cat['total'] = 1
    #df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).count()

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data=df_cat, kind='count', x='variable', hue='value', col='cardio').set_axis_labels('variable', 'total').fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[
        (df['ap_lo'] <= df['ap_hi']) & 
        (df['height'] >= df['height'].quantile(0.025)) & 
        (df['height'] <= df['height'].quantile(0.975)) & 
        (df['weight'] >= df['weight'].quantile(0.025)) & 
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)


    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11,9))

    plt.subplots_adjust(left=0.1, bottom=0.1)

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, fmt='.1f', annot=True, mask=mask)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
