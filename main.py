import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import uuid

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    
    if request.method == "POST":
        
        desc = request.form.get('text')
        rec_id = request.form.get('uuid')
        duration = 1
        
        for key, value in request.files.items():
            print(key, value)
            
            file =  request.files[key]
            filename = secure_filename(file.filename)
            if not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], rec_id))):
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], rec_id))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, filename))
            
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "input.txt"), "a") as f:
                f.write(f"file '{filename}'\n")
                f.write(f"duration {duration}\n")
            
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"), "w") as f:
            f.write(desc)
                      
    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    print(reels)
    reels_user = [(i, i[:-4]) for i in reels]
    print(reels_user)
    return render_template("gallery.html", reels=reels_user)

app.run(debug=True)