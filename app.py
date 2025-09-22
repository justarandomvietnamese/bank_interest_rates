import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df_melted = pd.read_excel('/content/drive/MyDrive/KIS/Lãi suất gửi tiết kiệm.xlsx', header=1, skiprows=[0])
df_melted.columns = df_melted.columns.str.strip()

# Melt the dataframe to long format
df_melted = df_melted.melt(id_vars=['BANK', 'CHANNEL', 'PRODUCT', 'CUSTOMERTYPE', 'NOTE'],
                           value_vars=['1M(%)', '3M(%)', '6M(%)', '9M(%)', '12M(%)'],
                           var_name='Term', value_name='Interest Rate (%)')

# Convert 'Term' to a categorical type for correct ordering in the plot
df_melted['Term'] = pd.Categorical(df_melted['Term'], categories=['1M(%)', '3M(%)', '6M(%)', '9M(%)', '12M(%)'], ordered=True)

# Fill missing values in 'Interest Rate (%)' with 0 or another appropriate value if needed
df_melted['Interest Rate (%)'] = df_melted['Interest Rate (%)'].fillna(0)

# Replace 'SMEs' with 'CORPORATE' in the CUSTOMERTYPE column
df_melted['CUSTOMERTYPE'] = df_melted['CUSTOMERTYPE'].replace('SMEs', 'CORPORATE')


st.title("Interactive Interest Rate Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")
selected_banks = st.sidebar.multiselect("Select Banks", df_melted['BANK'].unique(), df_melted['BANK'].unique())
selected_channels = st.sidebar.multiselect("Select Channels", df_melted['CHANNEL'].unique(), df_melted['CHANNEL'].unique())
selected_customer_types = st.sidebar.multiselect("Select Customer Types", df_melted['CUSTOMERTYPE'].unique(), df_melted['CUSTOMERTYPE'].unique())
selected_terms = st.sidebar.multiselect("Select Terms", df_melted['Term'].unique(), df_melted['Term'].unique())

# Filter data based on selections
filtered_df = df_melted[
    (df_melted['BANK'].isin(selected_banks)) &
    (df_melted['CHANNEL'].isin(selected_channels)) &
    (df_melted['CUSTOMERTYPE'].isin(selected_customer_types)) &
    (df_melted['Term'].isin(selected_terms))
]

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Plotting
st.subheader("Interest Rates by Bank and Term")

if not filtered_df.empty:
    plt.figure(figsize=(15, 8))
    sns.barplot(x='BANK', y='Interest Rate (%)', hue='Term', data=filtered_df, errorbar=None)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.title("Interest Rates by Bank and Term", fontsize=16)
    plt.xlabel("Bank", fontsize=12)
    plt.ylabel("Interest Rate (%)", fontsize=12)
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.legend(title="Term", bbox_to_anchor=(1.05, 1), loc='upper left', title_fontsize=12, fontsize=10)

    # Add numerical labels on top of bars
    for container in plt.gca().containers:
        plt.bar_label(container, fmt='%.2f', fontsize=8)

    st.pyplot(plt)
else:
    st.warning("No data to display for the selected filters.")
