from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    users = ['Alice', 'Bob', 'Charlie', 'David']
    return render_template('index.html',users=users)

@app.route('/',methods=['POST'])
def recommend_top_5_products():
    users = ['Alice', 'Bob', 'Charlie', 'David']
    recommended_products = []
    if request.method == "POST":
        reviews_username = request.form["username"]
        recommended_products = recommend_products(reviews_username)
    return render_template("index.html", users=users,recommended_products=recommended_products)

def recommend_products(username):
    # Simple mock recommendation based on username length for illustration
    products  = [
            {
                'name': 'Product 1',
                'description': 'A great product for everyone.',
                'price': '99.99',
                'url': '/product/1',
            },
            {
                'name': 'Product 2',
                'description': 'An amazing new product.',
                'price': '49.99',
                'url': '/product/2',
            },
            {
                'name': 'Product 1',
                'description': 'A great product for everyone.',
                'price': '99.99',
                'url': '/product/1',
            },
            {
                'name': 'Product 2',
                'description': 'An amazing new product.',
                'price': '49.99',
                'url': '/product/2',
            },
            {
                'name': 'Product 1',
                'description': 'A great product for everyone.',
                'price': '99.99',
                'url': '/product/1',
            },
            {
                'name': 'Product 2',
                'description': 'An amazing new product.',
                'price': '49.99',
                'url': '/product/2',
            }
            # Add more products as needed
        ]
    # In a real case, this could be a model prediction or product filtering logic.
    recommended = products #[:5]  # Recommend first 5 products as an example
    return recommended

if __name__ == "__main__":
    app.run(debug=True)

