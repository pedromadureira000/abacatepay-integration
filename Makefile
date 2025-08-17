.PHONY: create-user

create-user:
	@read -p "Enter username: " username; \
	read -s -p "Enter password: " password; \
	echo ""; \
	python -m src.create_user $$username $$password

create-user2:
	@read -p "Enter username: " username; \
	echo -n "Enter password: "; \
	stty -echo; \
	read password; \
	stty echo; \
	echo ""; \
	python -m src.create_user $$username $$password
