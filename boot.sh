#!/bin/bash
export FLASK_APP=game.py
export FLASK_APP_DATABASE_USER='postgres'
export FLASK_APP_DATABASE_PASSWORD='svinqtamaika_123'
export FLASK_APP_DATABASE_DB='business_game'
export FLASK_APP_DATABASE_HOST='localhost'
export FLASK_APP_DATABASE_PORT='5432'
gunicorn -b 0.0.0.0:5001 -w 16 game:app --access-logfile /home/business_game/business_game/logs/gunicorn-access.log --error-logfile /home/business_game/business_game/logs/gunicorn-error.log
