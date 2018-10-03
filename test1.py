'''
LICENSE: MIT
https://github.com/keras-team/keras/blob/a07253d8269e1b750f0a64767cc9a07da8a3b7ea/LICENSE

実験メモ
Dropoutをなくしてみたが、あまりへんかなし
SGDにへんこうしたら、しゅうそくがすごくおそくなった
面白い。

試したいアイデアがあるので、
自前のactivation functionを書いてみる。
'''

from __future__ import print_function

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import optimizers

from keras.layers import Activation
from keras import backend
from keras.utils.generic_utils import get_custom_objects

smoothing = 0
def custom_activation(x):
    return smoothing * backend.tanh(x / smoothing)

def replace_intermediate_layer_in_keras(model, layer_id, new_layer):
    from keras.models import Model

    layers = [l for l in model.layers]

    x = layers[0].output
    for i in range(1, len(layers)):
        if i == layer_id:
            x = new_layer(x)
        else:
            x = layers[i](x)

    new_model = Model(input=model.input, output=x)
    return new_model

batch_size = 128
num_classes = 10
epochs = 20

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Dense(512, activation='linear', input_shape=(784,)))
model.add(Activation(custom_activation))
# model.add(Dropout(0.2))
model.add(Dense(512, activation='linear'))
model.add(Activation(custom_activation))
# model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='linear'))
model.add(Activation(custom_activation))
# model.add(Dense(num_classes, activation='softmax'))

model.summary()

sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
rms_prop = optimizers.RMSprop()

# model.compile(loss='categorical_crossentropy',
#              optimizer=sgd,
#              metrics=['accuracy'])

# to create input layer
model = replace_intermediate_layer_in_keras(model, 1, Activation(custom_activation))

for i in range(5):
    smoothing = 0.01 * 1e2**(1.0 * (4 - i) / 4)

    model = replace_intermediate_layer_in_keras(model, 2, Activation(custom_activation))
    # model.summary()
    model = replace_intermediate_layer_in_keras(model, 4, Activation(custom_activation))
    # model.summary()
    model = replace_intermediate_layer_in_keras(model, 6, Activation(custom_activation))
    # model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=1,
                    verbose=1,
                    validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
