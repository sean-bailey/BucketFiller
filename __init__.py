'''
general idea:
Use flask to connect to s3

upload, list, download, delete, all in an easy ui with minimal configuration.


'''

from flask import Flask, render_template, request, redirect, Response
from flask import make_response, send_file
#from werkzeug.security import secure_filename
from werkzeug import secure_filename
from helpers import *
app = Flask(__name__)
# app.config.from_object("flask_s3_upload.config")
app.config.from_object("config")


@app.route('/download/<objectname>')
def download_object_to_user(objectname):
    #TODO: fix this as it was for demo purposes
    if not objectname == "No":

        objectsize = get_object_size(objectname, app.config["S3_BUCKET"])
        print("printing getobject")
        print(get_object(objectname, objectsize, app.config["S3_BUCKET"]))
        print("done printing getobject")
        #myfile = get_object(objectname, objectsize, app.config["S3_BUCKET"])
        # return send_file(myfile, as_attachment=True, attachment_filename=objectname)
        return Response(
            get_object(objectname, objectsize, app.config["S3_BUCKET"]),
            mimetype='application/octet-stream',
            headers={"Content-Disposition":
                     "attachment;filename=%s" % objectname}
        )
    else:
        return redirect("/list")


@app.route("/delete/<objectname>")
def file_deletion(objectname):
    if not objectname == "No":
        delete_object(objectname, app.config["S3_BUCKET"])
        return redirect("/list")
    else:
        return redirect("/list")


@app.route("/upload", methods=["POST"])
def upload_file():

    if "user_file[]" not in request.files:
        return "no user file key in request.files"
    filelist = request.files.getlist("user_file[]")
    print(filelist)
    print(len(filelist))
    outputarray = []

    for file in filelist:
        print(file.filename)
        """
            These attributes are also available

            file.filename               # The actual name of the file
            file.content_type
            file.content_length
            file.mimetype

        """
        if file.filename == "":
            return "Please select a file"

        elif file.filename != "":  # and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            output = upload_file_to_s3(file, app.config["S3_BUCKET"])
            # return str(output)
            print(str(output))
            outputarray.append(str(output))
        else:
            return redirect("/upload")
    return str(outputarray)


@app.route('/')
def index():
    return render_template("index.html", bucketname=app.config["S3_BUCKET"])


@app.route('/list')
def list_contents():
    linkdict = list_contents_of_bucket(app.config["S3_BUCKET"])
    if linkdict is None or len(linkdict) < 1:
        linkdict = {}
        linkdict[''] = "No Data In Bucket."
    return render_template("listfiles.html", linkdict=linkdict)


@app.route('/upload')
def upload_file_page():
    return render_template("multifileuploader.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
