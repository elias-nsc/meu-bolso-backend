APP_NAME=meu-bolso

up-prod:
	docker compose -f composes/production.yml up -d --build

down-prod:
	docker compose -f composes/production.yml down

up-dev:
	docker compose -f composes/develop.yml up --build

down-dev:
	docker compose -f composes/develop.yml down

test:
	docker compose -f composes/test.yml up --build --abort-on-container-exit

logs:
	docker logs -f meu-bolso-prod