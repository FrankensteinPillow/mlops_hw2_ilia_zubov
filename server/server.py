from concurrent import futures

import grpc
import joblib
import pandas as pd

from server.pb import model_pb2, model_pb2_grpc
from server.settings import settings


class PredictionService(model_pb2_grpc.PredictionServiceServicer):
    def __init__(self):
        self.model = joblib.load(settings.model_path)

    def Predict(self, request, context):
        input_data = pd.DataFrame(
            [
                {
                    "Id": 0,
                    "SepalLengthCm": request.sepal_length,
                    "SepalWidthCm": request.sepal_width,
                    "PetalLengthCm": request.petal_length,
                    "PetalWidthCm": request.petal_width,
                }
            ]
        )
        answer = self.model.predict(input_data)
        return model_pb2.PredictResponse(
            prediction=answer[0], model_version=settings.model_version
        )

    def Health(self, request, context):
        if self.model is not None:
            return model_pb2.HealthResponse(status="ok")
        return model_pb2.HealthResponse(status="Model not loaded")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    model_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionService(), server
    )
    server.add_insecure_port(f"[::]:{settings.port}")
    server.start()
    server.wait_for_termination()
