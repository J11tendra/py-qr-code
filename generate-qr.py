import qrcode
from PIL import Image


def create_qr_code_with_logo(url, logo_path, qr_size=290, logo_size=130):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="rgb(213,68,39)", back_color="black")
    qr_img = qr_img.convert("RGBA")

    width, height = qr_img.size
    pixels = qr_img.load()

    corner_size = 7

    for x in range(corner_size):
        for y in range(corner_size):
            pixels[x, y] = (0, 0, 0, 255)

    for x in range(width - corner_size, width):
        for y in range(corner_size):
            pixels[x, y] = (0, 0, 0, 255)

    for x in range(corner_size):
        for y in range(height - corner_size, height):
            pixels[x, y] = (0, 0, 0, 255)

    logo = Image.open(logo_path)
    logo = logo.convert("RGBA")
    logo = logo.resize((logo_size, logo_size))

    x = (qr_img.width - logo.width) // 2
    y = (qr_img.height - logo.height) // 2

    qr_img.paste(logo, (x, y), logo)

    return qr_img


url = "https://github.com/J11tendra/"
logo_path = "./assets/new-kuru.png"
qr_img = create_qr_code_with_logo(url, logo_path)
qr_img.save("qr_code_with_logo_and_black_corners-1.png")
