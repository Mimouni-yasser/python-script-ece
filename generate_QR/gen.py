import sys
import qrcode
from PIL import Image

if(__name__ == '__main__'):
    
    if(len(sys.argv) != 2):
        print("Usage: python gen.py <id>")
        exit(-1)

    logo_path = 'C:\\Users\\Yasser Mimouni\\OneDrive\\Desktop\\python script ece\\generate QR\\logo.jpg'
    logo = Image.open(logo_path)
    basewidth = 150
    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS )
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H)

    # taking url or text
    id = sys.argv[1]
    QRcode.add_data(id)
    # generating QR code
    QRcode.make()

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=(144, 62, 61), back_color="white").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    img_name = "qr_"+sys.argv[1]+".png"
    QRimg.save('C:\\Users\\Yasser Mimouni\\OneDrive\\Desktop\\python script ece\\generate QR\\generated_qr\\'+img_name)

