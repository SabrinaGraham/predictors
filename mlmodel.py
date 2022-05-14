'''
This is a multiple linear regression model to predit the crime rate for parish divisions
Dataset:
crimerates.csv, which contains the relevant crime data and features for each division. This includes
information by parish, type of crime, crime rate by division etc.
'''


import pandas as pd 

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import pickle


# Importing the dataset
df = pd.read_csv('crimerates.csv', encoding='latin-1')


#Take a look at all the dataset features
# df.head()


#Get required features for data training
cdf = df[['CRIME_RATE_BY_DIVISION','MONTH','CRIME_TYPE', 'DIVISION']]
cdf['CRIME_TYPE'] = cdf['CRIME_TYPE'].replace(['Aggravated Assault','Larceny/Theft','Murder','Rape','Robbery'],[1,2,3,4,5])
cdf['MONTH'] = cdf['MONTH'].replace(['January','February','March','April','May','June','July','August','September','October','November','December'],[1,2,3,4,5,6,7,8,9,10,11,12])

#Use dummy varibales for categorical variables 
dummies = pd.get_dummies(cdf, prefix='', prefix_sep='', columns=['DIVISION'], drop_first=True)

#crime rate by division - independent value 
X = dummies.iloc[:, 1:].values 

#divisions - dependent values
y = dummies.iloc[:, 0].values 

#splitting the dataset into training and test set
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size= 0.2, random_state=0) 


reg = LinearRegression() 
#Fitting model with trainig data
reg.fit(X_train, y_train)

# Pickle serializes objects so they can be saved to a file, and loaded in a program again later on.
pickle.dump(reg, open('model.pkl','wb'))

'''
# Prediction tester
model = pickle.load(open('model.pkl','rb'))
new = model.predict([[1,3,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
print(new)
'''