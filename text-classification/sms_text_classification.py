# -*- coding: utf-8 -*-
"""sms_text_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tu0nS_Ghn-9mbZvEh1wPLJPaRJo0mEj7
"""

# import libraries
try:
  # %tensorflow_version only exists in Colab.
  !pip install tf-nightly
except Exception:
  pass
import tensorflow as tf
import pandas as pd
from tensorflow import keras
!pip install tensorflow-datasets
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# get data files
!wget https://cdn.freecodecamp.org/project-data/sms/train-data.tsv
!wget https://cdn.freecodecamp.org/project-data/sms/valid-data.tsv

train_file_path = "train-data.tsv"
test_file_path = "valid-data.tsv"

# Load the data into DataFrames
train_data = pd.read_csv(train_file_path, sep='\t', header=None, names=['label', 'message'])
test_data = pd.read_csv(test_file_path, sep='\t', header=None, names=['label', 'message'])

# Display the first few rows of the training data
print("Training Data:")
print(train_data)

# Display the first few rows of the test data
print("\nTest Data:")
print(test_data)

# Mapping for label encoding
label_mapping = {'ham': 0, 'spam': 1}

# Apply the mapping to both train and test data
train_data['label'] = train_data['label'].map(label_mapping)
test_data['label'] = test_data['label'].map(label_mapping)

print("Training Data:")
print(train_data)

print("\nTest Data:")
print(test_data)

tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(train_data['message'])

X_train = tokenizer.texts_to_sequences(train_data['message'])
X_test = tokenizer.texts_to_sequences(test_data['message'])

print(X_train[0])

X_train = tf.keras.preprocessing.sequence.pad_sequences(X_train)
X_test = tf.keras.preprocessing.sequence.pad_sequences(X_test, maxlen=X_train.shape[1])

model = keras.Sequential([
    keras.layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128),
    keras.layers.LSTM(128),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, train_data['label'], epochs=10, batch_size=64, validation_split=0.2)

loss, accuracy = model.evaluate(X_test, test_data['label'])
print(f"Model Accuracy: {accuracy:.2%}")

probabilities = model.predict(X_test)

# Find the maximum probability associated with the label 'spam'
max_spam_probability = np.max(probabilities[test_data['label'] == 1])

print(f"Highest Probability for 'spam' Label: {max_spam_probability:.4f}")

# Predict probabilities on the entire test set
probabilities = model.predict(X_test)

# Find the highest probability associated with the 'ham' label
max_ham_probability = np.max(probabilities[test_data['label'] == 0])

print(f"Highest Probability for 'ham' Label: {1 - max_ham_probability:.4f}")

# function to predict messages based on model
# (should return list containing prediction and label, ex. [0.008318834938108921, 'ham'])
def predict_message(pred_text):
    # Tokenize and pad the input text
    pred_seq = tokenizer.texts_to_sequences([pred_text])
    pred_seq = tf.keras.preprocessing.sequence.pad_sequences(pred_seq, maxlen=X_train.shape[1])

    # Make the prediction
    probability = model.predict(pred_seq)[0][0]

    # Convert probability to 'ham' or 'spam'
    prediction_label = 'spam' if probability >= 0.0073 else 'ham'

    return [probability, prediction_label]

pred_text = "how are you doing today?"
prediction = predict_message(pred_text)
print(prediction)

# Run this cell to test your function and model. Do not modify contents.
def test_predictions():
  test_messages = ["how are you doing today",
                   "sale today! to stop texts call 98912460324",
                   "i dont want to go. can we try it a different day? available sat",
                   "our new mobile video service is live. just install on your phone to start watching.",
                   "you have won £1000 cash! call to claim your prize.",
                   "i'll bring it tomorrow. don't forget the milk.",
                   "wow, is your arm alright. that happened to me one time too"
                  ]

  test_answers = ["ham", "spam", "ham", "spam", "spam", "ham", "ham"]
  passed = True

  for msg, ans in zip(test_messages, test_answers):
    print(msg)
    prediction = predict_message(msg)
    print("Prediction: {}".format(prediction))
    print("Actual: {}\n".format(ans))
    if prediction[1] != ans:
      passed = False

  if passed:
    print("You passed the challenge. Great job!")
  else:
    print("You haven't passed yet. Keep trying.")

test_predictions()