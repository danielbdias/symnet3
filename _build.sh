#!/bin/bash

docker build -t symnet3:latest .

echo "To run the container, use the following command:"
echo "docker run -it symnet3:latest /bin/bash"