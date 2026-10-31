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

## Setting
Set the url and expected body message in `monitor_sites.py`

### Discord notifications

In Discord, open **Server Settings > Integrations > Webhooks**, create a
webhook, select the destination channel, and copy its webhook URL.
You need the Manage Webhooks permission. A bot is not required.

Set `DISCORD_WEBHOOK_URL` in the environment of the process running the monitor:

```sh
export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/<id>/<token>'
python main.py --messenger discord
```

For Docker, build the image as above and pass the environment variable at runtime:

```sh
docker run --env DISCORD_WEBHOOK_URL \
  --mount type=bind,source="$(pwd)/log/monitor.log",target=/usr/src/app/log/monitor.log \
  website-monitoring python main.py --messenger discord
```

For scheduled runs, supply the variable through the scheduler's environment or
a private wrapper script. Keep the URL secret; do not commit it or bake it into
the Docker image. Discord and logger modes do not require Slack credentials.

Use `--send_all_success True` to also send `all ok!` when every check passes.
The default messenger remains `logger`; choose `slack` or `discord` to send
notifications to one service per run.

Discord messages longer than 2,000 characters are split into multiple posts,
with automatic mentions disabled. Missing Discord configuration stops the run
before monitoring begins. Delivery errors are logged without the webhook URL;
the remaining sites are still checked and the process exits with status 1.
Requests time out after 10 seconds of inactivity. Failed sends are not retried
automatically, including rate-limit responses (HTTP 429).

### Tests

```sh
python -m unittest discover -s tests -v
```

Tests mock external requests and do not send real notifications.
