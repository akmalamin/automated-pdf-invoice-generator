"""engine/qr_generator.py — Creates dynamic QR codes for PDF embedding."""

import os
import qrcode
from config import Config


class QRGenerator:
    """Generates verification/payment QR codes as temporary images."""

    @staticmethod
    def generate(data_string, filename="qr_temp.png"):
        output_path = os.path.join(Config.OUTPUT_DIR, filename)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=1,
        )
        qr.add_data(data_string)
        qr.make(fit=True)

        img = qr.make_image(fill_color=Config.PRIMARY_COLOR, back_color="white")
        img.save(output_path)
        return output_path