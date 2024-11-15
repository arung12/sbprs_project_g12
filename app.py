from flask import Flask, render_template, request
import model 

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
    recommended = model.recommend_products(username)
    return recommended

if __name__ == "__main__":
    app.run(debug=True)

