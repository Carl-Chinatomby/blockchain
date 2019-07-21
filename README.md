# blockchain

## Installation

1. `docker build . -t blockchain:1.0`
1. `docker run -p 5000:5000 --mount type=bind,src=<ENTER_WORKING_DIR>,dst=/var/app blockchain:1.0`

Webserver is running on 0.0.0.0:5000

## Routes

### GET /mine

### POST /transactions/new

### GET /chain

### POST /nodes/register

### GET /nodes/resolve
