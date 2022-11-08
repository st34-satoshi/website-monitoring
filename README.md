# website-monitoring
Website Monitoring

## Run

### Build
`docker build . -t website-monitoring`

### Run
`docker run --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log website-monitoring python main.py`

see log: `log/monitor.log`

#### use slack
- `cp messenger/secret.py.tmp messenger/secret.py` and set your slack token.
- `docker build . -t website-monitoring`
- `docker run --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log website-monitoring python main.py --messenger slack`
