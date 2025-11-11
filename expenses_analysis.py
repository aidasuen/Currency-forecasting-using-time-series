import pandas as pd
import matplotlib.pyplot as plt
import os

output_folder = "graphs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df = pd.read_excel("Курсы валют.xlsx")

df.columns = ['Date', 'USD_quant', 'USD']

df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

df['Month'] = df['Date'].dt.month_name()
df['Year'] = df['Date'].dt.year
df['Change_%'] = df['USD'].pct_change() * 100 


df.to_excel("usd_kzt_clean.xlsx", index=False)

print("Средний курс USD/KZT за период:", df['USD'].mean())
print("Максимальный курс:", df['USD'].max())
print("Минимальный курс:", df['USD'].min())


plt.figure(figsize=(12,6))
plt.plot(df['Date'], df['USD'], color='blue', label='USD/KZT')
plt.title('Динамика курса USD/KZT за год')
plt.xlabel('Дата')
plt.ylabel('Курс')
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(output_folder, "usd_trend.png"))
plt.close()

df['Change_%_MA'] = df['Change_%'].rolling(window=7).mean() 

plt.figure(figsize=(12,6))
plt.plot(df['Date'], df['Change_%_MA'], color='red', label='Изменение курса (7-дн. среднее)')
plt.axhline(0, color='gray', linestyle='--')
plt.title('Сглаженное изменение курса USD/KZT (%)')
plt.xlabel('Дата')
plt.ylabel('Изменение, %')
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(output_folder, "usd_change_percent_smooth.png"))
plt.close()

monthly_avg = df.groupby(df['Date'].dt.month)['USD'].mean()
months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_avg.index = months_order

plt.figure(figsize=(12,6))
plt.plot(monthly_avg.index, monthly_avg.values, marker='o', linestyle='-', color='green', label='Средний курс')
plt.title('Средний курс USD/KZT по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Средний курс')
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(output_folder, "usd_monthly_avg_line.png"))
plt.close()


print(f"Все графики сохранены в папке '{output_folder}'")
