#-*- encoding: utf8 -*-
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,FileResponse, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.conf import settings 
import base64
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os, shutil


# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload(request):
    if request.method == 'POST' and request.FILES['photo']:
        upload_file = request.FILES['photo']
        fullname = upload_file.name
        idx = fullname.index('.')
        filename = fullname[:idx]
        media_dir = 'media/page/files/'
        rm_file = media_dir + 'test.jpg'
        if os.path.isfile(rm_file):
            os.remove(rm_file)

        copy_file = 'static/test.jpg'
        if os.path.isfile(copy_file):
            os.remove(copy_file)
        fs = FileSystemStorage(location=media_dir)
        fs.save(upload_file.name, upload_file)
        os.rename(media_dir + fullname, media_dir + 'test.jpg')
        shutil.copy(media_dir+'/test.jpg', 'static/test.jpg')
        r, p = getResult()
        return render(request, 'show.html',{'result':r, 'prob':p*100, 'MEDIA_URL':settings.MEDIA_URL})
    return render(request, 'upload.html')
    

def webcam(request):
    return render(request, 'webcam.html')

def show(request):
    r, p = getResult()
    return render(request, 'show.html',{'result':r, 'prob':p*100, 'STATIC_URL':settings.STATIC_URL})

@csrf_exempt
def canvasToImage(request):
    data = request.POST.__getitem__('data')
    data = data[39:]
    data += '=' *(4 - len(data) % 4)
    path = 'media/page/files/'
    filename = 'test.jpg'
    image = open(path+filename, "wb")
    image.write(base64.b64decode(data))
    image.close()
    r, p = getResult()
    return render(request, 'show.html',{'result':r, 'prob':p*100, 'MEDIA_URL':settings.MEDIA_URL})

def getResult():
    poketmon=['꼬부기','이상해씨','파이리','버터플','뮤','푸린','마자용','나옹','디그다','야돈','고라파덕','꼬마돌','쥬레곤','뽀뽀라','또가스','고오스','잉어킹','메타몽','이브이','피카츄','잠만보','롱스톤','치코리타','브케인','리아코','토게피','데덴네','마릴','나몰빼미']
    width = 150
    height = 150
    img_jpg = Image.open('media/page/files/test.jpg')
    img_jpg = img_jpg.convert('RGB')
    resize_img = img_jpg.resize((width, height), Image.ANTIALIAS)
    input_data=img_to_array(resize_img)
    model = load_model('media/page/files/final_model.hdf5')
    name = poketmon[model.predict_classes(np.array([input_data]))[0]]
    # detail_model = load_model('media/page/files/detail_model/'+name+'.hdf5')
    # jpg_index = detail_model.predict_classes(np.array([input_data]))
    probability=max(model.predict(np.array([input_data]))[0])
    # index=jpg_index[0]
    return name,probability

    
    