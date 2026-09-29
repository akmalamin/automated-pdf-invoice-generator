"""engine/data_loader.py — Parses invoice line-items from spreadsheet data."""

import os
import pandas as pd


class DataLoader:
    """Loads and aggregates batch invoice orders."""

    def __init__(self, filepath):
        self.filepath = filepath

    def load_orders(self):
        print(f"\n📂 Loading orders from: {self.filepath}")

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")

        ext = os.path.splitext(self.filepath)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(self.filepath)
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(self.filepath, engine="openpyxl")
        else:
            raise ValueError(f"Unsupported format: {ext}")

        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

        # Group line-items by invoice_id
        invoices = {}
        for _, row in df.iterrows():
            inv_id = str(row.get("invoice_id", "INV-0001")).strip()

            if inv_id not in invoices:
                invoices[inv_id] = {
                    "invoice_id": inv_id,
                    "date": str(row.get("date", "2025-03-30")).strip(),
                    "due_date": str(row.get("due_date", "2025-04-30")).strip(),
                    "customer_name": str(row.get("customer_name", "Client")).strip(),
                    "customer_email": str(row.get("customer_email", "")).strip(),
                    "customer_address": str(row.get("customer_address", "")).strip(),
                    "items": [],
                }

            qty = int(row.get("quantity", 1))
            unit_price = float(str(row.get("unit_price", 0)).replace("$", "").replace(",", ""))

            invoices[inv_id]["items"].append({
                "description": str(row.get("item_description", "Services Rendered")).strip(),
                "quantity": qty,
                "unit_price": unit_price,
                "total": qty * unit_price,
            })

        print(f"   ✅ Parsed {len(invoices)} unique invoice orders")
        return list(invoices.values())