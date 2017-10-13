# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

__all__ = [
    "KerasModel"
]

class KerasModel:

	#Class for a model using Keras backend Tensorflow
	
	def __init__(self, n_features, n_classes, learning_rate):

		self.n_features = n_features
		self.n_classes = n_classes
		self.learning_rate = learning_rate
		

	def example_model(self):
		
		"""
		3 (linear connected) layer example model: 
		- 1 Dense layer with n_features (training variables) dimension 
		- 1 Dropout layer (reduces overtraining effects) 
		- 1 Dense layer with n_classes dimension
		"""

		model = Sequential()
		model.add(Dense(10, activation = 'relu', input_shape = self.n_features))
		model.add(Dropout(0.5))
		model.add(Dense(self.n_classes, activation = 'softmax'))

		# Compile the model:

		model.compile(loss = 'categorical_crossentropy', optimizer = Adam(lr = self.learning_rate), metrics = ['accuracy'])

		
		