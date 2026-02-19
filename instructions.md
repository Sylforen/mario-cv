docker build -t mario-ml .

docker run --gpus all -it --rm \
    -v "$PWD":/app \
    mario-ml
