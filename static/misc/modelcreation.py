import pandas as pd
import numpy as np
import joblib
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

#importing the data and selecting the row
data=pd.read_csv('rice.csv')

#drop column that are not important
cols_to_drop=['state_name','crop_year','season','crop']
data=data.drop(cols_to_drop,axis=1)

#add dummy value if any production value is missing
data.production=data.production.fillna(0)

#convert categorical value to binary
#create dummy column for the column you want to convert, concatenate to the datafreame and drop the extinct column
districnamedummy=pd.get_dummies(data['district_name'])
data=pd.concat((data,districnamedummy),axis=1)
data=data.drop(['district_name'],axis=1)

#clean data
x=data.values#input column
y=data['production'].values#output column
x=np.delete(x,4,axis=1)#delete column that is not important

# Using Skicit-learn to split data into training and testing sets
# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

#random forest regressor
rf_rg=RandomForestRegressor(n_estimators=4000,random_state=0)
rf_rg.fit(x_train,y_train)

#model creation
joblib.dump(rf_rg,'model')