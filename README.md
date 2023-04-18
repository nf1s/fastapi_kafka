# FastAPI kafka

## run

```bash
docker compose up -d
```

## Create topic

switch to container shell

```bash
docker exec -it kafka bash
```

run

```bash
kafka-topics --create --topic test.events --bootstrap-server kafka:29092 --partitions 4 --replication-factor 1
```
