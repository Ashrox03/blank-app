from flask import Flask, request, jsonify, render_template

# Initialize Flask App
app = Flask(__name__)

# Placeholder Data for MSMEs
msme_data = [
    {
        "id": "MSME001",
        "name": "Greenfield Enterprises",
        "sector": "Manufacturing",
        "location": "Mumbai",
        "annual_revenue": 5000000,
        "credit_score": 720,
        "loan_history": [
            {"amount": 200000, "status": "repaid"},
            {"amount": 500000, "status": "default"},
        ],
    },
    {
        "id": "MSME002",
        "name": "BlueSky Traders",
        "sector": "Retail",
        "location": "Delhi",
        "annual_revenue": 2000000,
        "credit_score": 680,
        "loan_history": [
            {"amount": 100000, "status": "repaid"}
        ],
    },
]

# Retrieval Function
def retrieve_msme_data(query):
    results = [msme for msme in msme_data if query.lower() in msme["name"].lower()]
    return results if results else []

# Validation Function
def validate_msme(msme):
    if msme["credit_score"] > 700 and msme["annual_revenue"] > 3000000:
        return f"MSME {msme['name']} is eligible for credit."
    else:
        return f"MSME {msme['name']} is not eligible for credit."

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/retrieve', methods=['GET'])
def retrieve():
    query = request.args.get('query', '')
    results = retrieve_msme_data(query)
    if results:
        return jsonify(results)
    else:
        return jsonify({"message": "No matching MSMEs found."})

@app.route('/validate', methods=['POST'])
def validate():
    msme = request.json
    result = validate_msme(msme)
    return jsonify({"validation": result})

# HTML Template (to be saved as templates/index.html)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MSME Credit Risk Tool</title>
    <script>
        async function fetchMSMEData() {
            const query = document.getElementById('query').value;
            const response = await fetch(`/retrieve?query=${query}`);
            const data = await response.json();
            document.getElementById('results').innerText = JSON.stringify(data, null, 2);
        }

        async function validateMSME() {
            const msme = JSON.parse(document.getElementById('msme').value);
            const response = await fetch('/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(msme),
            });
            const data = await response.json();
            document.getElementById('validation').innerText = data.validation;
        }
    </script>
</head>
<body>
    <h1>MSME Credit Risk Tool</h1>

    <section>
        <h2>Retrieve MSME Data</h2>
        <input type="text" id="query" placeholder="Enter MSME name">
        <button onclick="fetchMSMEData()">Search</button>
        <pre id="results"></pre>
    </section>

    <section>
        <h2>Validate MSME</h2>
        <textarea id="msme" placeholder='Enter MSME JSON here'></textarea>
        <button onclick="validateMSME()">Validate</button>
        <pre id="validation"></pre>
    </section>
</body>
</html>
"""

# Save HTML Template to File
import os
os.makedirs('templates', exist_ok=True)
with open('templates/index.html', 'w') as f:
    f.write(html_template)

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
