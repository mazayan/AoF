#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

def get_x_features(dataset):
    scaler = StandardScaler()
    scaler.fit(dataset.iloc[:,1:4])
    scaled_features = scaler.transform(dataset.iloc[:,1:4])
    return scaled_features

#code referenced from http://marubon-ds.blogspot.com/2017/09/knn-k-nearest-neighbors-by-tensorflow.html
def k_nearest_neighbors(reader_opioid_dataset, x_features, target_classifiers):
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

    k = 10

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
    y_vals_eval = []
    for pred, actual in zip(prediction_outcome, y_vals_test):
        print("Prediction %s, Actual %s" %(pred, np.argmax(actual)))
        y_vals_eval.append(np.argmax(actual))
        if pred == np.argmax(actual):
            print("Correct!")
            accuracy += 1


    print("Accuracy: %s" %(accuracy / len(prediction_outcome)))
    print(confusion_matrix(y_vals_eval, prediction_outcome))
    print(classification_report(y_vals_eval, prediction_outcome, target_names=target_classifiers))























