import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Membuat sebuah dataset function to get all order by category
def create_sum_orders_category_df (df):
    sum_orders_category_df = df.groupby(by="product_category_name_english").agg({
        "order_item_id": "sum",
    })
    return sum_orders_category_df

def create_daily_transaction_happen(df):
    daily_transaction_happen_df = df.resample(rule='D', on='shipping_limit_date').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_transaction_happen_df = daily_transaction_happen_df.reset_index()
    daily_transaction_happen_df.rename(columns={
        "shipping_limit_date": "day",
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return daily_transaction_happen_df

# Memasukan data yang akan diolah
all_df = pd.read_csv("all_data.csv")

# Mengubah kolom tersebut menjadi datetime
all_df["shipping_limit_date"]= pd.to_datetime(all_df["shipping_limit_date"])

#Membuat limit tanggal min dan max
min_date = all_df["shipping_limit_date"].min()
max_date = all_df["shipping_limit_date"].max()

# Membuat sidebar memakai streamlit
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://api.megabuild.co.id/storage/canvas/images/9V4V6LUQgEQfkiznFMRUT0tGCnikrm0HpnJTH5NI.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["shipping_limit_date"] >= str(start_date)) & 
                (all_df["shipping_limit_date"] <= str(end_date))]

daily_trasanction_happen_df = create_daily_transaction_happen(main_df)
sum_orders_category_df = create_sum_orders_category_df(main_df)

st.header('Analisis Sebuah E-commerce :sparkles:')

# Memasukan sub header dan isinya
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_trasanction_happen_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = daily_trasanction_happen_df.revenue.sum() 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_trasanction_happen_df["day"],
    daily_trasanction_happen_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#18a31c"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Tabel jenis barang yang laku dan tidak laku
st.subheader("Jenis Produk yang laku")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#1044ad", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_orders_category_df.sort_values(by="order_item_id", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_orders_category_df.sort_values(by="order_item_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)





