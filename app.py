import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from fastai.vision import *

UPLOAD_FOLDER = os.path.join('static','image')
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
path = pathlib.Path('./models/')

def get_image(filename):
	img_src = os.path.join(app.config['UPLOAD_FOLDER'],filename)
	defaults.device = torch.device('cpu')
	img = open_image(img_src)
	learn = load_learner(path)
	pred_class,pred_idx,outputs = learn.predict(img)
	return render_template('output.html',output=pred_class)

def allowed_file(filename):
    	return '.' in filename and \
        	filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            img_src = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            img = open_image(img_src)
            learn = load_learner(path)
            pred_class,pred_idx,outputs = learn.predict(img)
            return render_template('output.html',output=pred_class)
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
	app.run(debug=True)
