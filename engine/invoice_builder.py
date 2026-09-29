"""engine/invoice_builder.py — ReportLab PDF invoice generator."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from config import Config
from engine.qr_generator import QRGenerator


class InvoiceBuilder:
    """Builds pixel-perfect, branded PDF invoices using ReportLab."""

    def __init__(self, invoice_data):
        self.inv = invoice_data
        self.filename = f"Invoice_{self.inv['invoice_id']}.pdf"
        self.output_path = os.path.join(Config.OUTPUT_DIR, self.filename)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.title_style = ParagraphStyle(
            "InvTitle",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor(Config.PRIMARY_COLOR),
        )
        self.body_style = ParagraphStyle(
            "InvBody",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor(Config.TEXT_DARK),
        )
        self.body_bold = ParagraphStyle(
            "InvBodyBold",
            parent=self.body_style,
            fontName="Helvetica-Bold",
        )
        self.right_style = ParagraphStyle(
            "InvRight",
            parent=self.body_style,
            alignment=2,  # Right align
        )

    def build_pdf(self):
        """Generates the PDF document."""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        story = []

        # ---------------------------------------------------------
        # 1. HEADER & BRANDING (Top Banner)
        # ---------------------------------------------------------
        company_info = f"<b>{Config.COMPANY_NAME}</b><br/>{Config.COMPANY_TAGLINE}<br/>{Config.COMPANY_ADDRESS.replace(chr(10), '<br/>')}<br/>{Config.COMPANY_EMAIL}"
        invoice_header = f"<b><font size='22' color='{Config.PRIMARY_COLOR}'>INVOICE</font></b><br/><br/><b>Invoice #:</b> {self.inv['invoice_id']}<br/><b>Date:</b> {self.inv['date']}<br/><b>Due Date:</b> {self.inv['due_date']}"

        header_table = Table(
            [
                [Paragraph(company_info, self.body_style), Paragraph(invoice_header, self.right_style)]
            ],
            colWidths=[4.0 * inch, 3.5 * inch],
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 15))

        # ---------------------------------------------------------
        # 2. BILL TO SECTION
        # ---------------------------------------------------------
        bill_to_text = f"<b><font color='{Config.SECONDARY_COLOR}'>BILL TO:</font></b><br/><b>{self.inv['customer_name']}</b><br/>{self.inv['customer_address']}<br/>{self.inv['customer_email']}"
        bill_table = Table([[Paragraph(bill_to_text, self.body_style)]], colWidths=[7.5 * inch])
        bill_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(Config.BG_LIGHT)),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        story.append(bill_table)
        story.append(Spacer(1, 20))

        # ---------------------------------------------------------
        # 3. LINE ITEMS TABLE
        # ---------------------------------------------------------
        table_data = [[
            Paragraph("<b>Item Description</b>", self.body_bold),
            Paragraph("<b>Qty</b>", self.body_bold),
            Paragraph("<b>Unit Price</b>", self.body_bold),
            Paragraph("<b>Total</b>", self.body_bold),
        ]]

        subtotal = 0.0
        for item in self.inv["items"]:
            subtotal += item["total"]
            table_data.append([
                Paragraph(item["description"], self.body_style),
                Paragraph(str(item["quantity"]), self.body_style),
                Paragraph(f"{Config.CURRENCY_SYMBOL}{item['unit_price']:,.2f}", self.body_style),
                Paragraph(f"{Config.CURRENCY_SYMBOL}{item['total']:,.2f}", self.body_style),
            ])

        items_table = Table(table_data, colWidths=[4.2 * inch, 0.8 * inch, 1.2 * inch, 1.3 * inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(Config.PRIMARY_COLOR)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ]))
        # Style table headers text color to white
        for cell_idx in range(4):
            table_data[0][cell_idx].style.textColor = colors.white

        story.append(items_table)
        story.append(Spacer(1, 15))

        # ---------------------------------------------------------
        # 4. TOTALS & DYNAMIC QR CODE SECTION
        # ---------------------------------------------------------
        tax_amount = subtotal * Config.TAX_RATE
        grand_total = subtotal + tax_amount

        # Generate verification QR Code
        qr_payload = f"VERIFIED INVOICE | ID: {self.inv['invoice_id']} | Total: ${grand_total:,.2f} | Payer: {self.inv['customer_name']}"
        qr_file = QRGenerator.generate(qr_payload, filename=f"qr_{self.inv['invoice_id']}.png")
        qr_image = Image(qr_file, width=1.1 * inch, height=1.1 * inch)

        totals_text = f"""
        <b>Subtotal:</b> {Config.CURRENCY_SYMBOL}{subtotal:,.2f}<br/>
        <b>Sales Tax ({(Config.TAX_RATE * 100):.2f}%):</b> {Config.CURRENCY_SYMBOL}{tax_amount:,.2f}<br/>
        <b><font size='12' color='{Config.PRIMARY_COLOR}'>TOTAL DUE:</font></b> <font size='12'><b>{Config.CURRENCY_SYMBOL}{grand_total:,.2f}</b></font>
        """

        summary_table = Table(
            [
                [
                    qr_image,
                    Paragraph(f"<b>Scan to Verify / Pay Online</b><br/><font size='7' color='#718096'>{Config.PAYMENT_TERMS}</font>", self.body_style),
                    Paragraph(totals_text, self.right_style)
                ]
            ],
            colWidths=[1.3 * inch, 3.2 * inch, 3.0 * inch],
        )
        summary_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 25))

        # ---------------------------------------------------------
        # 5. FOOTER & NOTES
        # ---------------------------------------------------------
        footer_p = Paragraph(f"<font color='#718096' size='8'>{Config.FOOTER_NOTE}</font>", self.body_style)
        story.append(footer_p)

        doc.build(story)
        print(f"   📄 Generated: {self.filename}")
        return self.output_path