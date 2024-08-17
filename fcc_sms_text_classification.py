# -*- coding: utf-8 -*-
"""fcc_sms_text_classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CZBlqR99_UOvxPugyZ7M_gzi1cACoRpp
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

train_dataset, valid_dataset = pd.read_csv('train-data.tsv',sep='\t',header=None,names=['class', 'text']) , pd.read_csv('valid-data.tsv',sep='\t',header=None,names=['class', 'text'])
x = keras.datasets.imdb.get_word_index(path="imdb_word_index.json")
def preprocess(df):
    df['class'] = df['class'].map({'ham': 0, 'spam': 1})
    labels = df.pop('class').astype(np.float32)
    data = df['text'].tolist()
    return data, labels
train_data, train_labels = preprocess(train_dataset)
valid_data, valid_labels = preprocess(valid_dataset)
def encode_text(text):
    tokens = [x.get(word, 0) for word in keras.preprocessing.text.text_to_word_sequence(text)]
    padded_sequence = keras.preprocessing.sequence.pad_sequences([tokens], maxlen=1000, padding='post', truncating='post')
    return np.squeeze(padded_sequence)
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=100000,output_dim=64,mask_zero=True),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation="sigmoid")
])
model.compile(loss="binary_crossentropy",optimizer=tf.keras.optimizers.Adam(0.01),metrics=['accuracy'])
model.fit(x=np.array([encode_text(text) for text in train_data]),y= train_labels, epochs=8, validation_data=(np.array([encode_text(text) for text in valid_data]),valid_labels))



# function to predict messages based on model
# (should return list containing prediction and label, ex. [0.008318834938108921, 'ham'])

def predict_message(pred_text):
    outcome = model.predict((np.array([(encode_text(pred_text))])))[0][0]
    label = "spam" if outcome > 0.5 else "ham"
    return [outcome, label]

pred_text = "wow, is your arm alright. that happened to me one time too"
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
    prediction = predict_message(msg)
    if prediction[1] != ans:
      passed = False

  if passed:
    print("You passed the challenge. Great job!")
  else:
    print("You haven't passed yet. Keep trying.")

test_predictions()