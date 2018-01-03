#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
#from pylab import *
#import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def get_x_features(dataset):
    scaler = StandardScaler()
    scaler.fit(dataset.iloc[:,1:3])
    scaled_features = scaler.transform(dataset.iloc[:,1:3])
    return scaled_features

#code referenced from http://marubon-ds.blogspot.com/2017/09/knn-k-nearest-neighbors-by-tensorflow.html
def k_nearest_neighbors(reader_opioid_dataset, x_features):
    x_vals = x_features
    y_vals = reader_opioid_dataset['Opioid Type']

    #one hot encoding
    y_vals = np.eye(len(set(y_vals)))[y_vals]

    #normalize
    x_vals = (x_vals - x_vals.min(0)) / x_vals.ptp(0)

    #train-test-split
    np.random.seed(59)
    train_indices = np.random.choice(len(x_vals), int(round(len(x_vals) * 0.8)), replace=False)
    test_indices = np.array(list(set(range(len(x_vals))) - set(train_indices)))

    x_vals_train = x_vals[train_indices]
    x_vals_test = x_vals[test_indices]
    y_vals_train = y_vals[train_indices]
    y_vals_test = y_vals[test_indices]

    feature_number = len(x_vals_train[0])

    k = 5

    x_data_train = tf.placeholder(shape=[None, feature_number], dtype=tf.float32)
    y_data_train = tf.placeholder(shape=[None, len(y_vals[0])], dtype=tf.float32)
    x_data_test = tf.placeholder(shape=[None, feature_number], dtype=tf.float32)

    #manhattan distance
    distance = tf.reduce_sum(tf.abs(tf.subtract(x_data_train, tf.expand_dims(x_data_test, 1))), axis=2)

    #nearest k points
    _, top_k_indices = tf.nn.top_k(tf.negative(distance), k=k)
    top_k_label = tf.gather(y_data_train, top_k_indices)

    sum_up_predictions = tf.reduce_sum(top_k_label, axis=1)
    prediction = tf.argmax(sum_up_predictions, axis=1)

    sess = tf.Session()
    prediction_outcome = sess.run(prediction, feed_dict={x_data_train: x_vals_train,
                                                        x_data_test: x_vals_test,
                                                        y_data_train: y_vals_train})

    #evaluation
    accuracy = 0
    for pred, actual in zip(prediction_outcome, y_vals_test):
        print("Prediction %s, Actual %s" %(pred, np.argmax(actual)))
        if pred == np.argmax(actual):
            print("Correct!")
            accuracy += 1

    print("Accuracy: %s" %(accuracy / len(prediction_outcome)))


#code referenced from https://github.com/mlucchini/python-for-data-science-and-machine-learning-bootcamp/blob/master/Machine%20Learning%20Sections/K-Nearest-Neighbors/K%20Nearest%20Neighbors%20with%20Python.ipynb
def knn(reader_opioid_dataset, x_features):
    X_train, X_test, y_train, y_test = train_test_split(x_features, reader_opioid_dataset['Opioid Type'], test_size=0.3)
    knn = KNeighborsClassifier(n_neighbors=35) #K value
    knn.fit(X_train, y_train)
    pred = knn.predict(X_test)
    print(classification_report(y_test, pred))

    error_rate = []
    for i in range(1,40):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(X_train, y_train)
        pred_i = knn.predict(X_test)
        error_rate.append(np.mean(pred_i != y_test))

    #plt.figure(figsize=(10,6))
    #plt.plot(range(1,40), error_rate, color='blue', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10)
    #plt.title('Error Rate vs. K Value')
    #plt.xlabel('K')
    #plt.ylabel('Error Rate')
    #plt.show()






















