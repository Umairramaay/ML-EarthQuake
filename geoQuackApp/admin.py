from django.contrib import admin
from datetime import datetime
import pandas as pd
import numpy as np
from geoQuackApp.models import Quake, Quake_Predictions
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

# Register your models here.

admin.site.register(Quake)
admin.site.register(Quake_Predictions)

if Quake.objects.all().count() == 0:
    # add the 1965 -2016 datasets
    df = pd.read_csv("database.csv")

    # preview df
    # print(df)

    df_load = df.drop(['Depth Error', 'Time', 'Depth Seismic Stations', 'Magnitude Error', 'Magnitude Seismic Stations', 'Azimuthal Gap', 'Horizontal Distance', 'Horizontal Error', 'Root Mean Square',
                       'Source', 'Location Source', 'Magnitude Source', 'Status'], axis=1)

    # preview drop

    # print(df_load.head())

    df_load = df_load.rename(columns={"Magnitude Type": "Magnitude_Type"})

    # Insert records to DB

    for index, row in df_load.iterrows():
        Date = row['Date']
        Latitude = row['Latitude']
        Longitude = row['Longitude']
        Type = row['Type']
        Depth = row['Depth']
        Magnitude = row['Magnitude']
        Magnitude_Type = row['Magnitude_Type']
        ID = row['ID']

        Quake(Date=Date, Latitude=Latitude, Longitude=Longitude, Type=Type,
              Depth=Depth, Magnitude=Magnitude, Magnitude_Type=Magnitude_Type, ID=ID).save()


if Quake_Predictions.objects.all().count() == 0:
    # add 2017 test data and 1965-2016 training data
    df_test = pd.read_csv(r"G:\360\Django\geodjango\UD\earthquakeTest.csv")
    df_train = pd.read_csv(r"G:\360\Django\geodjango\UD\database.csv")

    df_train_loaded = df_train.drop(['Depth Error', 'Time', 'Depth Seismic Stations', 'Magnitude Seismic Stations', 'Root Mean Square', 'Source',
                                     'Location Source', 'Magnitude Source', 'Status', 'Magnitude Error', 'Azimuthal Gap', 'Horizontal Distance', 'Horizontal Error'], axis=1)
    df_test_loaded = df_test[['time', 'latitude', 'longitude', 'mag', 'depth']]

    df_train_loaded = df_train_loaded.rename(
        columns={'Magnitude Type': 'Magnitude_Type'})
    df_test_loaded = df_test_loaded.rename(
        columns={'time': 'Date', 'latitude': 'Latitude', 'longitude': 'Longitude', 'mag': 'Magnitude', 'depth': 'Depth'})

    # Creating Training and Testing DF
    df_testing = df_test_loaded[['Latitude',
                                 'Longitude', 'Magnitude', 'Depth']]
    df_training = df_train_loaded[[
        'Latitude', 'Longitude', 'Magnitude', 'Depth']]

    # Dropping Nulls From Datasets
    df_training.dropna()
    df_testing.dropna()

    # Creating Training Features
    X = df_training[['Latitude', 'Longitude']]
    y = df_training[['Magnitude', 'Depth']]

    # Creating Testing Features

    X_new = df_testing[['Latitude', 'Longitude']]
    y_new = df_testing[['Magnitude', 'Depth']]

    # Using Train_test_split on training Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Building Model RF
    model_reg = RandomForestRegressor(random_state=50)
    model_reg.fit(X_train, y_train)
    model_reg.predict(X_test)
    score = model_reg.score(X_test, y_test) * 100

    # Improving Accuracy by Automating Hyper Parameter Tuning
    parameters = {'n_estimators': [10, 20, 50, 100, 200, 500]}

    grid_obj = GridSearchCV(model_reg, parameters)
    grid_fit = grid_obj.fit(X_train, y_train)
    best_fit = grid_fit.best_estimator_
    results = best_fit.predict(X_test)

    score = best_fit.score(X_test, y_test)*100
    # print(score)
    # Using Best Fit Model for prediction
    final_results = best_fit.predict(X_new)
    # Evaluate
    final_score = best_fit.score(X_new, y_new)*100
    # Store Pridiction Results
    lst_Magnitudes = []
    lst_Depth = []
    i = 0
    for r in final_results.tolist():
        lst_Magnitudes.append(final_results[i][0])
        lst_Depth.append(final_results[i][1])
        i += 1

    df_results = X_new[['Latitude', 'Longitude']]
    df_results['Magnitude'] = lst_Magnitudes
    df_results['Depth'] = lst_Depth
    df_results['Score'] = final_score

    for index, row in df_results.iterrows():
        Latitude = row['Latitude']
        Longitude = row['Longitude']
        Magnitude = row['Magnitude']
        Depth = row['Depth']
        Score = row['Score']

        Quake_Predictions(Latitude=Latitude, Longitude=Longitude,
                          Magnitude=Magnitude, Depth=Depth, Score=Score).save()
