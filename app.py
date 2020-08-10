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




app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_manager'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)
#start of session key generator to ensure falsh message is displayed
secret = secrets.token_urlsafe(32)
app.secret_key = secret
#end of session key generator

#start of file upload file handling 
##############################################
UPLOAD_FOLDER = '/Users/sttec/OneDrive/full stack dev/data project/cook_brave/static/uploads'
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
    
#######################################################################
#end of file upload file handling

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





@app.route('/uploadshome')
def uploadshome():
    return render_template("upload_image.html")





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

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())

#end of all recipe home page code




# start of edit recipe codes 
@app.route('/editrecipe_home')
def editrecipe_home():
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

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            debug=True)
