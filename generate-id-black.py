import qrcode
from PIL import Image


def create_qr_code_with_logo(
    url,
    logo_path,
    top_image_path=None,
    qr_size=290,
    logo_size=130,
    top_image_scale=1.0,
    extra_padding=100,
):
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

    logo = Image.open(logo_path)
    logo = logo.convert("RGBA")
    logo = logo.resize((logo_size, logo_size))

    x = (qr_img.width - logo.width) // 2
    y = (qr_img.height - logo.height) // 2

    qr_img.paste(logo, (x, y), logo)

    if top_image_path:
        top_image = Image.open(top_image_path).convert("RGBA")
        scaled_width = min(int(width * top_image_scale), width)
        scaled_height = int(scaled_width * top_image.height / top_image.width)
        top_image = top_image.resize((scaled_width, scaled_height))

        top_image_with_bg = Image.new("RGBA", (width, scaled_height), (0, 0, 0, 255))
        offset_x = (width - scaled_width) // 2
        top_image_with_bg.paste(top_image, (offset_x, 0), top_image)
    else:
        top_image_with_bg = Image.new(
            "RGBA", (width, int(width * top_image_scale)), (0, 0, 0, 255)
        )

    padding_area = Image.new("RGBA", (width, extra_padding), (0, 0, 0, 255))

    combined_height = height + top_image_with_bg.height + extra_padding
    combined_img = Image.new("RGBA", (width, combined_height), (0, 0, 0, 255))
    combined_img.paste(padding_area, (0, 0))
    combined_img.paste(top_image_with_bg, (0, extra_padding))
    combined_img.paste(qr_img, (0, top_image_with_bg.height + extra_padding))

    return combined_img


url = "https://github.com/J11tendra/"
logo_path = "./assets/new-kuru.png"
top_image_path = "./assets/kuru-white.png"
qr_img = create_qr_code_with_logo(url, logo_path, top_image_path, top_image_scale=0.85)
qr_img.save("./Id-cards/black-id-card.png")
