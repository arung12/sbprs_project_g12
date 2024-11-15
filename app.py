from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def recommend_top_5_products():
    print(request.method)
    reviews_username = request.form['username']
    print('User name=',reviews_username)
    recommended_products = []
    if request.method == "POST":
        reviews_username = request.form["username"]
        recommended_products = recommend_products(username)
    return render_template("index.html", recommended_products=recommended_products)

def recommend_products(username):
    # Simple mock recommendation based on username length for illustration
    products = [
        "Laptop", "Smartphone", "Headphones", "Smartwatch", "TV", "Camera", "Speaker", "Tablet", "Keyboard", "Mouse"
    ]
    # In a real case, this could be a model prediction or product filtering logic.
    recommended = products[:5]  # Recommend first 5 products as an example
    return recommended

if __name__ == "__main__":
    app.run(debug=True)

