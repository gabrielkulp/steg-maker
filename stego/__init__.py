# Application factory and Python's package marker
from flask import Flask
import os, subprocess, atexit, shutil

TMP_DIR = "/tmp/stego"

def create_app():
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	
	# configuration
	app.instance_path = "instance"
	app.config["UPLOAD_FOLDER"]   = os.path.join(app.instance_path, "uploads")
	app.config["DOWNLOAD_FOLDER"] = os.path.join(app.instance_path, "downloads")
	app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
	app.config["ALLOWED_EXTENSIONS"] = {"jpg", "jpeg", "bmp"}
	
	if not (os.path.islink(app.instance_path) and os.path.exists(os.readlink(app.instance_path))):
		#TMP_DIR = subprocess.run(["mktemp", "-d"], encoding="utf-8", capture_output=True).stdout.strip()
		print("got this far")
		if not os.path.isdir(TMP_DIR):
			os.makedirs(TMP_DIR)

		print("using", TMP_DIR, "as instance path")
		if os.path.islink(app.instance_path):
			os.unlink(app.instance_path)
		os.symlink(TMP_DIR, app.instance_path)

		os.makedirs(app.config['UPLOAD_FOLDER'])
		os.makedirs(app.config['DOWNLOAD_FOLDER'])

	from . import views
	app.register_blueprint(views.bp)
	app.add_url_rule("/", endpoint="home")
	app.add_url_rule("/home", endpoint="home")
	app.add_url_rule("/embed", endpoint="embed")
	app.add_url_rule("/extract", endpoint="extract")
	app.add_url_rule("/return-image", endpoint="return_image")
	app.add_url_rule("/return-message", endpoint="return_message")

	atexit.register(cleanup, app=app)

	return app

def cleanup(app):
	print(f"removing {app.instance_path} -> {os.readlink(app.instance_path)}")
	if os.path.islink(app.instance_path) and os.path.exists(os.readlink(app.instance_path)):
		shutil.rmtree(os.readlink(app.instance_path))
