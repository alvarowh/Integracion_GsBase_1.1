import ftplib
import os

directorio_imagenes = "C:/Users/alvar/Documents/ferrer/Fotos/Product Creation/Formatted Images/"

session = ftplib.FTP('ftp.camanwi.com','imagesResources@camanwi.com','1535nuTNT')

# Leo los JPG del directorio local de imagenes
included_extensions = ['jpg']
images_names = [fn for fn in os.listdir(directorio_imagenes)
                if any(fn.endswith(ext) for ext in included_extensions)]

for image in images_names:
    file = open(directorio_imagenes+image,'rb')                  # file to send
    session.storbinary('STOR'+image, file)     # send the file
    print(image+ " uploaded")
    file.close()                                    # close file and FTP
session.quit()







