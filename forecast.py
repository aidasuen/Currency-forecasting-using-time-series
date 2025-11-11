import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error

if not os.path.exists("graphs"):
    os.makedirs("graphs")

df = pd.read_excel("Курсы Валют.xlsx")  
df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
df.set_index('Date', inplace=True)


plt.figure(figsize=(10,4))
plt.plot(df['USD'])
plt.title("Курс USD к KZT")
plt.xlabel("Дата")
plt.ylabel("Курс")
plt.grid(True)
plt.savefig("graphs/course_usd.png") 
plt.close()  


train = df.iloc[:-7]
test = df.iloc[-7:]


model = ARIMA(train['USD'], order=(1,1,1))
model_fit = model.fit()


forecast = model_fit.forecast(steps=7)

plt.figure(figsize=(10,4))
plt.plot(train.index, train['USD'], label='Train')
plt.plot(test.index, test['USD'], label='Actual')
plt.plot(test.index, forecast, label='Forecast')
plt.legend()
plt.title("Прогноз курса USD на 7 дней")
plt.xlabel("Дата")
plt.ylabel("Курс")
plt.grid(True)
plt.savefig("graphs/forecast_7days.png")
plt.close()

mae = mean_absolute_error(test['USD'], forecast)
print("Средняя ошибка прогноза (MAE):", round(mae,2))

future_forecast = model_fit.forecast(steps=30)
future_dates = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=30, freq='D')

plt.figure(figsize=(10,4))
plt.plot(df.index, df['USD'], label='Исторические данные')
plt.plot(future_dates, future_forecast, label='Прогноз на 30 дней')
plt.legend()
plt.title("Прогноз курса USD на 30 дней")
plt.xlabel("Дата")
plt.ylabel("Курс")
plt.grid(True)
plt.savefig("graphs/forecast_30days.png")
plt.close()

print("Все графики сохранены в папку 'graphs'.")
