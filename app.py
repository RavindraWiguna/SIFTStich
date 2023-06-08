from flask import Flask, request, jsonify, render_template, redirect, session, flash, send_from_directory
from flask_session import Session
from backend.Stitcher import Stitcher
from backend.cv_util import *
from backend.security import *
import os
import cv2 # for example

app = Flask(__name__, static_folder='public')

# set where the upload folder inside instance folder (idk keknya harus instance?)
uploads_folder = 'uploads'
results_folder = 'results'
# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, uploads_folder), exist_ok=True)
# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, results_folder), exist_ok=True)
# set so that session have time out
app.config["SESSION_PERMANENT"] = False
# set tipe session is filesystem ( since we dont use db )
app.config["SESSION_TYPE"] = "filesystem"

# so that each user have their own unique session for our app
Session(app)

@app.route('/')
def home():
    return render_template('./index.html')


@app.route('/result', methods=['GET'])
def showResultPage():
    if(not session.get('totalimg')):
        flash("You haven't upload yet")
        redirect('/')
    
    # ok udah ada
    return render_template('result.html', imgSources=session.get('fileNames'), resultfileName=session.get('resultfileName'))

@app.route('/uploads/<path:filename>')
def showStaticUpload(filename):
    return send_from_directory(os.path.join(app.instance_path, uploads_folder),
                               filename, as_attachment=True)

# sama aja si benernya, cuma tak bedain aja sama upload si result
@app.route('/result/<path:filename>')
def showResultImage(filename):
    return send_from_directory(os.path.join(app.instance_path, results_folder),
                               filename, as_attachment=True)

# stitch dengan nge set img height to min height
def doStichVersi1(imgPaths):
    # read the example img
    imgs = [cv2.imread(path) for path in imgPaths]

    # find min height
    min_height = min(img.shape[1] for img in imgs)
    # resize it to the same height (requirement for stitching)
    resized = [resizeHeight(img, min_height) for img in imgs]

    stitcher = Stitcher()
    res = stitcher.stitch(resized, showMatches=True)

    if res is not None:
        (result, vis) = res
        # now save it to disk
        fileName = create_random_name(32)
        fullName = f'{fileName}.png'
        filePath = f'./instance/results/{fullName}'
        cv2.imwrite(filePath, result)
        # print('DIDDDD')
        return fullName
    
    return None
    


@app.route('/upload', methods=['POST'])
def handleUpload():
    totalImage = request.form['totalimg']
    totalImage=int(totalImage)
    files = []
    for i in range(totalImage):
        image = request.files[f'img{i+1}']
    
        if image.filename == '':
            flash('Some photo are not selected yet, Please select all photo')
            return redirect('/')

        if(not isAllowedExtension(image.filename)):
            flash('Some of photo extension are not allowed')
            return redirect('/')

        files.append(image)
    
    # simpen dulu all photo
    filePaths = []
    fileNames = []
    for image in files:
        fileName = create_random_name(32)
        extension = image.filename.rsplit('.', 1)[1] # rsplit split the string from right, and 1 is the maxsplit, so it will be [name, extension]
        fullName = f'{fileName}.{extension}'

        fullPath = os.path.join(app.instance_path, uploads_folder, fullName)
        image.save(fullPath)
        fileNames.append(fullName)
        filePaths.append(fullPath)

    session["totalimg"] = totalImage
    session['fileNames'] = fileNames

    # stitch it and save the location to the session
    resultfileName = doStichVersi1(filePaths)

    if resultfileName is None:
        flash('Keypoint matches is not enough. Images can\'t be stitched')
        return redirect('/')

    session['resultfileName'] = resultfileName
    return redirect('/result')

    # print(request.data) (kosong)
    # print('---')
    # print(request.values) (all value except files)
    # print('----')
    # print(request.form) (one of the value, and isi dari form)
    # print('---')
    # print(request.files) ( all files)
    # print('---')
    # return redirect('/')

# @app.route('/test', methods=['POST'])
# def testImg():
#     # read the example img
#     imageA = cv2.imread('example_img/first/canyon.jpg')
#     imageB = cv2.imread('example_img/second/canyon.jpg')

#     # resize it to the same width (requirement for stitching)
#     imageA = resizeWidth(imageA, targetWidth=400)
#     imageB = resizeWidth(imageB, targetWidth=400)

#     # now match them height, same a requirement too
#     imageA, imageB = matchHeight([imageA, imageB])

#     stitcher = Stitcher()
#     (result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

#     # now save it to disk
#     fileName = create_random_name(32)
#     filePath = f'./public/results/{fileName}.png'
#     cv2.imwrite(filePath, result)
#     # print('DIDDDD')
#     return jsonify({'src':filePath})




if __name__ == '__main__':
    app.run()
