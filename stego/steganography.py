import os, subprocess, shutil, hashlib


def embed(filename, message, passphrase, out_dir):
	outfile = os.path.join(out_dir, os.path.basename(filename))
	shutil.copyfile(filename, outfile)
	
	p = subprocess.run(["steghide", "embed", "--coverfile", outfile, "--passphrase", passphrase], input=message, encoding="utf-8", capture_output=True)

	if p.returncode == 0:
		with open(outfile, "rb") as f:
			ext = "." + filename.split(".")[-1]
			new_out = hashlib.md5(f.read()).hexdigest() + ext
			os.rename(outfile, os.path.join(out_dir, new_out))
		return new_out
	else:
		print("Something went wrong with steghide:", p.stderr)
		if "file format" in p.stderr:
			raise RuntimeError("File contents was not as expected")
		return None


def extract(filename, passphrase):
	tmp_file = subprocess.run(["mktemp"], encoding="utf-8", capture_output=True).stdout.strip()
	print("temp file:", tmp_file)

	p = subprocess.run(["steghide", "extract", "--stegofile", filename, "--extractfile", tmp_file, "--force", "--passphrase", passphrase], encoding="utf-8", capture_output=True)

	if p.returncode == 0:
		with open(tmp_file, "r") as f:
			message = f.read()
		return message
	else:
		print("Something went wrong with steghide:", p.stderr)
		if "could not extract" in p.stderr:
			raise RuntimeError("No message found with that passphrase")
		return None
