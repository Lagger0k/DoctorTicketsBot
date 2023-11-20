THIS_FILE := $(lastword $(MAKEFILE_LIST))

db_container := local_db


.DEFAULT_GOAL := start_db

.PHONY: cleanup start_db migrate

cleanup:
	docker ps -q --filter "name=${db_container}" | grep -q . && docker stop ${db_container} || true


start_db: cleanup
	docker run -d --name ${db_container} --rm -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test_ticket -p 54321:5432 postgres

migrate:
	cd etl/ && alembic upgrade head