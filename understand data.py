import pandas as pd

# ضبط إعدادات العرض في البايثون عشان الكلام يظهر كامل
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 1000)

# قراءة وطباعة Case_Briefs.csv بالكامل
df_briefs = pd.read_csv("Case_Briefs.csv")
print("--- ALL CASE BRIEFS & TASKS ---")
for index, row in df_briefs.iterrows():
  print(f"\nCard / Brief {index + 1}:")
  print(row.to_string())
  print("-" * 50)

print ("################################################################")

# قراءة ملف المبيعات
df_sales = pd.read_csv("Sales_Transactions.csv")

print("--- معاينة بيانات المبيعات ---")
print(df_sales.head())

# حساب إجمالي الإيرادات وإجمالي الكميات المباعة
if "Revenue" in df_sales.columns and "Quantity" in df_sales.columns:
  total_revenue = df_sales["Revenue"].sum()
  total_units = df_sales["Quantity"].sum()
  print(f"\nإجمالي الإيرادات الكلية: {total_revenue}")
  print(f"إجمالي الوحدات المباعة: {total_units}")
else:
  print(
      "\nالأعمدة المطلوبة (مثل Revenue أو Quantity) تحتاج للتأكد من أسمائها"
      " الدقيقة في ملف Data_Dictionary."
  )