generate:
	python -m grpc_tools.protoc -I ./protos --python_out=server/pb --grpc_python_out=server/pb ./protos/model.proto

predict:
	grpcurl -plaintext -d '{"sepal_length": 1.3, "sepal_width": 2.1, "petal_length": 2.2, "petal_width": 0.8}' -proto ./protos/model.proto localhost:50051 PredictionService.Predict

check_health:
	grpcurl -plaintext -proto ./protos/model.proto localhost:50051 PredictionService.Health

build:
	docker build -t hw2 .

run:
	uv run main.py

run_docker:
	docker rm -f hw2 && docker run --name hw2 -p 50051:50051 hw2

format:
	ruff check --select I,F401 --fix . && ruff format --line-length 79 .
