import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. DATA GENERATION (Tera Code - Optimized)
# ==========================================
print("⏳ Generating Data... Please wait.")
n = 500000 # Testing ke liye 5 Lakh theek hai. 1 Crore ke liye n = 10000000 kar dena baad me.

np.random.seed(42) # Result har baar same rahega
Dates = pd.date_range(start="2020-01-01", end="2024-12-31", freq='h')
data = {
    "date": np.random.choice(Dates, n),
    "Transaction_ID": np.arange(1, n+1),
    "Customer_ID": np.random.randint(1, 100001, n),
    "Product_Category": np.random.choice(["Electronics", "Clothing", "Home", "Beauty", "Sports"], n),
    "Payment_Mode": np.random.choice(["UPI", "Credit Card", "Debit Card", "Cash"], n),
    "City": np.random.choice(["Jaipur","Delhi","Bangalore","Pune","Hyderabad","Kolkata","Mumbai","Ahmedabad","Surat","Chennai"], n),
    "Amount": np.random.randint(100, 50001, n),
    "Status": np.random.choice(["Completed", "Refunded", "Failed"], n, p=[0.7, 0.1, 0.2])
}

df = pd.DataFrame(data)

# --- MEMORY OPTIMIZATION ---
df["Transaction_ID"] = df["Transaction_ID"].astype("int32")
df["Customer_ID"] = df["Customer_ID"].astype("int32")
df["Amount"] = df["Amount"].astype("int32")
df["Category"] = df["Product_Category"].astype("category") # String se fast hota hai
df["City"] = df["City"].astype("category")

# ==========================================
# 2. DATA ANALYSIS (Tera Logic)
# ==========================================
print("🧹 Cleaning & Analyzing Data...")

# Missing Values Simulation (Jo tune kiya tha)
df.loc[df.sample(frac=0.05).index, "Amount"] = np.nan
df["Amount"] = df["Amount"].fillna(df["Amount"].mean())

# Year Analysis
df["Year"] = df["date"].dt.year
df["Month"] = df["date"].dt.month_name()

# Insight 1: City wise Failed Transactions
total_txn = df.groupby("City", observed=False)["Status"].count()
failed_txn = df[df["Status"] == "Failed"].groupby("City", observed=False)["Status"].count()
failed_percentage = ((failed_txn / total_txn) * 100).sort_values(ascending=False)

# Insight 2: YoY Growth (2022 vs 2023)
df_filtered = df[df["Year"].isin([2022, 2023])]
pivot_table = df_filtered.pivot_table(values="Amount", index="Product_Category", columns="Year", aggfunc="sum")
pivot_table["Growth_Value"] = pivot_table[2023] - pivot_table[2022]
pivot_table["Growth_%"] = ((pivot_table[2023] - pivot_table[2022]) / pivot_table[2022]) * 100

# ==========================================
# 3. VISUALIZATION DASHBOARD (LinkedIn wala Jadoo 🎨)
# ==========================================
print("📊 Creating Dashboard...")

# Style set karna (Professional look ke liye)
sns.set_style("whitegrid")
plt.figure(figsize=(18, 10)) # Badi image banegi
plt.suptitle('Big Mart Mega Sales Analysis (500k Transactions)', fontsize=20, fontweight='bold', color='#333333')

# --- Graph 1: Revenue Share by Category (Pie Chart) ---
plt.subplot(2, 3, 1)
cat_sales = df.groupby('Product_Category')['Amount'].sum()
plt.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'), startangle=140)
plt.title('Revenue Share by Category', fontsize=12)

# --- Graph 2: Monthly Sales Trend (Line Chart) ---
plt.subplot(2, 3, 2)
monthly_trend = df.groupby(df['date'].dt.to_period('M'))['Amount'].sum()
# Sirf last 2 years ka trend dikhate hain taki graph saaf dikhe
monthly_trend.tail(24).plot(kind='line', marker='o', color='#2ecc71', linewidth=2)
plt.title('Monthly Sales Trend (Last 2 Years)', fontsize=12)
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.grid(True, linestyle='--', alpha=0.7)

# --- Graph 3: Failed Transaction Rate by City (Bar Chart) ---
plt.subplot(2, 3, 3)
sns.barplot(x=failed_percentage.index, y=failed_percentage.values, palette='Reds_r')
plt.title('High Risk Cities (Failed Txn %)', fontsize=12)
plt.xticks(rotation=45)
plt.ylabel('Failure Rate (%)')

# --- Graph 4: Payment Mode Preference (Bar Chart) ---
plt.subplot(2, 3, 4)
sns.countplot(x='Payment_Mode', data=df, palette='viridis', order=df['Payment_Mode'].value_counts().index)
plt.title('Preferred Payment Modes', fontsize=12)

# --- Graph 5: Year-Over-Year Growth % (Bar Chart) ---
plt.subplot(2, 3, 5)
sns.barplot(x=pivot_table.index, y=pivot_table['Growth_%'], palette='coolwarm')
plt.title('Category Growth (2022 vs 2023)', fontsize=12)
plt.ylabel('Growth %')
plt.axhline(0, color='black', linewidth=0.8) # Zero line

# --- Graph 6: Top 10 High Value Customers (Horizontal Bar) ---
plt.subplot(2, 3, 6)
top_cust = df.groupby('Customer_ID')['Amount'].sum().nlargest(5)
sns.barplot(x=top_cust.values, y=top_cust.index.astype(str), palette='magma')
plt.title('Top 5 Platinum Customers', fontsize=12)
plt.xlabel('Total Spent')
plt.ylabel('Customer ID')

# Layout adjust aur Save
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Big_Mart_Dashboard.png', dpi=300) # High Quality Image Save hogi
print("✅ Dashboard Saved as 'Big_Mart_Dashboard.png'")

# ==========================================
# 4. EXCEL EXPORT (Boss ke liye Report)
# ==========================================
print("💾 Saving Excel Report...")
with pd.ExcelWriter("Big_Mart_Report.xlsx") as writer:
    pivot_table.to_excel(writer, sheet_name="YoY Growth")
    failed_percentage.to_excel(writer, sheet_name="City Failure Rates")
    df.head(1000).to_excel(writer, sheet_name="Sample Data") # Pura data excel me nahi aayega, sirf sample

print("🎉 Process Complete! Check folder for Image and Excel.")
plt.show()















































































