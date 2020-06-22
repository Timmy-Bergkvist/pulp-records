
# pulp-records
A record collection and recommendation site.


**Target Audience**

  Pulp Records is a website for people who like music and want to share their favorite records.
  The website provides user with information about various music records, description and a tracklist.
  On the platform there will be an option to create an account to add music records.

## UX

**Project sections:**

  - Homepage: Containing a welcome message to sign up to the account with a logo and some info at the bottom.
  
  - Sign up form: Containing a form that enables user to sign up for the app.

  - Login form: Containing a form that enables user to login for the app.
  
  - Add Record: Containing a form that enables user to add a record with information.
  
  - Profile: Containing user information and the options to delete and edit the acount.
  
  - Records: A page displaying all the records.
  
  - View Record: A page that contains all the information, reviews and a link to buy the record.

**User Stories**

As a user of this platform, I will be able to:

  - Access the platform from a desktop, tablet and a smartphone.
  
  - Have an option to login and logout of the account.
  
  - Have an option to delete and edit records of the user account.
  
  - Have an option to delete user account.
  
  - Have an option to upload a record with information about the band.
  
  - 

**Mockups**
  
  I have used Figma Mockups to visualize images I can work from.

- <a href="" target="_blank">Desktop</a>

- <a href="" target="_blank">Phone</a>

- <a href="" target="_blank">Tablet</a>


## Features

**Existing Features**

- A registration form to sign up for the application.

- A login form to access the application.

- A personal profile page where the user can display his or hers added records.

- A delete profile button to delete the user account and the records added by the user.

- A edit and delete record function to update and delete the users records.

- A nav bar that displays a Logo, Home, Records, Add Records, Profile and Login Log out urls.

- Toast messages to highlight different right, wrong and info actions for the users.

**Features Left to Implement**

- A comment section to comment others records.

- A edit user function to edit the username or email.

- To set up a linkt to buy the records.

- A search function to search for record title and artist.

- Alerts popups to give the user a yes or no option, for delete and update.

- An implementation to add new genres for other music alternatives.

- A record selection function to select the genre so only that specific music records will be displayed.

## Technologies Used

**Language**

- <a href="https://en.wikipedia.org/wiki/HTML" target="_blank"> Html </a>
  
- <a href="https://en.wikipedia.org/wiki/Cascading_Style_Sheets" target="_blank"> Css </a>

- <a href="https://en.wikipedia.org/wiki/JavaScript" target="_blank"> JavaScript </a>

- <a href="https://en.wikipedia.org/wiki/Python_(programming_language)" target="_blank"> Python </a>

**Libraries**

- <a href="https://palletsprojects.com/p/jinja/" target="_blank"> Jinja</a>

- <a href="https://github.com/mongodb/mongo-python-driver" target="_blank"> PyMongo </a>

**Framework**

- <a href="https://en.wikipedia.org/wiki/Flask_(web_framework)" target="_blank"> Flask </a>

- <a href="https://materializecss.com/" target="_blank"> materializecss </a>

**Other**

- <a href="https://en.wikipedia.org/wiki/Heroku" target="_blank"> Heroku </a>

- <a href="https://code.visualstudio.com/" target="_blank"> VS Code </a>

- <a href="https://www.figma.com/" target="_blank"> Figma </a>
  
## Database structure

I have used Mongodb database for this project
- <a href="https://www.mongodb.com/cloud/atlas" target="_blank"> Mongodb </a>

![Image of database](https://timmy-bergkvist.github.io/pulp-records/static/images/database-structure.jpg)

 **Collection Name:**
 genre, recordCollection, users.
 
 **recordCollection**
 ```shell
  {
    _id: ObjectID(String),
    genre_name: String,         // Genre
    artist_name: String,        // Name of the artist or band
    record_title: String,       // Name of the record
    image_id: String,           // Url for image
    added_by: String,           // Added by user
    record_description: String, // Description of the record
    tracklist: String           // Tracklist for the record
  }
 ```
 
 **users**
 ```shell
  {
    _id: ObjectID(String),
    username: String,           // User name to register
    email: String,              // User email to register
    password: Binary(String),   // method='sha256'
  }
 ```
 
 **genre**
 ```shell
  {
    _id: ObjectID(String),
    genre_name: string,         // Genre
  }
 ```


## Testing 

  - The responsive is run and tested at:
    - http://ami.responsivedesign.is/#

  - The HTML code is run and tested at:
    - https://validator.w3.org/#validate_by_input
  
  - The CSS code is run and tested at:
    - https://jigsaw.w3.org/css-validator/#validate_by_input
    
  - The JavaScript is run and tested at:
    - https://jshint.com/  
    
  - The Python is run and tested at:
    - http://pep8online.com/
  

  - text
  
  - text

 
 
  - Bugs
    ```shell
       bug fix so collapsible header will stay and not bounce back up.
       
       document.getElementById("recordfix").addEventListener("click", function(e) {
       e.stopPropagation();
       });
    ```
  
## Deployment
  
To run this project you need the following tools installed:

  - <a href="https://www.python.org/downloads/" target="_blank"> Python3 </a>
  - <a href="https://code.visualstudio.com/" target="_blank"> VS Code </a> or a code editor that have a debug tool.
  - <a href="https://www.mongodb.com/cloud/atlas" target="_blank"> MongoDB </a>
  - <a href="https://git-scm.com/" target="_blank"> Git </a>
  - <a href="https://en.wikipedia.org/wiki/Heroku" target="_blank"> Heroku </a>

**Local deployment**

The following instructions are based on Windows 10 and VS Code editor.

> Instructions:

  I.    Clone the repository in Github
 ```shell
  git clone <repository name>.git
 ```
    
  II.   create a virtual environment with the command:
```shell
 python -m venv env
```

  III.   Activate an environment
```shell

virtualenv env
source env/bin/activate

For more information:
https://code.visualstudio.com/docs/python/environments
```

  IV.   Install all the package that's needed
```shell
pip install Flask
pip install pymongo
pip install dnspython
pip install Flask-PyMongo
```

  VI.   Create a database in MongoDB Atlas
`https://www.mongodb.com/`

  VII.   Create a .env file with your credentials: e.g
```shell
MONGO_URI="insert your mongo URI"
SECRET_KEY="insert your secret key here"
```
    
  VIII.   Run the application
```shell
python app.py

Open the website at http://127.0.0.1:5000
```

**Heroku deployment**
    
This project is hosted using Heroku.

> Instructions:

I.    Install Heroku
  
```shell
       npm install -g heroku
       heroku login
       cd my-project/
       git init
       
       Existing Git repository:
       heroku git:remote -a <app name>
```

II.    Generate a requirements file and then install from it in another environment.

 ```shell
       pip freeze > requirements.txt
 ```
    
III.   Create a Procfile

 ```shell
       echo web: python app.py > Procfile
 ```
 
 IV.   Deploy your application to Heroku

 ```shell
       git add .
       git commit -am "make it better"
       git push heroku master
       
       Existing Git repository:
       heroku git:remote -a <app name>
 ```
    
V.    Set the environment variables on your Heroku settings.

 ```shell
       MONGO_URI="mongodb+srv://<USER NAME>:<SECRET KEY HERE>@mycluster-pcvdt.mongodb.net/<DATABASE NAME>?retryWrites=true&w=majority
       IP="0.0.0.0"
       PORT="5000"
 ```
    
## Credits
  
   **media**
  - The photos used in this site were obtained from:
    - https://www.discogs.com/

    - https://pixabay.com/sv/

   **Acknowledgements**
  - Inspiration for this project was obtained from:
    
