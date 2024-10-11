# PyAgent
Python Agent runs code in agents for distributed work handeling

## Run the server

```sh
$ pyagent serve --host 127.0.0.1 --port 8000 --name DEV-MANAGER-1
```

## Connect an agent

```sh
$ pyagent agent --url wss://my_subdomain.example.io/ws --token ABCD-AUTH-TOKEN --tags KOLKATA --tags IN-16
```