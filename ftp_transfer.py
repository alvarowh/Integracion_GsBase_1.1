from ftplib import FTP
import os
import time
import re
import fileinput


start=time.time()

ftp = FTP()
ftp.set_debuglevel(0)
ftp.connect('ftp.camanwi.com', 21)
ftp.login('imagesResources@camanwi.com', '1535nuTNT')

ftp.cwd('')


def ftp_upload(localfile):
    fp = open(localfile, 'rb')
    ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
    fp.close()



directorio_imagenes = "C:/Users/alvar/Documents/ferrer/Fotos/Product Creation/Formatted Images/"

# Leo los JPG del directorio local de imagenes
included_extensions = ['jpg']
images_names = [fn for fn in os.listdir(directorio_imagenes)
                if any(fn.endswith(ext) for ext in included_extensions)]



def upload_img(file):
    ftp_upload(directorio_imagenes + "/" + file, file)



#Obtengo lista de imagenes ya alojadas en el servidorsubidas.
def getUploadedImages():
    filelist=[]
    ftp.retrlines('LIST',filelist.append)
    ftp_image_list=[]
    for f in filelist:

        picture=(re.findall('(?=\S*$)(.*)', f))
        picture=picture[0]
        if any(picture.endswith(ext) for ext in included_extensions):
            ftp_image_list.append(picture)

    return ftp_image_list

def batch_image_upload(image_names_input):
    ftp_uploaded_images=getUploadedImages()
    for image in image_names_input:
        print(image)
        #if image not in ftp_uploaded_images:
        #    print(image + " uploaded")
        #    upload_img(image)
        #else:
        #    print("I am already uploaded")

ftp.quit()


end=time.time()
print(end-start)