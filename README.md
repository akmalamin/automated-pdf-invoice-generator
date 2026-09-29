# 📄 Automated PDF Invoice & Receipt Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Engine: ReportLab](https://img.shields.io/badge/Engine-ReportLab-red.svg)](https://www.reportlab.com/)
[![Code Style: Clean Architecture](https://img.shields.io/badge/Architecture-Modular-green.svg)]()

An enterprise-grade, automated PDF billing and invoice engine built with Python. Ingests raw batch order spreadsheets (CSV/Excel), computes taxes, subtotals, and line-item totals with precision, and programmatically compiles branded, vector-sharp PDF invoices with dynamic QR code verification.

---

## 🌟 Key Features

- **🚀 Batch Order Processing:** Automatically groups multi-line items by `invoice_id` and customer profile.
- **📐 Pixel-Perfect Typography (ReportLab PLATYPUS):** Engineered with professional corporate color palettes, auto-wrapping table cells, alternating grid borders, and executive headers.
- **🧮 Automated Financial Math:** Dynamically calculates line totals, customizable state/regional tax percentages, and grand totals with zero floating-point calculation errors.
- **📱 Real-Time Scannable QR Codes:** Embeds dynamic QR codes linking to payment gateways or instant invoice verification metadata.
- **🏢 Fully Customizable Branding:** Easy centralized configuration for company logos, names, addresses, payment terms, and custom color palettes.

---

## 📁 Project Architecture

```text
PDF_Invoice_Generator/
│
├── main.py                     # CLI entry point for batch processing
├── config.py                   # Central company branding, tax rates & styling
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git tracking rules
│
├── engine/                     # Core business logic
│   ├── __init__.py
│   ├── data_loader.py          # Data ingestion and order grouping engine
│   ├── qr_generator.py         # Dynamic vector QR code generation
│   └── invoice_builder.py      # ReportLab layout, table styling & PDF generation
│
├── input/                      # Batch order spreadsheets
│   └── orders.csv              # Raw input data
│
└── output/                     # Production PDF destination
    ├── Invoice_INV-2025-001.pdf
    ├── Invoice_INV-2025-002.pdf
    └── Invoice_INV-2025-003.pdf
