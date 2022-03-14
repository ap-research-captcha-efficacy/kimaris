import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from os import path
from PIL import Image

vocab = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "a",
    11: "b",
    12: "c",
    13: "d",
    14: "e",
    15: "f",
}

class amadeus():
    def __init__(self, path, image_size, batch_size, load_from_file=False, epochs=15):
        if load_from_file and not self.check_for_save():
            print("save does not yet existing, defaulting to normal routine")
            load_from_file = False
        self.image_size = image_size
        self.batch_size = batch_size

        self.fitted = load_from_file
        self.dataset_loaded = False

        if not load_from_file:
            self.dataset_training, self.dataset_validation = self.load_datasets(path)
        self.model = self.load_model_from_disk() if load_from_file else self.construct_model()

        if not load_from_file:
            self.fit(epochs)

    def load_datasets(self, path):
        dataset_training = keras.preprocessing.image_dataset_from_directory(
            path, 
            validation_split=0.2,
            seed=1337,
            subset="training",
            image_size=self.image_size,
            labels="inferred",
            batch_size=self.batch_size,
        )

        dataset_validation = keras.preprocessing.image_dataset_from_directory(
            path,
            validation_split=0.2,
            seed=1337,
            subset="validation",
            image_size=self.image_size, 
            labels="inferred", 
            batch_size=self.batch_size,
        )
        self.dataset_loaded = True
        return (dataset_training, dataset_validation)
    
    def construct_model(self):
        inputs = keras.Input(shape=self.image_size+(3,))
        x = layers.Rescaling(scale=1.0/255)(inputs)

        x = layers.Conv2D(filters=32, kernel_size=(3, 3), activation="relu", padding="same")(x)
        x = layers.MaxPooling2D(pool_size=(3, 3), padding="same")(x)
        x = layers.Conv2D(filters=32, kernel_size=(3, 3), activation="relu", padding="same")(x)
        x = layers.MaxPooling2D(pool_size=(3, 3), padding="same")(x)
        x = layers.Conv2D(filters=32, kernel_size=(3, 3), activation="relu", padding="same")(x)

        x = layers.GlobalAveragePooling2D()(x)

        num_classes = 16
        outputs = layers.Dense(num_classes, activation="softmax")(x)

        return keras.Model(inputs=inputs, outputs=outputs)
    
    def load_model_from_disk(self):
        try:
            return keras.models.load_model("./saves/final")
        except Exception as e:
            print(e, "error loading model from disk, try generating it the normal way")

    def check_for_save(self):
        return path.isdir("./saves/final")

    def fit(self, epochs):
        if not self.dataset_loaded or not self.model:
            print("tried to fit before loading dataset inclusive(or) loading model")
            return
        callbacks = [
            keras.callbacks.ModelCheckpoint("./saves/{epoch}"),
        ]
        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")
        self.model.fit(self.dataset_training, epochs=epochs, callbacks=callbacks, validation_data=self.dataset_validation)
        self.model.save("./saves/final")
        self.fitted = True

    def test_accuracy_on_image_pil(self, img):
        if not self.fitted:
            print("tried testing unfitted dataset")
            return
        img = img.convert("RGB")
        img = img.resize((self.image_size[1], self.image_size[0]), resample=Image.NEAREST)
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = self.model.predict(img_array)
        score = predictions[0]

        return vocab[np.argmax(score)]

    def test_accuracy_on_image(self, path):
        return self.test_accuracy_on_image_pil(Image.open(path))

    def plot_model(self):
        if not self.model:
            print("tried plotting None model")
            return
        keras.utils.plot_model(self.model, show_shapes=True)