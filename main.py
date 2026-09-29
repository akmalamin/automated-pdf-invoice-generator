"""
main.py — Automated PDF Invoice & Billing Generator.

Usage:
    python main.py                     → Generate all invoices from orders.csv
    python main.py --input input/my.csv → Generate from custom file
"""

import argparse
from config import Config
from engine.data_loader import DataLoader
from engine.invoice_builder import InvoiceBuilder


def main():
    parser = argparse.ArgumentParser(description="📄 Enterprise PDF Invoice Generator")
    parser.add_argument("--input", default=f"{Config.INPUT_DIR}/orders.csv", help="Path to orders CSV/Excel")
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════╗
║   📄  AUTOMATED PDF INVOICE GENERATOR — Day 108          ║
║   Enterprise ReportLab Engine with Dynamic QR Codes      ║
╚══════════════════════════════════════════════════════════╝
    """)

    # 1. Load batch order data
    loader = DataLoader(args.input)
    orders = loader.load_orders()

    if not orders:
        print("❌ No invoice orders found.")
        return

    # 2. Build PDFs
    print(f"\n🚀 Generating {len(orders)} PDF invoices...\n")
    generated_files = []

    for order in orders:
        builder = InvoiceBuilder(order)
        pdf_path = builder.build_pdf()
        generated_files.append(pdf_path)

    print(f"\n{'=' * 60}")
    print(f"🏁 BATCH GENERATION COMPLETE!")
    print(f"📁 Output folder: {Config.OUTPUT_DIR}/")
    print(f"📄 Invoices created: {len(generated_files)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()