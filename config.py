"""config.py — Company branding & invoice settings."""

import os


class Config:
    # Company Branding
    COMPANY_NAME = "Apex Digital Solutions Inc."
    COMPANY_TAGLINE = "Enterprise Cloud & Software Systems"
    COMPANY_ADDRESS = "100 Innovation Blvd, Suite 400\nSan Francisco, CA 94107"
    COMPANY_EMAIL = "billing@apexdigital.io"
    COMPANY_PHONE = "+1 (800) 555-0199"

    # Invoice Formatting
    CURRENCY_SYMBOL = "$"
    TAX_RATE = 0.0825  # 8.25% Sales Tax
    PAYMENT_TERMS = "Payment Due within 30 Days of Issue."
    FOOTER_NOTE = "Thank you for your business! Please remit payment via wire transfer or scan the QR code."

    # Styling Palette (Hex codes)
    PRIMARY_COLOR = "#1A365D"    # Deep Navy
    SECONDARY_COLOR = "#2B6CB0"  # Accent Blue
    TEXT_DARK = "#2D3748"        # Dark Gray
    BG_LIGHT = "#EDF2F7"         # Light Gray Table Header

    # Directories
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"


os.makedirs(Config.INPUT_DIR, exist_ok=True)
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)