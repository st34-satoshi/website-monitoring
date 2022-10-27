# website-monitoring
Website Monitoring

## Run

### Build
`docker build . -t website-monitoring`

### Run
`docker run --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log website-monitoring python main.py`
