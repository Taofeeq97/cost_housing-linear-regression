import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
desired_width=320

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns',7)
df_cost_revenue_dirty=pd.read_csv("cost_revenue_dirty.csv")
shape=df_cost_revenue_dirty.shape
print(shape)
print(df_cost_revenue_dirty)
nan_input=df_cost_revenue_dirty.isna()
print(nan_input)
duplicated_row=df_cost_revenue_dirty[df_cost_revenue_dirty.duplicated()]
print(duplicated_row)
data_info=df_cost_revenue_dirty.info()
print(data_info)

chars_to_remove = [',', '$']
columns_to_clean = ['USD_Production_Budget',
                    'USD_Worldwide_Gross',
                    'USD_Domestic_Gross']

for col in columns_to_clean:
    for char in chars_to_remove:
        # Replace each character with an empty string
        df_cost_revenue_dirty[col] = df_cost_revenue_dirty[col].astype(str).str.replace(char, "")
    # Convert column to a numeric data type
    df_cost_revenue_dirty[col] = pd.to_numeric(df_cost_revenue_dirty[col])
print(f'this is the new dataset{df_cost_revenue_dirty}')

new_data_info=df_cost_revenue_dirty.info()
print(new_data_info)

df_cost_revenue_dirty.Release_Date=pd.to_datetime(df_cost_revenue_dirty.Release_Date)
print(df_cost_revenue_dirty)
describe_data=df_cost_revenue_dirty.describe()
print(describe_data)

lowest_budgetfilm=df_cost_revenue_dirty[df_cost_revenue_dirty.USD_Production_Budget==1100]
print(lowest_budgetfilm)

zero_gross_domestically=df_cost_revenue_dirty[df_cost_revenue_dirty.USD_Domestic_Gross==0]
print(f'Number of films that grossed domesticalled at $0 is : {len(zero_gross_domestically)}')
z_g=zero_gross_domestically.sort_values("USD_Production_Budget", ascending=False)
print(z_g)

international_release=df_cost_revenue_dirty.loc[(df_cost_revenue_dirty.USD_Domestic_Gross==0)&
                                                (df_cost_revenue_dirty.USD_Worldwide_Gross!=0)]
print(f'the number of international release is : {len(international_release)}')
print(international_release)

scrape_date=pd.Timestamp("2018-05-01")
future_release=df_cost_revenue_dirty[df_cost_revenue_dirty.Release_Date >= scrape_date]
print(f"Number of unreleased films is : {len(future_release)}")
print(future_release)
clean_new_df=df_cost_revenue_dirty.drop(future_release.index)
print(clean_new_df)
money_losing=clean_new_df.loc[clean_new_df.USD_Production_Budget > clean_new_df.USD_Worldwide_Gross]
lost_money_movies=len(money_losing)/len(clean_new_df)*100
print(f'percentage film that recorded loss in revenue is : {lost_money_movies} %')
plt.figure(figsize=(8,4),dpi=200)
with sns.axes_style('darkgrid'):
    ax=sns.scatterplot(data=clean_new_df,
                x="USD_Production_Budget",
                y="USD_Worldwide_Gross",
                hue='USD_Worldwide_Gross',
                size='USD_Worldwide_Gross',)

    ax.set(ylim=(0, 3000000000),
       xlim=(0, 450000000),
       ylabel='Revenue in $ billions',
       xlabel='Budget in $100 millions')

#plt.show()

plt.figure(figsize=(8,4),dpi=200)
with sns.axes_style('darkgrid'):
    ax=sns.scatterplot(data=clean_new_df,
                x="Release_Date",
                y="USD_Production_Budget",
                hue='USD_Worldwide_Gross',
                size='USD_Worldwide_Gross',)

    ax.set(ylim=(0, 450000000),
       xlim=(clean_new_df.Release_Date.min(), clean_new_df.Release_Date.max()),
       ylabel='Budget in $100 millions',
       xlabel='Year')

#plt.show()
dt_index = pd.DatetimeIndex(clean_new_df.Release_Date)
years = dt_index.year

decades = years//10*10
clean_new_df['Decade'] = decades
hello=clean_new_df.info()
old_films=clean_new_df[clean_new_df.Decade<=1960]
new_films=clean_new_df[clean_new_df.Decade>=1960]

plt.figure(figsize=(8, 4), dpi=200)
with sns.axes_style('darkgrid'):
    ax = sns.regplot(data=new_films,
                     x='USD_Production_Budget',
                     y='USD_Worldwide_Gross',
                     color='#2f4b7c',
                     scatter_kws={'alpha': 0.3},
                     line_kws={'color': '#ff7c43'})

    ax.set(ylim=(0, 3000000000),
           xlim=(0, 450000000),
           ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions')

#plt.show()
regression = LinearRegression()
X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])

y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])
regression.fit(X, y)
intercept=regression.intercept_
print(intercept)
coef=regression.coef_
print(coef)

print("fpr old films")
X = pd.DataFrame(old_films, columns=['USD_Production_Budget'])

y = pd.DataFrame(old_films, columns=['USD_Worldwide_Gross'])
regression.fit(X, y)
intercept=regression.intercept_
print(f"the intercept is: {intercept}")
coef=regression.coef_
print(f' the slope coefficient is: {coef}')
print(f'the r=square is: {regression.score(X, y)}')