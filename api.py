from flask import Flask, request, jsonify

app = Flask(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# Dummy recommendations (replace with your actual logic)
def get_recommendations(query):
    return [
        {
            "assessment_name": "SHL Numerical Reasoning",
            "url": "https://www.shl.com/example-numerical",
            "remote_support": "Yes",
            "adaptive": "Yes",
            "duration": "30 minutes",
            "test_type": "Cognitive"
        },
        {
            "assessment_name": "SHL Verbal Reasoning",
            "url": "https://www.shl.com/example-verbal",
            "remote_support": "Yes",
            "adaptive": "No",
            "duration": "25 minutes",
            "test_type": "Cognitive"
        }
    ]

# Recommend endpoint
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    recommendations = get_recommendations(query)
    return jsonify({"recommendations": recommendations}), 200

# Run locally
if __name__ == '__main__':
    app.run(debug=True)


















