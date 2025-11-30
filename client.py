import grpc

from server.pb import model_pb2, model_pb2_grpc
from server.settings import settings

channel = grpc.insecure_channel(f"localhost:{settings.port}")
stub = model_pb2_grpc.PredictionServiceStub(channel)

request = model_pb2.PredictRequest(
    sepal_length=3.1,
    sepal_width=2.2,
    petal_length=0.8,
    petal_width=1.1,
)
response = stub.Predict(request)
print("Prediction:", response.prediction)
