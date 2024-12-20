import tensorflow as tf
import tf2onnx
import onnx


model = tf.keras.models.load_model(r'C:\Users\lucas\Desktop\LaTiranaV2 - machine learning\model.keras')
@tf.function(input_signature=[tf.TensorSpec([None, 224, 224, 3], tf.float32)])

def model_func(input):
    return model(input)
onnx_model, _ = tf2onnx.convert.from_function(model_func, input_signature=[tf.TensorSpec([None, 224, 224, 3], tf.float32)])
onnx.save_model(onnx_model, "model.onnx")
