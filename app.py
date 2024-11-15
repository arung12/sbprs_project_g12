from flask import Flask, render_template, request
import model 

app = Flask(__name__)

@app.route('/')
def home():
    users = model.get_popular_users()
    return render_template('index.html',users=users,username="")

@app.route('/',methods=['POST'])
def recommend_top_5_products():
    users = model.get_popular_users()
    recommended_products = []
    username=""
    if request.method == "POST":
        username = request.form.get('username')
        customUsername = request.form.get('customUsername')

        if username=="Other" and customUsername:
            username = customUsername

        if username:
            recommended_final= recommend_products(username)
            if recommended_final is None:
                recommended_products =[]
            else:  
                recommended_products = recommended_final.to_dict(orient='records')
    return render_template("index.html",username=username, users=users,recommended_products=recommended_products)

def recommend_products(username):
    recommended = model.get_recommended_products(username)
    return recommended

if __name__ == "__main__":
    app.run(debug=True)

