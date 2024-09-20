#!/bin/zsh
celery -A app.celery purge
redis-cli flushall
