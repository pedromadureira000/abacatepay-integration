.PHONY: create-user

create-user:
	@read -p "Enter username: " username; \
	read -s -p "Enter password: " password; \
	echo ""; \
	python -m src.create_user $$username $$password
