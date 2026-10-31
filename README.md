# website-monitoring
Website Monitoring.

Access the url and check if the response is what you expect.

## Run

### Prepare
- `$ touch log/monitor.log`

### Build
`$ docker build . -t website-monitoring`

### Run
`$ docker run --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log website-monitoring python main.py`

see log: `log/monitor.log`

#### send ok message if all ok
with `--send_all_success True`

#### use slack
- `$ cp messenger/secret.py.tmp messenger/secret.py` and set your slack token.
- `$ docker build . -t website-monitoring`
- `$ docker run --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log website-monitoring python main.py --messenger slack`

#### use discord

```sh
export DISCORD_WEBHOOK_URL='<webhook-url>'
docker run --env DISCORD_WEBHOOK_URL \
  --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log \
  website-monitoring python main.py --messenger discord
```

## Setting
Set the url and expected body message in `monitor_sites.py`
