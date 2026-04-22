# casino-reg-ie
gambling regulation in ireland api

data:
- grab data from some sites
- scraping automation on schedule (later)

db:
- postgresql
- sqlalchemy
- - insert_reg_blob

###  setup
```
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e ".[dev]"

~/databases/bases/postgresql-18.3/bin/initdb -D ~/databases/data/pg18.3-casino-reg-ie --encoding=UTF8 --locale=en_IE.UTF-8
kate ~/databases/pg18.3-casino-reg-ie.conf
~/databases/bases/postgresql-18.3/bin/createdb -p 5433 casino-reg-ie
~/databases/bases/postgresql-18.3/bin/psql -p 5433 -d casino-reg-ie
```

### usage
```
curl -X POST http://localhost:5000/ingest -H "Content-Type: application/json" -d '{ "source": "source.ie", "content": "some data" }'

curl http://localhost:5000/regulations
```
