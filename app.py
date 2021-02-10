from flask import Flask, render_template, redirect, request
import imageio
import requests
import matplotlib.pyplot as plt
import IPython.display as dp
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import random
import string

app = Flask(__name__)

@app.route('/')
def main_page():
  return render_template("index.html")

@app.route('/', methods=['POST'])
def to_sketch():
  if request.method == 'POST':
    # Simpan gambar yang sudah diupload
    gambar = request.files['gambar']
    nama_gambar = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))+gambar.filename
    image_path = "./static/images/before/"+nama_gambar
    gambar.save(image_path)
    
    #membalikkan warna dengan dikurangi dari 255
    gambar_sumber = imageio.imread(image_path)
    grayscale_img = grayscaleimg(gambar_sumber)
    inv_img = (255 - grayscale_img)

    #blurkan gambar
    blurred_img = scipy.ndimage.filters.gaussian_filter(inv_img, sigma=5)

    #Generate the target image by applying the dodge
    target_img= dodging(blurred_img, grayscale_img)

    #Save the image
    sketch_path = "./static/images/after/"+nama_gambar
    plt.imsave(sketch_path, target_img, cmap='gray', vmin=0, vmax=255)

  return render_template("index.html", gambar = nama_gambar)

def grayscaleimg(rgb): 
  # Proses perubahan warna ke hitam putih
  #rumusnya Y= 0.299*R + 0.587*G + 0.114*B (greyscale)
  return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


#Create function to perform dogding(belnding together greyscale and blurred image)
def dodging(blur_img, gryscl_img):
    resultant_dodge=blur_img*255/(255-gryscl_img) 
    resultant_dodge[resultant_dodge>255]=255
    resultant_dodge[gryscl_img==255]=255
    return resultant_dodge.astype('uint8')

if __name__ == '__main__':
  app.run(debug = True)