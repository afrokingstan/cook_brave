# COOKBRAVE

This is an online cookbook where external users can find and share recipes. While the owner's goal is to promote a brand of cooking tools (e.g. oven, pressure cooker, etc.) as recommended tools for each recipe. the selling point is that external users benefit from a free recipe book while the site owner benefits from the avaliability of the opportunity to promote a brand of cooking tools.

 
## UX
 
- As a external user, I want to be able to find and share recipes, so that I can try new recipes, ingredients and cooking tools.
- As a site owner, I want to promote a brand of cooking tools, so that I can encourage external user to buy and use my promoted cooking tools to achieve their goals in cooking through the free recipes.

## Features

- Feature 1 - Users are allowed to store and easily access cooking recipes.
- Feature 2 - Backend code and frontend form to allow users to add new recipes to the site, edit them and delete them.
- Feature 3 - Backend and frontend functionality for users to locate recipes based on the recipe's fields.


### Existing Features
- Feature 1 - Users are allowed to easily access cooking recipes, by having them make use of the navigation menu and the recommended cooking tools filter.
- Feature 2 - allows users to add new recipes to the site, to achieve storing and sharing recipes with other users, by having them upload a recipe image and fill out a form
- Feature 3 - allows users to edit and delete recipes on the site,  to achieve updating and deleting recipes, by having them edit and delete recipe data using dedicated forms
- Feature 4 - frontend functionality for users to easily locate recipes based specific criteria, to achieve recipe filter, by having them use the Cuisines navigation menu and the recommended cooking tools links.

### Features Left to Implement
Additional features to be implemented in the future:
- A full search functionality
- A dashboard to provide some statistics about all the recipes.
- A like and ratings feature for each recipe
- A login to delete and edit recipe recipes 

### Features Left to Implement
Additional features to be implemented in the future:
- A full search functionality
- A dashboard to provide some statistics about all the recipes.
- A like and ratings feature for each recipe
- A login to delete reciepes 

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
    - The project uses **HTML** to define the meaning and structure of web content.
- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
    - The project uses **Javascript** to program how the some form elements behaviour and value on the occurrence of an event.
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
    - The project uses **CSS** to describes how elements and document written in HTML should be presented on screen.
- [Bootstrap](https://getbootstrap.com/)
    - The project uses **Bootstrap** to quickly design and customize responsive mobile-first sites.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
    - The project uses **Flask** as a web frame work to python.
- [Python](https://wiki.python.org/moin/)
    - The project uses **Python** to configure server side system and create, read, update and delete data.
- [MongoDB](https://www.mongodb.com/)
    - The project uses **MongoDB** to store recipe data online.
- [Flask-Pymongo](https://flask-pymongo.readthedocs.io/en/latest/)
    - The project uses **Flask-Pymongo** to bridges Flask and PyMongo and provides some convenience helpers.
- [Heroku](https://www.heroku.com/)
    - The project uses **Heroku** to simplify the processes of deploying, configuring, scaling, tuning, and managing apps .
- [Github](https://github.com/)
    - The project uses **Github** to simplify version control, code reviews.
- [Gitpod](https://www.gitpod.io/)
    - The project uses **Gitpod** to simplify remote working.
- [Visualcode](https://code.visualstudio.com/)
    - The project uses **Visualcode** to simplify local machine working and code editing.
- [Anaconda Navigator](https://www.anaconda.com/)
    - The project uses **Anaconda Navigator** to simplify local server and app testing.


## Testing

1. add recipe form:
    1. Go to the "Add" recipe page by selecting the Add menu in the Recipe navigation menu and verify a flash message informs of what you can do.
    2. Try to upload the empty form and verify that an error message about the required fields appears
    3. After successfull upload of recipe image check to see if you are now on a the add recipe form and the name of the uploaded file is prepopulated on the new form.
    4. Try to submit the empty form and verify that an error message about the required fields appears
    5. Try to submit the form with an empty fields and verify that a relevant error message appears
    6. Try to submit the form with an empty required tools and verify that a relevant error message appears
    7. Try to submit the form with all inputs valid and verify that a success message appears.

2. Edit recipe form:
    1. Go to the "Edit" recipe page by selecting the Edit menu in the Recipe navigation menu and verify a flash message informs of what you can do.
    2. Select a recipe you want to edit by clicking the "EDIT" button Try to edit the recipe form and verify that an information message about the submitted form appears.

3. Delete recipe form:
    1. Go to the "Delete" recipe page by selecting the Delete recipe menu in the Recipe navigation menu and verify a flash message informs of what you can do.
    2. Select a recipe you want to delete by clicking the "Delete" button Try to delete the recipe form and verify that an information message about this action appears.

interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.
- Undefined variable 'all_cuisines'
- Unused variable 'all_cuisines
- testing codes locally
these were resolved during the testing stage of this project.

## Deployment
After testing is done and the project is ready for deployment I committed all changes to github and deployed the project on Heroku
differences between the deployed version and the development version, includes :
- Different values for environment variables ? Heroku Configuration Var included the MONGOURI and password
- Different configuration files? During deployment the app.py file included port and IP to match that on Heroku 
- Deployment method in Keroku - Github

In addition, how to run my code locally.
- locally : I would ensure that Anaconda Navigator is started and Visual code is started from this enviroment. Then I will ensure my .env file is present next I will proceed to run the app.py file in Visual code and view it rendered on the web browser http://127.0.0.1:5000/ 


## Credits

### Content
- The text for section Y was copied from the [thehappyfoodie](https://thehappyfoodie.co.uk/)

### Media
- The photos used in this site were obtained from [pixabay](https://pixabay.com/)

### Acknowledgements

- I received inspiration for this project from the project Example idea 1 of [codeinstitute](https://courses.codeinstitute.net) - Data Centric Development Milestone Project.
- I received UI design inspiration for this project from my mentor Reuben Ferrante.
