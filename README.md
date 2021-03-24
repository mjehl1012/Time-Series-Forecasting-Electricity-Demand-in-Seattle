# Time-Series-Forecasting-Electricity-Demand-in-Seattle
**Description**\
Great uncertainty in the electricity generation and distribution process leads to waste, resulting in higher costs for both consumers and producers of electricity. Forecasting energy use is a key step towards modernizing the grid, and my project uses linear regression to quantify the relationship between different aspects of weather and hourly electricity demand.

**Exogenous Variables and Target**\
The target variable is hourly electricity demand in megawatt-hours (MWh), "the amount of electricity generated by a one megawatt electric generator operating or producing electricity for one hour." Exogenous features for the SARIMAX model include:
* Temperature
* Day of Week (binary: 1 - weekend, 0 - weekday)

**Data Used**\
Historical hourly weather data comes from a special bulk download request through NOAA. I used the EIA API to pull in all of the hourly electricity demand data as well as the day-ahead demand forecast data used to compute the EIA forecast RMSE.

**Tools used**
* Pandas
* NumPy
* scikit-learn
* Seaborn
* Matplotlib
* statsmodels
* TBATS
* Facebook Prophet

**Possible Impacts**\
From generation to delivery to consumption, inefficiencies at every step of electricity's journy add up to a lot of waste. Our nation's electric infrastructure is aging and being pushed to do more than it was originally designed to do. Modernizing the grid through enhanced forecasting to make it "smarter" and more resilient will deliver electricity more reliably and efficiently, and can reduce peak loads and lower operational costs for utilities. My best model outperformend the EIA day-ahead demand forecast by 12MWh. Implementing my model could potentially save Seattle City Light over $1,400 per hour.