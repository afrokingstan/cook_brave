import os
import bson
import secrets
from flask import Flask, render_template, redirect, request, url_for, session, flash, abort
from werkzeug.exceptions import HTTPException
from  werkzeug.debug import get_current_traceback
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv(verbose=True)

# database connection code
app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_manager'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)
#start of session key generator to ensure falsh message is displayed
secret = secrets.token_urlsafe(32)
app.secret_key = secret
#end of session key generator

#start of exception handling code
@app.errorhandler(bson.errors.InvalidId)
def handle_exception(e):
   flash("That object does not exist",  "danger")
   return redirect(url_for('get_recipes'))

@app.errorhandler(Exception)
def unhandled_exception(e):
   return render_template('500_generic.html'), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template("500_generic.html"), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
#end of exceptopn handling code

#start of all recipe home page code
@app.route('/get_recipes')
def get_recipes():
    return render_template("allrecipes.html", recipes=mongo.db.recipes.find().sort("_id", -1))

@app.route('/')
@app.route('/sort_recipes')
def sort_recipes():
    offset = 2
    limit = 3
    starting_id = mongo.db.recipes.find().sort("_id", -1)
    last_id = starting_id[offset]['_id']
    return render_template("recipes.html", recipes=mongo.db.recipes.find({'_id' : {'$gte' : last_id}}).sort("_id", -1).limit(limit))

#end of all recipes homepage

#start ofpagination code
@app.route('/page2')
def page2():
    flash("You are on Page Two", "info")
    offset = 1
    starting_id = mongo.db.recipes.find().sort("_id", -1)
    last_id = starting_id[offset]['_id']
    return render_template("recipes.html", recipes=mongo.db.recipes.find({'_id' : {'$lt' : last_id}}).sort("_id", -1))

@app.route('/page1')
def page1():
    flash("You are on Page One", "info")
    offset = 2
    limit = 3
    starting_id = mongo.db.recipes.find().sort("_id", -1)
    last_id = starting_id[offset]['_id']
    return render_template("recipes.html", recipes=mongo.db.recipes.find({'_id' : {'$gte' : last_id}}).sort("_id", -1).limit(limit))
#end of pagination

#start of add recipe code
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
                           cuisines=mongo.db.cuisines.find(),
                           required_tools=mongo.db.required_tools.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    flash("You successfully added one recipe", "info")
    return redirect(url_for('get_recipes'))
#end of add recipe code

#start of file upload file handling 
@app.route('/uploadshome')
def uploadshome():
    flash("Please select a recipe image to upload", "info")
    return render_template("upload_image.html")

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_image", methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part', 'danger')
            return redirect("upload_image.html")
        image = request.files['image']
        # if user does not select file, browser also
        # submit an empty part without filename
        if image.filename == '':
            flash('No selected file', 'danger')
            return redirect("upload_image.html")
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image uploaded', 'info')
            return redirect(url_for('add_recipe', 
            filename=filename))
        else:
            flash('That file extension is not allowed', 'danger')
            return redirect("upload_image.html")
#end of file upload file handling

# start of edit recipe codes 
@app.route('/editrecipe_home')
def editrecipe_home():
    flash("Please select the recipe you want to edit", "info")
    return render_template("editrecipe_home.html", recipes=mongo.db.recipes.find())

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.cuisines.find()
    all_tools = mongo.db.required_tools.find()
    return render_template('editrecipe.html', recipe=the_recipe,
                           cuisines=all_categories,
                           tool=all_tools)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
                   {
        'required_tools': request.form.get('required_tools'),
        'cuisine_name': request.form.get('cuisine_name'),
        'recipe_name': request.form.get('recipe_name'),
        'preparation_time': request.form.get('preparation_time'),
        'cooking_time': request.form.get('cooking_time'),
        'author': request.form.get('author'),
        'alias': request.form.get('alias'),
        'date_stamp': request.form.get('date_stamp'),
        'ingredients': request.form.get('ingredients'),
        'image_name': request.form.get('image_name'),
        'preparation_steps': request.form.get('preparation_steps')
    })
    flash("You successfully updated one recipe", "info")
    return redirect(url_for('get_recipes'))
# end of edit recipe code

#start of delete recipe code
@app.route('/deleterecipe_home')
def deleterecipe_home():
    flash("Please select the recipe you want to delete", "info")
    return render_template("deleterecipe_home.html", recipes=mongo.db.recipes.find())

@app.route('/delete_single_recipe/<recipe_id>')
def delete_single_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.cuisines.find()
    all_tools = mongo.db.required_tools.find()
    return render_template('delete_single_recipe.html', recipe=the_recipe,
                           cuisines=all_categories,
                           tool=all_tools)

@app.route('/remove_recipe/<recipe_id>', methods=["POST"])
def remove_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash("You successfully deleted one recipe", "danger")
    return redirect(url_for('get_recipes'))
#end of delete recipe code

# start of filter recipe code
@app.route('/Afrofilter')
def Afrofilter():
    cur = mongo.db.recipes.find({"cuisine_name": "African"})
    results = list(cur) 
# Checking the cursor is empty 
# or not 
    if len(results)==0:
        flash("These no African recipes, would you like to add one", "info")
        return render_template("404.html")
    else:
        flash("These are all the African Cuisine recipes", "info")
        return render_template("filter.html", recipes=mongo.db.recipes.find({"cuisine_name": "African"}))

@app.route('/Carifilter')
def Carifilter():
    cur = mongo.db.recipes.find({"cuisine_name": "Caribbean"})
    results = list(cur) 
# Checking the cursor is empty 
# or not 
    if len(results)==0:
        flash("These no Caribbean recipes, would you like to add one", "info")
        return render_template("404.html")
    else:
        flash("These are all the Caribbean Cuisine recipes", "info")
        return render_template("filter.html", recipes=mongo.db.recipes.find({"cuisine_name": "Caribbean"}))

@app.route('/Spanifilter')
def Spanifilter():
    cur = mongo.db.recipes.find({"cuisine_name": "Spanish"})
    results = list(cur) 
# Checking the cursor is empty 
# or not 
    if len(results)==0:
        flash("These no Spanish recipes, would you like to add one", "info")
        return render_template("404.html")
    else:
        flash("These are all the Spanish recipes", "info")
        return render_template("filter.html", recipes=mongo.db.recipes.find({"cuisine_name": "Spanish"}))

@app.route('/BPfilter')
def BPfilter():
    cur = mongo.db.recipes.find({"required_tools": "brand Pressure cooker"})
    results = list(cur) 
# Checking the cursor is empty 
# or not 
    if len(results)==0:
        flash("These no brand Pressure cooker recipes, would you like to add one", "info")
        return render_template("404.html")
    else:
        flash("These are all the brand Pressure cooker recipes", "info")
        return render_template("filter.html", recipes=mongo.db.recipes.find({"required_tools": "brand Pressure cooker"}))

@app.route('/BSfilter')
def BSfilter():
    cur = mongo.db.recipes.find({"required_tools": "brand steamer"})
    results = list(cur) 
# Checking the cursor is empty 
# or not 
    if len(results)==0:
        flash("These no brand steamer recipes, would you like to add one", "info")
        return render_template("404.html")
    else:
        flash("These are all the brand steamer recipes", "info")
        return render_template("filter.html", recipes=mongo.db.recipes.find({"required_tools": "brand steamer"}))

@app.route('/BGfilter')
def BGfilter():
    cur = mongo.db.recipes.find({"required_tools": "brand grill"})
    results = list(cur) 
# Checking the cursor is empty 
# or not 
    if len(results)==0:
        flash("These no the brand grill recipes, would you like to add one", "info")
        return render_template("404.html")
    else:
        flash("These are all the brand grill recipes", "info")
        return render_template("filter.html", recipes=mongo.db.recipes.find({"required_tools": "brand grill"}))

@app.route('/BCfilter')
def BCfilter():
    cur = mongo.db.recipes.find({"required_tools": "brand cooker"})
    results = list(cur) 
# Checking the cursor is empty 
# or not 
    if len(results)==0:
        flash("These no the brand cooker recipes, would you like to add one", "info")
        return render_template("404.html")
    else:
        flash("These are all the brand cooker recipes", "info")
        return render_template("filter.html", recipes=mongo.db.recipes.find({"required_tools": "brand cooker"}))

@app.route('/OUfilter')
def OUfilter():
    cur = mongo.db.recipes.find({"required_tools": "others unbranded"})
    results = list(cur) 
# Checking the cursor is empty 
# or not 
    if len(results)==0:
        flash("These no others unbranded recipes, would you like to add one", "info")
        return render_template("404.html")
    else:
        flash("These are all the others unbranded recipes", "info")
        return render_template("filter.html", recipes=mongo.db.recipes.find({"required_tools": "others unbranded"}))
#end of filter recipe code

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
