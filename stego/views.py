from flask import (
	Blueprint, g, redirect, render_template, request,
	url_for, abort, current_app,send_from_directory
)
from werkzeug.exceptions import abort
import urllib.request, urllib.error
import os, hashlib
from . import steganography

bp = Blueprint('views', __name__)

@bp.route("/")
@bp.route("/home")
def home():
	return render_template("home.html")


@bp.route("/embed", methods=["GET", "POST"])
def embed():
	if (request.method == "GET"):
		return render_template("embed.html")
	
	upload = request.files["file"]
	message = request.form["message"]
	passphrase = request.form["passphrase"]
	
	if not (upload and message and passphrase):
		print("incomplete request")
		abort(400)

	path = safe_save(upload, current_app.config['UPLOAD_FOLDER'])
	if not path:
		msg = "Unsupported file format. Only JPEG and BMP!"
		return render_template("error.html", message=msg)

	try:
		return_name = steganography.embed(path, message, passphrase, current_app.config['DOWNLOAD_FOLDER'])
	except (Exception, RuntimeError) as e:
		print(str(e))
		if type(e) == RuntimeError:
			return render_template("error.html", message=str(e))
		else:
			abort(500)

	if not return_name:
		return render_template("error.html", message="bad embed")

	return redirect(url_for("views.return_image", filename=return_name))


@bp.route("/extract", methods=["GET", "POST"])
def extract():
	if request.method == "GET":
		return render_template("extract.html")
	
	upload = request.files["file"]
	passphrase = request.form["passphrase"]
	
	if not ('file' in request.files and passphrase and upload):
		print("incomplete request")
		abort(400)

	path = safe_save(upload, current_app.config['UPLOAD_FOLDER'])
	if not path:
		msg = "Unsupported file format. Only JPEG and BMP!"
		return render_template("error.html", message=msg)
	
	try:
		message = steganography.extract(path, passphrase)
	except Exception as e:
		if type(e) == RuntimeError:
			return render_template("error.html", message=str(e))
		else:
			abort(500)

	if not message:
		return render_template("error.html", message="bad extract")

	return render_template("return-message.html", message=message)


def safe_save(upload, directory):
	if not upload or not upload.filename:
		print("no file or no filename")
		return None
	
	# get extension
	ext = upload.filename.split(".")[-1]

	if ext not in current_app.config["ALLOWED_EXTENSIONS"]:
		print("not an allowed extension:", ext)
		return None

	# pick a filename and location for saving
	filename = hashlib.md5(upload.read()).hexdigest() + "." + ext
	path = os.path.join(directory, filename)
	
	# check if it's already been uploaded
	if not os.path.isfile(path):
		upload.seek(0) # reset position in file after hashing
		upload.save(path)
	else:
		print("already exists")

	return path


# serve the raw image
@bp.route("/download/<filename>")
def download(filename):
	directory = os.path.join("..",current_app.config["DOWNLOAD_FOLDER"])
	return send_from_directory(directory, filename)

# serve image with pretty frame
@bp.route("/return-image/<filename>")
def return_image(filename):
	return render_template("return-image.html", filename=filename)
