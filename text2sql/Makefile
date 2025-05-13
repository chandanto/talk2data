# === VARIABLES ===
APP_NAME=talk2data
PORT=8501
SECRETS_PATH=$(CURDIR)/.streamlit

# === TARGETS ===

# Build debug (with Alpine, for dev/debugging)
build-debug:
	docker build -t $(APP_NAME):1.0.0 -f Dockerfile.alpine .

# Remove docker image of debug
clean-debug:
	docker rmi -f $(APP_NAME):debug || true

# Run debug container with secrets mounted
run-debug:
	docker run -it --rm \
		-p $(PORT):8501 \
		-v $(SECRETS_PATH):/app/.streamlit \
		$(APP_NAME):1.0.0

# Build production (distroless)
build-prod:
	docker build -t $(APP_NAME):latest -f Dockerfile.alpine .

# Remove docker image of production
clean-prod:
	docker rmi -f $(APP_NAME):prod || true

# Run production container with secrets mounted
run-prod:
	docker run -it --rm \
		-p $(PORT):8501 \
		-v $(SECRETS_PATH):/app/.streamlit \
		$(APP_NAME):latest

# Clean up all Docker images
clean:
	docker rmi -f $(APP_NAME):1.0.0 $(APP_NAME):latest || true
