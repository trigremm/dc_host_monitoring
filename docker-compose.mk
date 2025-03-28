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
	# prepare directories
	mkdir -p .docker/prometheus
	chmod 777 .docker/prometheus
	mkdir -p .docker/grafana
	chmod 777 .docker/grafana
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
