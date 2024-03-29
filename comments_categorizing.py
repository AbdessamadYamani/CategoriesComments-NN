# -*- coding: utf-8 -*-
"""Comments-Categorizing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LiuX9HGQjjn_kL-LygpzbQYvgD0-teVB
"""

import pandas as pd
import numpy as np
import string
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv('CommentsSheet.csv', header=None)
comments = data[0]
categories = data[1]

# Convert categories to numerical values
encoder = LabelEncoder()
categories = encoder.fit_transform(categories)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(comments, categories, test_size=0.2)

# Tokenize comments
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

# Pad sequences
maxlen = 100
X_train = tf.keras.preprocessing.sequence.pad_sequences(X_train, padding='post', maxlen=maxlen)
X_test = tf.keras.preprocessing.sequence.pad_sequences(X_test, padding='post', maxlen=maxlen)

# Create model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=10000, output_dim=64, input_length=maxlen),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(encoder.classes_), activation='softmax')
])

# Compile model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Check if there's a saved model, if not, train and save the model
try:
    model = tf.keras.models.load_model('saved_model')
except:
    # Train model
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
    # Save model
    model.save('saved_model')

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)
print('Accuracy:', accuracy)

# Classify new comment
new_comment = input("Enter your comment: ")
new_comment = new_comment.lower().translate(str.maketrans("", "", string.punctuation))
new_comment = tokenizer.texts_to_sequences([new_comment])
new_comment = tf.keras.preprocessing.sequence.pad_sequences(new_comment, padding='post', maxlen=maxlen)
predicted_category = encoder.inverse_transform([np.argmax(model.predict(new_comment))])[0]
print('Predicted category:', predicted_category)