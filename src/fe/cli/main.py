import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from be.db import engine, SessionLocal
from be.model.models import Base, Regulation


app = Flask(__name__)

Base.metadata.create_all(bind=engine)


def insert_reg_blob(source: str, content: str):
    session = SessionLocal()
    try:
        record = Regulation(source=source, content=content)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id
    finally:
        session.close()


@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    source = data.get("source")
    content = data.get("content")
    if not source or not content:
        return jsonify({"error": "source and content required"}), 400
    record_id = insert_reg_blob(source, content)
    return jsonify({"id": record_id})


@app.route("/regulations", methods=["GET"])
def get_regulations():
    session = SessionLocal()
    try:
        records = session.query(Regulation).all()
        return jsonify([
            {
                "id": r.id,
                "source": r.source,
                "content": r.content,
                "created_at": r.created_at.isoformat()
            }
            for r in records
        ])
    finally:
        session.close()

@app.route("/regulations/<int:id>", methods=["DELETE"])
def delete_regulation(id: int):
    session = SessionLocal()
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
    port = os.getenv("PORT", 5000)
    app.run(debug=True, port=port)


if __name__ == "__main__":
    main()
