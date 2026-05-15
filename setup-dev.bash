#!/bin/bash
echo "Running initial dev setup..."

python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
echo ".env created, remember to edit after creating db"


echo "Setup complete, run pytest to confirm"
