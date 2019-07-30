from PIL import Image
import os
import re
import collections
import json
import ftp_transfer

directorio_input_image = "C:/Users/alvar/Documents/ferrer/Fotos/Product Creation/Raw Images/"
directorio_output_image = "C:/Users/alvar/Documents/ferrer/Fotos/Product Creation/Formatted Images/"



def changeImagesToJPG(directorio_input_image,directorio_output_image):

    image_dict= collections.defaultdict(list)

    for file in os.listdir(directorio_input_image):
        filename, file_extension = os.path.splitext(file)
        rootfile=re.findall('(^[0-9]+)_',filename)[0]

        if file_extension == ".jfif" :
            im = Image.open(directorio_input_image+filename+file_extension)
            im.save(directorio_output_image+filename+".jpg")
            image_dict[rootfile].append(filename + ".jpg")


        if file_extension == ".jpg":
            im = Image.open(directorio_input_image + filename + file_extension)
            im=im.convert("RGB")
            im.save(directorio_output_image + filename + ".jpg")
            image_dict[rootfile].append(filename + ".jpg")


        if file_extension == ".png" :
            im = Image.open(directorio_input_image+filename+file_extension)
            im=im.convert("RGB")
            im.save(directorio_output_image+filename+".jpg")
            image_dict[rootfile].append(filename + ".jpg")


    return image_dict

    with open(directorio_output_image+'image_data.json', 'w') as outfile:
        json.dump(image_dict, outfile)

image_list=changeImagesToJPG(directorio_input_image,directorio_output_image)

