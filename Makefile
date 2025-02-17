.PHONY: dev
dev:
	uvicorn main:app --reload --host 0.0.0.0