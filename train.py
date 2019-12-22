import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd

# df = pd.read_excel('usd.xls').drop('USD_quant', 1)
scaler = MinMaxScaler(feature_range=(0, 1))

# def get_rates():
#     df_usd = df['USD'].values.astype('float32').reshape(-1, 1)
#     df_usd_scaled = scaler.fit_transform(df_usd)

#     train_size = int(len(df_usd_scaled))
#     return df_usd_scaled[0:train_size,:]

def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

def train_model(X_train, Y_train, X_test, Y_test, agent):
    # try:
    model = Sequential()
    model.add(Dense(180,input_dim=X_train.shape[1]))  #input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(90, activation='relu'))
    model.add(Dense(30, activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
    mcp_save = ModelCheckpoint('.mdl_wts_%s.hdf5' % agent, save_best_only=True, monitor='val_loss', mode='min')
    model.fit(X_train, Y_train, epochs=200, batch_size=30, validation_data=(X_test, Y_test), 
                        callbacks=[earlyStopping, mcp_save], verbose=0, shuffle=False)
    model.load_weights('.mdl_wts_%s.hdf5' % agent)
    return model
    # except:
    #     return train_model(X_train, Y_train, X_test, Y_test, agent)

def create_dataset_test(dataset, look_back=1):
    X = []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
    return np.array(X)

def predict_buyer(train, agent):
    print("=== Start Predict ===")
    train = scaler.fit_transform(train)
    train_size = int(len(train) * 0.8)
    test_size = len(train) - train_size

    train, test = train[0:train_size,:], train[train_size:len(train),:]

    X_train, Y_train = create_dataset(train)
    X_test, Y_test = create_dataset(test)

    model = train_model(X_train, Y_train, X_test, Y_test, agent)

    pred_data = test[-6:]

    pred_data_scaled = create_dataset_test(pred_data)
    pred = model.predict(pred_data_scaled)
    pred = scaler.inverse_transform(pred)
    print("=== END Predict ===")
    keras.backend.clear_session() 

    return pred[0][0]