![Spotify_Logo_CMYK_Green](https://github.com/mohamedmosaed/IoT_Fitbit_analysis/blob/main/image/Fitbit-Logo-2007.jpg)
# Fitbit Data Analysis
***What is Fitbit?
A Fitbit is an activity tracker worn on the wrist just like a watch, that tracks our day-to-day activity, whether we walk, run, swim, cycle or work out at the gym.***

The goal of this project is to analyze the data come form Fitbit device and show the user his activitu rate.

# **Dashboard Image**
![Dashboard](https://github.com/mohamedmosaed/IoT_Fitbit_analysis/blob/main/image/Screenshot%202022-03-02%20150946.png)

# Methods
Data was collected via kaggle from this **[link](https://www.kaggle.com/mjazzy/fitbit-fitness-bellabeat-high-tech-company)**.

# Libraries used:
Pandas,
Numpy,
pandas_profiling,
random,
matplotlib.pyplot,
seaborn,
statsmodels,
Sklearn



Initiate Linear Regression Estimator
```sh
# Instantiate Linear Regressions 
linearRegressionModel = make_pipeline(
    MinMaxScaler(),
    SimpleImputer(strategy='mean'),
    LinearRegression())

# fit the model
linearRegressionModel.fit(X_train,y_train)
```


Initiate Ridge Estimator
```sh
# Instantiate Ridge 
model_ridge = make_pipeline(
    MinMaxScaler(),
    SimpleImputer(strategy='mean'),
    Ridge())

# fit the model
model_ridge.fit(X_train, y_train)
```

Initiate Random Forest Regressor Estimator
```sh
# Instantiate RandomForestRegressor 
model_forest = make_pipeline(
    MinMaxScaler(),
    SimpleImputer(strategy='mean'),
    RandomForestRegressor(random_state=42, n_jobs=-1))

# fit the model
model_forest.fit(X_train, y_train)
```
Initiate Random Forest Classifier
```sh
# Instantiate RandomForestRegressor 
model_forest_class =make_pipeline(
    OneHotEncoder(),
    MinMaxScaler(),
    RandomForestClassifier(n_jobs=-1,
                           random_state=42)
)

# fit the model
model_forest_class.fit(X_train, y_train)
```
# License
***MIT License***

Copyright (c) 2021 Fadil Shaikh, Jafar Sakha, Mikayla Kosmala, Mohamed Mosaed, Royce Roberts

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
