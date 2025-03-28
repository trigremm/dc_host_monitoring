all: ps

ps:
	docker compose ps

logs:
	while true; do docker compose logs -f --tail 100; sleep 10 ;done

prune:
	docker system prune -f -a

pull:
	git pull

build:
	docker compose build

up:
	# prepare directories with proper permissions
	mkdir -p .docker/prometheus/data
	chmod 777 .docker/prometheus/data
	mkdir -p .docker/grafana/data
	chmod 777 .docker/grafana/data
	mkdir -p .docker/loki/data
	chmod 777 .docker/loki/data
	# start services
	docker compose up -d --no-build

stop:
	docker compose stop

down:
	docker compose down

restart: stop up

recreate: pull build stop up ps

r: recreate

rl: recreate logs