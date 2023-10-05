.PHONY: help
help: ## Show this help (usage: make help)
	@echo "Usage: make [target]"
	@echo "Targets:"
	@awk '/^[a-zA-Z0-9_-]+:.*?##/ { \
		helpMessage = match($$0, /## (.*)/); \
		if (helpMessage) { \
			target = $$1; \
			sub(/:/, "", target); \
			printf "  \033[36m%-20s\033[0m %s\n", target, substr($$0, RSTART + 3, RLENGTH); \
		} \
	}' $(MAKEFILE_LIST)

.PHONY: pre-commit
pre-commit:	## Run pre-commit hooks
	pre-commit

.PHONY: test
test:	## Run project tests
	pytest

.PHONY: build
build:	## Build project with docker-compose
	docker-compose up --build

.PHONY: up
up:	## Run project with docker-compose
	docker-compose up --remove-orphans

.PHONY: clean
clean: ## Clean up project containers, networks and volumes with docker-compose
	docker-compose down -v --remove-orphans | true
	docker-compose rm -f | true
	docker volume rm python-backend-template_backend_postgres_data | true

.PHONY: down
down: ## Stop project with docker-compose and remove containers and networks, but volume remains
	docker-compose down --remove-orphans | true

.PHONY: autogenerate
autogenerate:  ## Generate migration file (usage: make autogenerate msg="migration message")
	docker-compose up -d | true
	docker-compose exec app alembic revision --autogenerate -m "$(msg)"

.PHONY: downgrade
downgrade:  ## Downgrade by 1 revision
	docker-compose up -d | true
	docker-compose exec app alembic downgrade -1

.PHONY: downgrade_to
downgrade_to:  ## Downgrade to the specific revision (usage: make downgrade_to revision="revision")
	docker-compose up -d | true
	docker-compose exec app alembic downgrade "$(revision)"
