from tensorflow.keras import Sequential,layers, Model
from tensorflow.keras import models
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping


def initialize_model_concat(model_nlp, model_images):

    # model_nlp = build_model_nlp() # comment-out to keep pre-trained weights not to start from scratch
    input_nlp = model_nlp.input
    output_nlp = model_nlp.output

    # model_num = build_model_num() # comment-out to keep pre-trained weights not to start from scratch
    input_images = model_images.input
    output_images = model_images.output

    inputs = [input_nlp, input_images]

    combined = layers.concatenate([output_nlp, output_images])

    x = layers.Dense(10, activation="relu")(combined)

    outputs = layers.Dense(1, activation="linear")(x)

    model_combined = models.Model(inputs=inputs, outputs=outputs)

    return model_combined


def train_model_concat(model,
                       X_train_pad,
                       X_train_images,
                       y_train,
                       batch_size=32,
                       patience=10,
                       epochs=1000,
                       validation_split=0.2,
                       learning_rate=1e-4,
                       validation_data=None):

    model.compile(loss="mse", optimizer=Adam(learning_rate=learning_rate), metrics=['mae'])
    es = EarlyStopping(patience=patience)

    model.fit(x=[X_train_pad, X_train_images],
    y=y_train,
    validation_split=validation_split,
    epochs=epochs,
    batch_size=batch_size,
    callbacks=[es])
