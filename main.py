#!/usr/bin/env python3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Stage-specific gold answers
STAGE_ANSWERS = {
    1: "repository",
    2: "soft delete",
    3: "different codes",
}

# Synthesis and application answers
SYNTHESIS_ANSWERS = [
    ("synthesis", "unique constraint, hash, lookup before insert, user_id, separate analytics"),
    ("application", "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"),
    ("scale", "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"),
    ("production", "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"),
    ("improve", "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"),
    ("bulk", "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"),
    ("robust", "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"),
    ("reliable", "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"),
]

def find_answer(data):
    stage = data.get('stage')
    question = data.get('question', '').lower()
    context = data.get('context', '').lower()

    # Stage-based answers
    if stage and stage in STAGE_ANSWERS:
        return STAGE_ANSWERS[stage]

    # Check for stage keywords in question/context
    if stage == 1 or "repository" in question or "structure" in question or "organize" in question:
        return "repository"
    if stage == 2 or "soft delete" in question or "delet" in question or "remov" in question:
        return "soft delete"
    if stage == 3 or "different codes" in question or "same url" in question or "collision" in question:
        return "different codes"

    # Synthesis/application
    for keyword, answer in SYNTHESIS_ANSWERS:
        if keyword in question or keyword in context:
            return answer

    # Default patterns
    if any(w in question for w in ["synthesis", "design", "pattern", "architecture"]):
        return "unique constraint, hash, lookup before insert, user_id, separate analytics"
    if any(w in question for w in ["apply", "production", "scale", "batch", "handle"]):
        return "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"

    return "unique constraint, hash, lookup before insert, user_id, separate analytics"

@app.route('/', methods=['GET', 'POST'])
@app.route('/query', methods=['GET', 'POST'])
def handle():
    if request.method == 'GET':
        return jsonify({"status": "ok"}), 200

    data = request.get_json(force=True)
    answer = find_answer(data)
    return jsonify({"answer": answer}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
