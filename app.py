"""
Underfloor Heating Mapper — a simple Flask web app.

How it works:
- When you visit the home page, Flask shows the upload form (index.html).
- When you pick an image and click "Upload", the browser sends the file to
  Flask, which saves it into the static/uploads/ folder.
- Flask then reloads the page and passes the filename to the template so it
  can display the uploaded image.
"""

import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Create the Flask application
app = Flask(__name__)

# Where uploaded images will be stored on disk
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Only allow these image types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    """Return True if the filename ends with an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Home page — shows the upload form and, if an image was just uploaded,
    displays that image below the form.
    """
    uploaded_image = None

    if request.method == "POST":
        # Check that the form actually included a file
        file = request.files.get("floor_plan")

        if file and file.filename and allowed_file(file.filename):
            # secure_filename cleans up the name to prevent security issues
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # Build the path the browser will use to fetch the image
            uploaded_image = url_for("static", filename=f"uploads/{filename}")

    return render_template("index.html", uploaded_image=uploaded_image)


if __name__ == "__main__":
    # Make sure the uploads folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # Start the development server (debug=True auto-reloads on code changes)
    app.run(debug=True)
