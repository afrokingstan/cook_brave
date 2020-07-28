import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv(verbose=True)


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_manager'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())

@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
                           cuisines=mongo.db.cuisines.find(),
                           required_tools=mongo.db.required_tools.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


@app.route('/editrecipe_home')
def editrecipe_home():
    return render_template("editrecipe_home.html", recipes=mongo.db.recipes.find())




@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.cuisines.find()
    all_tools =  mongo.db.required_tools.find()
    return render_template('editrecipe.html', recipe=the_recipe, 
                           cuisines=all_categories,
                           tool=all_tools)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            #port=int(os.environ.get('PORT')),
            debug=True)