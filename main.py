from flask import Flask, render_template, url_for, request, flash, redirect
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from colorthief import ColorThief
import os

UPLOAD_FOLDER = 'static/' 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) 
 
app = Flask(__name__) 
app.secret_key = 'dsad'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
Bootstrap(app)

 

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        # check if the post request has the file part 
        file = request.files['image'] 

        # if user does not select file, browser also 
        # submit an empty part without filename 
        if file.filename == '':
            print('No selected file') 
            return redirect(request.url) 
        
        filename = secure_filename(file.filename) 
        flash('file {} saved'.format(file.filename)) 
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path) 
        color_num = int(request.form['colors_number'])
        color_thief = ColorThief(path)
        palette = color_thief.get_palette(color_count=color_num - 1)
        return render_template('index.html', palette=palette, img_source=url_for('static', filename=filename))
    
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
