# website-monitoring
Website Monitoring.

Access the url and check if the response is what you expect.

## Run

### Build
`docker build . -t website-monitoring`

### Run
`docker run --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log website-monitoring python main.py`

see log: `log/monitor.log`

#### send ok message if all ok
with `--send_all_success True`

#### use slack
- `cp messenger/secret.py.tmp messenger/secret.py` and set your slack token.
- `docker build . -t website-monitoring`
- `docker run --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log website-monitoring python main.py --messenger slack`

## Setting
Set the url and expected body message in `monitor_sites.py`
