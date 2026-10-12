import os
import pandas as pd

# إنشاء مجلد لحفظ الملفات النظيفة
output_dir = "cleaned_data"
os.makedirs(output_dir, exist_ok=True)

# 1. تنظيف ملف المبيعات (Sales_Transactions.csv)
try:
  df_sales = pd.read_csv("Sales_Transactions.csv")
  df_sales = df_sales.drop_duplicates()
  df_sales.fillna(
      {
          "Gross_Sales_EGP": 0,
          "Net_Sales_EGP": 0,
          "Gross_Profit_EGP": 0,
          "Quantity": 0,
      },
      inplace=True,
  )
  df_sales.to_csv(
      os.path.join(output_dir, "Sales_Transactions_Cleaned.csv"), index=False
  )
  print("تم تنظيف وحفظ: Sales_Transactions.csv")
except Exception as e:
  print("خطأ في Sales_Transactions:", e)

# 2. تنظيف ملف العملاء (Customers.csv)
try:
  df_customers = pd.read_csv("Customers.csv")
  df_customers = df_customers.drop_duplicates()
  df_customers.to_csv(
      os.path.join(output_dir, "Customers_Cleaned.csv"), index=False
  )
  print("تم تنظيف وحفظ: Customers.csv")
except Exception as e:
  print("خطأ في Customers:", e)

# 3. تنظيف ملف تاريخ المخزون (Inventory_History.csv)
try:
  df_inv = pd.read_csv("Inventory_History.csv")
  df_inv = df_inv.drop_duplicates()
  df_inv["Snapshot_Month"] = pd.to_datetime(
      df_inv["Snapshot_Month"], errors="coerce"
  )
  df_inv.fillna(0, inplace=True)
  df_inv.to_csv(
      os.path.join(output_dir, "Inventory_History_Cleaned.csv"), index=False
  )
  print("تم تنظيف وحفظ: Inventory_History.csv")
except Exception as e:
  print("خطأ في Inventory_History:", e)

# 4. تنظيف ملف الحملات التسويقية (Marketing.csv)
try:
  df_mkt = pd.read_csv("Marketing.csv")
  df_mkt = df_mkt.drop_duplicates()
  df_mkt["Start_Date"] = pd.to_datetime(df_mkt["Start_Date"], errors="coerce")
  df_mkt["End_Date"] = pd.to_datetime(df_mkt["End_Date"], errors="coerce")
  df_mkt.fillna(
      {"Spend_EGP": 0, "Impressions": 0, "Clicks": 0, "Attributed_Revenue_EGP": 0},
      inplace=True,
  )
  df_mkt.to_csv(os.path.join(output_dir, "Marketing_Cleaned.csv"), index=False)
  print("تم تنظيف وحفظ: Marketing.csv")
except Exception as e:
  print("خطأ في Marketing:", e)

# 5. تنظيف ملف أوامر الإنتاج (Production_Orders.csv)
try:
  df_prod = pd.read_csv("Production_Orders.csv")
  df_prod = df_prod.drop_duplicates()
  df_prod["Start_Date"] = pd.to_datetime(df_prod["Start_Date"], errors="coerce")
  df_prod["Due_Date"] = pd.to_datetime(df_prod["Due_Date"], errors="coerce")
  df_prod["Completion_Date"] = pd.to_datetime(
      df_prod["Completion_Date"], errors="coerce"
  )
  df_prod["Primary_Bottleneck"].fillna("None", inplace=True)
  df_prod.to_csv(
      os.path.join(output_dir, "Production_Orders_Cleaned.csv"), index=False
  )
  print("تم تنظيف وحفظ: Production_Orders.csv")
except Exception as e:
  print("خطأ في Production_Orders:", e)

# 6. تنظيف ملف أوامر الشراء (Purchase_Orders.csv)
try:
  df_po = pd.read_csv("Purchase_Orders.csv")
  df_po = df_po.drop_duplicates()
  df_po["Order_Date"] = pd.to_datetime(df_po["Order_Date"], errors="coerce")
  df_po["Promised_Date"] = pd.to_datetime(
      df_po["Promised_Date"], errors="coerce"
  )
  df_po["Actual_Receipt_Date"] = pd.to_datetime(
      df_po["Actual_Receipt_Date"], errors="coerce"
  )
  df_po.to_csv(
      os.path.join(output_dir, "Purchase_Orders_Cleaned.csv"), index=False
  )
  print("تم تنظيف وحفظ: Purchase_Orders.csv")
except Exception as e:
  print("خطأ في Purchase_Orders:", e)

# 7. تنظيف ملف خدمة العملاء (Customer_Service.csv)
try:
  df_cs = pd.read_csv("Customer_Service.csv")
  df_cs = df_cs.drop_duplicates()
  df_cs["Open_Date"] = pd.to_datetime(df_cs["Open_Date"], errors="coerce")
  df_cs.fillna({"CSAT_1_to_5": df_cs["CSAT_1_to_5"].mean()}, inplace=True)
  df_cs.to_csv(
      os.path.join(output_dir, "Customer_Service_Cleaned.csv"), index=False
  )
  print("تم تنظيف وحفظ: Customer_Service.csv")
except Exception as e:
  print("خطأ في Customer_Service:", e)

# 8. تنظيف ملف حركة الموقع (Web_Traffic_Daily.csv)
try:
  df_web = pd.read_csv("Web_Traffic_Daily.csv")
  df_web = df_web.drop_duplicates()
  df_web["Date"] = pd.to_datetime(df_web["Date"], errors="coerce")
  df_web.fillna(0, inplace=True)
  df_web.to_csv(
      os.path.join(output_dir, "Web_Traffic_Daily_Cleaned.csv"), index=False
  )
  print("تم تنظيف وحفظ: Web_Traffic_Daily.csv")
except Exception as e:
  print("خطأ في Web_Traffic_Daily:", e)

print(
    "\n🎉 تم الانتهاء من تنظيف كافة الملفات وحفظها في مجلد باسم: 'cleaned_data'"
)