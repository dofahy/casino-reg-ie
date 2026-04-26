import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from regulate_ie.core.logging import setup_logging
from regulate_ie.db import Base, get_engine, get_session, init_engine
from regulate_ie.model.models import Regulation

app = Flask(__name__)
logger = logging.getLogger(__name__)


def init_app():
    load_dotenv()
    setup_logging()
    init_engine()
    Base.metadata.create_all(bind=get_engine())


def insert_reg_blob(source: str, content: str):
    session = get_session()
    try:
        record = Regulation(source=source, content=content)
        session.add(record)
        session.commit()
        session.refresh(record)
        logger.info("DB insert success id=%s source=%s", record.id, source)
        return record.id
    except Exception:
        logger.exception("DB insert failed")
        raise
    finally:
        session.close()


@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    source = data.get("source")
    content = data.get("content")
    logger.info("Ingest request received source=%s size=%s", source, len(content or ""))
    if not source or not content:
        logger.warning("Invalid ingest request missing fields")
        return jsonify({"error": "source and content required"}), 400
    record_id = insert_reg_blob(source, content)
    logger.info("Inserted regulation id=%s", record_id)
    return jsonify({"id": record_id})


@app.route("/regulations", methods=["GET"])
def get_regulations():
    session = get_session()
    try:
        records = session.query(Regulation).all()
        return jsonify(
            [
                {
                    "id": r.id,
                    "source": r.source,
                    "content": r.content,
                    "created_at": r.created_at.isoformat(),
                }
                for r in records
            ]
        )
    finally:
        session.close()


@app.route("/regulations/<int:id>", methods=["DELETE"])
def delete_regulation(id: int):
    session = get_session()
    try:
        record = session.get(Regulation, id)
        if not record:
            return jsonify({"error": "not found"}), 404
        session.delete(record)
        session.commit()
        return jsonify({"deleted": id})
    finally:
        session.close()


def main():
    init_app()
    port = os.getenv("PORT", 5000)
    app.run(debug=True, port=int(port))


if __name__ == "__main__":
    main()
