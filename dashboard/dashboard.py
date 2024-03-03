import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import calendar

# Assuming 'orders_merge' is your DataFrame
orders_merge = pd.read_csv("./dashboard/all_data.csv")

st.title('Interactive Data Analysis Project')
st.subheader('E-Commerce Public Dataset in Brazil')

st.sidebar.header('Salma Mardhiyah')

# Load example image
example_image = "https://freeimage.host/i/JMPtJJp"

# Display image in the sidebar
st.sidebar.image(example_image, use_column_width=True)
num_of_products = st.sidebar.slider("Select the number of products to display", min_value=1, max_value=20, value=10)
st.sidebar.subheader('Data Appear Parameter')
year = st.sidebar.multiselect('Select year', ['2017', '2018'], ['2017', '2018'])

# Corrected usage of st.tabs
tab1, tab2, tab3, tab4 = st.tabs(["Year Income", "Payments Type", "Hottest Products", "Unpopular Products"])

with tab1:
    st.markdown('### Bar Chart\n')

    # Sidebar for filtering data
    selected_years = [int(y) for y in year]

    # Filter data for the years 2017 and 2018 up to August
    income_2017_2018 = orders_merge[(orders_merge['year'].isin(selected_years)) & (orders_merge['month'].astype(int) <= 8)]

    # Calculate total income per month and year for the Bar Chart
    monthly_income_2017_2018_august = income_2017_2018.groupby(['year', 'month'])['payment_value'].sum().reset_index()
    monthly_income_2017_2018_august['month'] = monthly_income_2017_2018_august['month'].astype(int).apply(lambda x: calendar.month_abbr[x])

    # Create a Clustered Bar Chart
    bar_chart_fig, bar_chart_ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='month', y='payment_value', hue='year', data=monthly_income_2017_2018_august, palette=['#5c9cbf', '#0a2d7d'])
    plt.title('Total Income per Month in the Years 2017-2018 (Up to August)')
    plt.legend(title='Year')
    st.pyplot(bar_chart_fig)

    with st.expander("See explanation"):
        st.write(
        """From the graph above, it is shown that income from 2017 to 2018 has 
        increased, where the biggest difference is seen in January. Of overall income, 
        2018 experienced an increase of 19.75 from 2017. However, in 2017 it 
        tended to increase every month while 2018 tended to be stagnant and decreased slightly
        """ )

with tab2:
    st.markdown('### Pie Chart')
    payment_type = orders_merge.groupby(by="payment_type")["order_id"].nunique().reset_index()

    fig = px.pie(payment_type, values='order_id', names='payment_type', title='',
                color_discrete_sequence=px.colors.qualitative.Set1)

    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # Mengatur margin untuk mengurangi ruang kosong di sekitar gambar
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    
    # Menambahkan judul di atas dan di tengah pie chart
    fig.update_layout(title=dict(text='Payment Type Distribution', x=0, y=1, xanchor='left',  pad=dict(b=30)))
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    st.plotly_chart(fig)

    with st.expander("See explanation"):
        st.write(
        """Credit cards are the type of payment most often chosen by customers 
        when making payment transactions with 74.5% compared 
        to boleto which is only 20% followed by vouchers and debit cards at 3.9% and 1.6%
        """ )


with tab3:
    st.markdown("### Hottest Products")

    # Top 10 categories with the highest number of sales
    top_product_category = orders_merge.groupby(by="product_category_name_english").order_id.nunique().sort_values(ascending=False)
    highest_index = top_product_category.idxmax()
    

    # Plot the top categories
    st.markdown(f"##### Top {num_of_products} Product Categories with the Highest Sales:")
    colors = ["blue"] + ['lightgrey'] * (num_of_products - 1)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=top_product_category.head(num_of_products).values, y=top_product_category.head(num_of_products).index, palette=colors, orient="h", dodge=False, ax=ax)
    ax.set_xlabel("Number of Sales")
    ax.set_ylabel("product_category_name_english", labelpad=20)
    st.pyplot(fig)

    # Display the top products
    top_table = top_product_category.reset_index().head(num_of_products).reset_index(drop=True)
    st.table(top_table.style.set_properties(**{'text-align': 'right'}))


with tab4:
    st.markdown("### Unpopular Products")

    # Top 10 categories with the lowest number of sales
    lowest_product_category = orders_merge.groupby(by="product_category_name_english").order_id.nunique().sort_values(ascending=True)
    lowest_index = lowest_product_category.idxmin()

    # Plot the bottom categories
    st.markdown(f"##### Top {num_of_products} Product Categories with the Lowest Sales:")
    colors = ['lightgrey'] * (num_of_products - 1) + ["blue"]
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=lowest_product_category.head(num_of_products).values[::-1], y=lowest_product_category.head(num_of_products).index[::-1], palette=colors, orient="h", dodge=False, ax=ax)
    ax.set_xlabel("Number of Sales")
    ax.set_ylabel("product_category_name_english", labelpad=20)
    st.pyplot(fig)

    lowest_table = lowest_product_category.reset_index().head(num_of_products).reset_index(drop=True)
    st.table(lowest_table.style.set_properties(**{'text-align': 'right'}))
