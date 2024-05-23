from flask import Flask,request,render_template
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.utils.utils import load_object
from jinja2 import Environment


app=Flask(__name__)

# Add enumerate to the Jinja2 environment globals
app.jinja_env.globals['enumerate'] = enumerate


@app.route('/')
def home_page():
    return render_template("index.html")

# for testing purpose
@app.route("/ping",methods=['GET'])
def ping():
    return "Success"

@app.route("/recommend",methods=["GET","POST"])
def predict_datapoint():
    if request.method=="GET":
        # getting the products list from the pickle file
        products_list = load_object("artifacts/products.pkl")
        return render_template("form.html",products=products_list)
    
    else:

        # getting the selected products from the form
        selected_products = request.form.getlist('products')
        
        # converting the list of products to set
        selected_products = set(selected_products)

        print("selected prods : ",selected_products)
        # calling the inference pipeline for prediction
        predict_pipeline=PredictionPipeline()
        # doing prediction
        recommendations=predict_pipeline.recommend(selected_products)
        print("recommendations",recommendations)

        return render_template("result.html",recommendations=recommendations,product=selected_products)



if __name__=="__main__":
    app.run(host="0.0.0.0") 