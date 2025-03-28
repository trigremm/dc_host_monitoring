# main commands
include docker-compose.mk

.PHONY: format f
format:
	# npm install -g prettier
	prettier --write .

f: format




