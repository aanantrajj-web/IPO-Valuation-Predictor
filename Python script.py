import pandas as pd
from sklearn.linear_model import LinearRegression
# Use your actual Windows username 'anant'
# (Make sure 'IPO History.xlsx' is actually saved inside your Downloads folder!)
my_data = pd.read_excel(r"C:\Users\anant\Downloads\IPO History.xlsx")
# 2. Train the AI Brain
X = my_data[['Revenue Growth %', 'Current Year EBITDA ($M)', 'Readiness Score (out of
100)']]
y = my_data['Final IPO Price']
ai_brain = LinearRegression()
ai_brain.fit(X, y)
# 3. Create predictions
my_data['Predicted_IPO_Price'] = ai_brain.predict(X)