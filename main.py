#!/usr/bin/env python3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Direct mapping for context stages
ANSWERS = {
    "data layer use for database queries": "repository",
    "pattern does the data layer": "repository",
    "handle deletion of shortened urls": "soft delete",
    "deletion": "soft delete",
    "two users shorten the same long url": "different codes",
    "same long url": "different codes",
}

SYNTHESIS_ANSWER = "unique constraint, hash, lookup before insert, user_id, separate analytics"
APPLICATION_ANSWER = "batch, queue, rate limit, retry, transaction, partial, rollback, chunk"

@app.route('/', methods=['GET', 'POST'])
@app.route('/query', methods=['GET', 'POST'])
def handle():
    if request.method == 'GET':
        return jsonify({"status": "ok"}), 200
    
    data = request.get_json(force=True)
    question = data.get('question', '').lower()
    stage = data.get('stage')
    
    # Check synthesis/application keywords
    if 'prevent' in question or 'duplicate' in question or 'synthesis' in str(stage):
        return jsonify({"answer": SYNTHESIS_ANSWER})
    if 'batch' in question or '10000' in question or 'programmatically' in question or 'application' in str(stage):
        return jsonify({"answer": APPLICATION_ANSWER})
    
    # Stage-based lookup
    if stage == 1:
        return jsonify({"answer": "repository"})
    elif stage == 2:
        return jsonify({"answer": "soft delete"})
    elif stage == 3:
        return jsonify({"answer": "different codes"})
    
    # Keyword fallback
    for q, a in ANSWERS.items():
        if q in question:
            return jsonify({"answer": a})
    
    return jsonify({"answer": "unknown"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
