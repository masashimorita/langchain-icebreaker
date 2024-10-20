.PHONY: build install sh run down

create-network:
	docker network create ollama_default

up:
	docker compose -f docker-compose.yml up

down:
	docker compose -f docker-compose.yml down

build:
	docker compose -f docker-compose.yml build

bash:
	docker compose -f docker-compose.yml run --rm app bash

shell:
	docker compose -f docker-compose.yml run --rm app bash pipenv shell

black:
	docker compose -f docker-compose.yml run --rm app bash pipenv run black .
