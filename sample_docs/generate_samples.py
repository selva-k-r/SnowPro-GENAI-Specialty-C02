"""
Generate synthetic sample documents for the SnowPro Gen AI C02 learning repo.

Everything here is invented. No real company, person, address or transaction
appears in these files. Each page carries a SYNTHETIC SAMPLE banner so the
output can never be mistaken for a real business record.
"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak)
from reportlab.lib.enums import TA_CENTER

OUT = "/home/claude/sample_docs"
os.makedirs(OUT, exist_ok=True)

S = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=S['Heading1'], fontSize=18, spaceAfter=10)
H2 = ParagraphStyle('H2', parent=S['Heading2'], fontSize=12, spaceBefore=12, spaceAfter=6)
BODY = ParagraphStyle('BODY', parent=S['BodyText'], fontSize=9.5, leading=13)
SMALL = ParagraphStyle('SMALL', parent=S['BodyText'], fontSize=8, textColor=colors.grey)
BANNER = ParagraphStyle('BANNER', parent=S['BodyText'], fontSize=7.5,
                        textColor=colors.HexColor('#b00020'), alignment=TA_CENTER)

BANNER_TEXT = ("SYNTHETIC SAMPLE DOCUMENT - generated for Snowflake Cortex training exercises. "
               "All companies, people, amounts and terms are fictional.")


def stamp(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#b00020'))
    canvas.drawCentredString(LETTER[0] / 2.0, 0.45 * inch,
                             "SYNTHETIC SAMPLE - fictional data for training purposes only")
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(LETTER[0] - 0.75 * inch, 0.45 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def build(name, story):
    doc = SimpleDocTemplate(os.path.join(OUT, name), pagesize=LETTER,
                            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                            topMargin=0.7 * inch, bottomMargin=0.8 * inch,
                            title=name)
    doc.build(story, onFirstPage=stamp, onLaterPages=stamp)
    print("wrote", name)


GRID = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8eef5')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a3d5c')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#b8c4d0')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
])


# ---------------------------------------------------------------- invoices
def invoice(fname, vendor, vaddr, vtax, inv_no, inv_date, due_date, po,
            bill_to, baddr, lines, terms, currency="USD", notes=None):
    st = [Paragraph(BANNER_TEXT, BANNER), Spacer(1, 10)]
    head = Table([[Paragraph(f"<b>{vendor}</b><br/><font size=8>{vaddr}<br/>Tax ID: {vtax}</font>", BODY),
                   Paragraph(f"<para align=right><font size=16><b>INVOICE</b></font><br/>"
                             f"<font size=9>Invoice No: <b>{inv_no}</b><br/>"
                             f"Invoice Date: {inv_date}<br/>"
                             f"Due Date: {due_date}<br/>"
                             f"PO Reference: {po}</font></para>", BODY)]],
                 colWidths=[3.6 * inch, 3.4 * inch])
    head.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    st += [head, Spacer(1, 16)]
    st += [Paragraph(f"<b>Bill To</b><br/><font size=9>{bill_to}<br/>{baddr}</font>", BODY),
           Spacer(1, 14)]

    data = [["Line", "Description", "Qty", "Unit Price", "Amount"]]
    subtotal = 0.0
    for i, (desc, qty, unit) in enumerate(lines, 1):
        amt = qty * unit
        subtotal += amt
        data.append([str(i), Paragraph(desc, ParagraphStyle('c', parent=BODY, fontSize=8.5)),
                     f"{qty:,.2f}", f"{unit:,.2f}", f"{amt:,.2f}"])
    tax = round(subtotal * 0.085, 2)
    total = round(subtotal + tax, 2)
    data += [["", "", "", "Subtotal", f"{subtotal:,.2f}"],
             ["", "", "", "Sales Tax 8.5%", f"{tax:,.2f}"],
             ["", "", "", f"Total Due ({currency})", f"{total:,.2f}"]]
    t = Table(data, colWidths=[0.45 * inch, 3.55 * inch, 0.7 * inch, 1.0 * inch, 1.1 * inch])
    style = GRID.getCommands() + [
        ('FONTNAME', (3, len(lines) + 3), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (3, len(lines) + 3), (-1, -1), colors.HexColor('#f2f6fa')),
        ('SPAN', (0, len(lines) + 1), (2, len(lines) + 1)),
        ('SPAN', (0, len(lines) + 2), (2, len(lines) + 2)),
        ('SPAN', (0, len(lines) + 3), (2, len(lines) + 3)),
    ]
    t.setStyle(TableStyle(style))
    st += [t, Spacer(1, 16),
           Paragraph(f"<b>Payment Terms:</b> {terms}", BODY)]
    if notes:
        st += [Spacer(1, 8), Paragraph(f"<b>Notes:</b> {notes}", SMALL)]
    st += [Spacer(1, 20),
           Paragraph("Remit payment by ACH or wire. Reference the invoice number on all remittances. "
                     "Questions regarding this invoice should be directed to accounts@example.invalid.", SMALL)]
    build(fname, st)


invoice("invoice_KF-2041.pdf",
        "Kestrel Freight Systems", "1400 Dockside Parkway, Suite 210<br/>Ashport, OR 97xxx",
        "TAX-KF-88142", "KF-2041", "2026-03-04", "2026-04-03", "PO-77310",
        "Meridian Grain Co.", "88 Silo Road<br/>Bexley Flats, KS 66xxx",
        [("Freight haulage, Ashport to Bexley Flats, 12 containers", 12, 1450.00),
         ("Fuel surcharge (indexed, March 2026)", 1, 2180.50),
         ("Detention charges, 6 hours beyond free time", 6, 95.00),
         ("Customs documentation handling", 12, 40.00)],
        "Net 30 from invoice date. 1.5% monthly interest on overdue balances.",
        notes="Detention charges are disputed by the customer and under review.")

invoice("invoice_AV-8817.pdf",
        "Alder &amp; Vance LLP", "77 Chancery Walk, Floor 9<br/>Northbrook, NY 10xxx",
        "TAX-AV-20551", "AV-8817", "2026-02-18", "2026-03-20", "PO-2026-0042",
        "Harbourview Analytics, Inc.", "512 Tidewater Avenue<br/>Harbourview, MA 02xxx",
        [("Contract review and redlining, Master Services Agreement", 14.5, 480.00),
         ("Regulatory research memorandum, data residency obligations", 8.0, 480.00),
         ("Client conference calls (3 sessions)", 3.25, 520.00),
         ("Filing and administrative disbursements", 1, 312.40)],
        "Net 30. Late payment fee of $150 applies after 45 days.")

invoice("invoice_TS-5530.pdf",
        "Tallgrass Supply Partners", "Unit 4, Prairie Industrial Estate<br/>Cedar Junction, IA 50xxx",
        "TAX-TS-66093", "TS-5530", "2026-03-29", "2026-04-13", "PO-91188",
        "Kestrel Freight Systems", "1400 Dockside Parkway, Suite 210<br/>Ashport, OR 97xxx",
        [("Pallet racking, heavy duty, 3.6m uprights", 40, 218.75),
         ("Beam sets, 2.7m, powder coated", 160, 46.20),
         ("Safety netting, 20m roll", 6, 289.00),
         ("Installation labour, two-person crew", 32, 78.50),
         ("Delivery and offload, flatbed", 2, 425.00)],
        "Net 15. Early settlement discount of 2% if paid within 7 days.",
        notes="Partial shipment: safety netting to follow under separate delivery note.")


# ---------------------------------------------------------------- contract
def contract():
    st = [Paragraph(BANNER_TEXT, BANNER), Spacer(1, 14),
          Paragraph("MASTER SERVICES AGREEMENT", H1),
          Paragraph("This Master Services Agreement (the \"Agreement\") is entered into as of "
                    "<b>1 April 2026</b> (the \"Effective Date\") by and between "
                    "<b>Harbourview Analytics, Inc.</b>, a corporation with its principal place of "
                    "business at 512 Tidewater Avenue, Harbourview, MA (\"Provider\"), and "
                    "<b>Meridian Grain Co.</b>, a corporation with its principal place of business at "
                    "88 Silo Road, Bexley Flats, KS (\"Customer\").", BODY),
          Spacer(1, 6),
          Paragraph("Agreement Reference: <b>MSA-HV-2026-0417</b>", BODY), Spacer(1, 10)]

    clauses = [
        ("1. Definitions",
         "\"Services\" means the data engineering and analytics services described in one or more "
         "Statements of Work executed under this Agreement. \"Deliverables\" means any report, model, "
         "dataset or documentation produced by Provider in the course of performing the Services. "
         "\"Confidential Information\" means non-public information disclosed by either party that is "
         "marked confidential or that a reasonable person would understand to be confidential."),
        ("2. Term and Renewal",
         "This Agreement commences on the Effective Date and continues for an initial term of "
         "<b>twenty-four (24) months</b> (the \"Initial Term\"). Following the Initial Term, this "
         "Agreement renews automatically for successive periods of <b>twelve (12) months</b> unless "
         "either party gives written notice of non-renewal not less than <b>sixty (60) days</b> before "
         "the end of the then-current term."),
        ("3. Fees and Payment",
         "Customer shall pay the fees set out in each Statement of Work. Invoices are payable "
         "<b>net thirty (30) days</b> from the invoice date. Provider may increase rates once per "
         "renewal term by no more than <b>four percent (4%)</b>, on ninety (90) days written notice. "
         "Amounts properly disputed in good faith are not subject to late fees while the dispute is "
         "being resolved under Section 10."),
        ("4. Termination",
         "Either party may terminate this Agreement for material breach if the breaching party fails to "
         "cure within <b>thirty (30) days</b> of written notice describing the breach. Customer may "
         "terminate any Statement of Work for convenience on <b>forty-five (45) days</b> written notice, "
         "in which case Customer shall pay for Services performed through the effective date of "
         "termination plus any non-cancellable third-party commitments."),
        ("5. Data Ownership and Residency",
         "Customer retains all right, title and interest in Customer Data. Provider is granted a limited "
         "licence to process Customer Data solely to deliver the Services. Provider shall store and "
         "process all Customer Data within the <b>United States</b>. Provider shall not transfer Customer "
         "Data outside that territory without Customer's prior written consent."),
        ("6. Confidentiality",
         "Each party shall protect the other's Confidential Information using no less than reasonable "
         "care and shall not disclose it except to employees and contractors with a need to know who are "
         "bound by obligations no less protective than these. Confidentiality obligations survive for "
         "<b>five (5) years</b> after termination, and indefinitely for trade secrets."),
        ("7. Limitation of Liability",
         "Except for breaches of Section 6 (Confidentiality) and Section 5 (Data Ownership and "
         "Residency), each party's aggregate liability arising out of this Agreement is limited to the "
         "<b>total fees paid by Customer in the twelve (12) months preceding the event</b> giving rise to "
         "the claim. Neither party is liable for indirect, incidental or consequential damages."),
        ("8. Indemnification",
         "Provider shall defend and indemnify Customer against third-party claims that the Deliverables "
         "infringe a United States patent, copyright or trade secret, provided Customer gives prompt "
         "notice and reasonable cooperation. This indemnity does not apply where the claim arises from "
         "Customer Data or from modifications made by Customer."),
        ("9. Service Levels",
         "Provider shall maintain availability of the hosted components of the Services at "
         "<b>99.5% measured monthly</b>, excluding scheduled maintenance notified at least five (5) "
         "business days in advance. Where availability falls below the target, Customer is entitled to a "
         "service credit of five percent (5%) of the monthly fee for each full percentage point below "
         "target, capped at twenty-five percent (25%) of the monthly fee."),
        ("10. Dispute Resolution and Governing Law",
         "The parties shall first attempt to resolve any dispute by good-faith negotiation between "
         "senior representatives within thirty (30) days. Any unresolved dispute shall be settled by "
         "binding arbitration administered in <b>Boston, Massachusetts</b> under the rules of a mutually "
         "agreed arbitral body. This Agreement is governed by the laws of the "
         "<b>Commonwealth of Massachusetts</b>, without regard to conflict-of-laws principles."),
        ("11. Assignment",
         "Neither party may assign this Agreement without the other's prior written consent, except that "
         "either party may assign to a successor in connection with a merger or sale of substantially all "
         "of its assets, on written notice."),
        ("12. Entire Agreement",
         "This Agreement, together with all Statements of Work, constitutes the entire agreement between "
         "the parties and supersedes all prior discussions. Amendments must be in writing and signed by "
         "authorised representatives of both parties."),
    ]
    for i, (h, body) in enumerate(clauses):
        st += [Paragraph(h, H2), Paragraph(body, BODY)]
        if i == 4:
            st.append(PageBreak())
            st.append(Paragraph(BANNER_TEXT, BANNER))
            st.append(Spacer(1, 10))
        if i == 9:
            st.append(PageBreak())
            st.append(Paragraph(BANNER_TEXT, BANNER))
            st.append(Spacer(1, 10))

    st += [Spacer(1, 24), Paragraph("Signed for and on behalf of the parties:", BODY), Spacer(1, 10)]
    sig = Table([["Harbourview Analytics, Inc.", "Meridian Grain Co."],
                 ["Name: R. Okonkwo", "Name: L. Castellanos"],
                 ["Title: Chief Operating Officer", "Title: VP, Supply Chain"],
                 ["Date: 1 April 2026", "Date: 1 April 2026"]],
                colWidths=[3.5 * inch, 3.5 * inch])
    sig.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 9),
                             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                             ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.grey)]))
    st.append(sig)
    build("contract_msa_harbourview.pdf", st)


contract()


# ------------------------------------------------------- financial statement
def financials():
    st = [Paragraph(BANNER_TEXT, BANNER), Spacer(1, 12),
          Paragraph("Meridian Grain Co.", H1),
          Paragraph("Unaudited Condensed Financial Statements<br/>"
                    "For the quarter ended <b>30 September 2026</b><br/>"
                    "Reporting currency: USD thousands", BODY),
          Spacer(1, 6),
          Paragraph("Document Reference: <b>FS-MGC-2026-Q3</b>", BODY),
          Spacer(1, 16),
          Paragraph("Condensed Statement of Operations", H2)]

    ops = [["", "Q3 2026", "Q3 2025", "YTD 2026", "YTD 2025"],
           ["Revenue", "48,210", "41,905", "139,640", "121,880"],
           ["Cost of goods sold", "(31,540)", "(28,110)", "(92,315)", "(83,440)"],
           ["Gross profit", "16,670", "13,795", "47,325", "38,440"],
           ["Selling and distribution", "(5,420)", "(4,860)", "(15,980)", "(14,120)"],
           ["General and administrative", "(4,105)", "(3,770)", "(12,240)", "(11,305)"],
           ["Research and development", "(1,260)", "(940)", "(3,510)", "(2,690)"],
           ["Operating income", "5,885", "4,225", "15,595", "10,325"],
           ["Interest expense", "(690)", "(755)", "(2,110)", "(2,290)"],
           ["Other income, net", "145", "88", "402", "231"],
           ["Income before tax", "5,340", "3,558", "13,887", "8,266"],
           ["Income tax expense", "(1,282)", "(854)", "(3,333)", "(1,984)"],
           ["Net income", "4,058", "2,704", "10,554", "6,282"]]
    t = Table(ops, colWidths=[2.8 * inch, 1.05 * inch, 1.05 * inch, 1.05 * inch, 1.05 * inch])
    t.setStyle(TableStyle(GRID.getCommands() + [
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold'),
        ('FONTNAME', (0, 12), (-1, 12), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 12), (-1, 12), colors.HexColor('#f2f6fa')),
    ]))
    st += [t, Spacer(1, 10),
           Paragraph("Figures in parentheses represent deductions. Percentages are calculated on "
                     "unrounded amounts.", SMALL),
           PageBreak(), Paragraph(BANNER_TEXT, BANNER), Spacer(1, 12),
           Paragraph("Condensed Balance Sheet", H2)]

    bs = [["", "30 Sep 2026", "31 Dec 2025"],
          ["Cash and cash equivalents", "12,440", "9,880"],
          ["Trade receivables", "27,315", "24,090"],
          ["Inventory", "33,760", "30,415"],
          ["Other current assets", "4,120", "3,655"],
          ["Total current assets", "77,635", "68,040"],
          ["Property, plant and equipment, net", "88,920", "91,440"],
          ["Intangible assets", "6,250", "6,880"],
          ["Total assets", "172,805", "166,360"],
          ["Trade payables", "21,455", "19,780"],
          ["Short-term borrowings", "8,000", "12,500"],
          ["Other current liabilities", "6,930", "6,215"],
          ["Total current liabilities", "36,385", "38,495"],
          ["Long-term debt", "42,100", "44,600"],
          ["Total liabilities", "78,485", "83,095"],
          ["Shareholders' equity", "94,320", "83,265"],
          ["Total liabilities and equity", "172,805", "166,360"]]
    t2 = Table(bs, colWidths=[3.4 * inch, 1.8 * inch, 1.8 * inch])
    t2.setStyle(TableStyle(GRID.getCommands() + [
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),
        ('FONTNAME', (0, 8), (-1, 8), 'Helvetica-Bold'),
        ('FONTNAME', (0, 12), (-1, 12), 'Helvetica-Bold'),
        ('FONTNAME', (0, 14), (-1, 14), 'Helvetica-Bold'),
        ('FONTNAME', (0, 16), (-1, 16), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 16), (-1, 16), colors.HexColor('#f2f6fa')),
    ]))
    st += [t2, PageBreak(), Paragraph(BANNER_TEXT, BANNER), Spacer(1, 12),
           Paragraph("Management Discussion", H2),
           Paragraph("Revenue grew 15.0% year on year in the third quarter, driven primarily by higher "
                     "volumes in the bulk grain segment and a favourable pricing environment in export "
                     "markets. Gross margin improved to 34.6% from 32.9%, reflecting lower inbound "
                     "freight costs following the renegotiation of the Kestrel Freight Systems haulage "
                     "contract in March 2026.", BODY),
           Spacer(1, 6),
           Paragraph("Operating expenses rose 9.8%, below revenue growth, as the company continued to "
                     "absorb the cost of its analytics modernisation programme. Research and development "
                     "spending increased 34.0% year on year, substantially all of which relates to the "
                     "demand-forecasting initiative begun in the first quarter.", BODY),
           Spacer(1, 6),
           Paragraph("Net debt reduced to $37.7 million from $47.2 million at the prior year end, "
                     "following the scheduled repayment of short-term borrowings and stronger operating "
                     "cash generation. The board has not declared a dividend for the quarter.", BODY),
           Spacer(1, 12), Paragraph("Principal Risks", H2),
           Paragraph("<b>Commodity price volatility.</b> A sustained 10% decline in benchmark grain "
                     "prices would reduce annual revenue by an estimated $11 million on current volumes.", BODY),
           Spacer(1, 4),
           Paragraph("<b>Counterparty concentration.</b> The three largest customers accounted for 38% of "
                     "revenue in the period, down from 44% in the prior year.", BODY),
           Spacer(1, 4),
           Paragraph("<b>Logistics disruption.</b> Port congestion at Ashport delayed 6% of scheduled "
                     "shipments in the quarter, with associated detention charges currently under dispute "
                     "with the haulage provider.", BODY)]
    build("financial_statement_mgc_q3_2026.pdf", st)


financials()


# --------------------------------------------------------------- text sample
with open(os.path.join(OUT, "support_tickets.txt"), "w") as f:
    f.write("""SYNTHETIC SAMPLE - fictional support tickets for training purposes only.

TICKET-4471 | 2026-03-02 | Priority: High
Customer: Meridian Grain Co.
The March invoice from Kestrel shows six hours of detention charges we do not
recognise. Our gate logs show the driver arrived 40 minutes outside the booking
window, which under clause 3 of the haulage schedule is the carrier's cost, not
ours. Please raise a dispute before the net-30 date. Frustrated that this is the
third month running.

TICKET-4488 | 2026-03-06 | Priority: Low
Customer: Harbourview Analytics, Inc.
Quick question rather than a problem - can we get the quarterly usage export as
CSV instead of the dashboard PDF? The PDF is fine, we just want to load it into
our own warehouse. No urgency at all, whenever suits.

TICKET-4502 | 2026-03-11 | Priority: Critical
Customer: Tallgrass Supply Partners
Racking delivery arrived without the safety netting and the delivery note says
"partial shipment to follow" with no date. We have installers on site being paid
to stand around. This is costing us real money every day it slips. Need a firm
date today.

TICKET-4519 | 2026-03-18 | Priority: Medium
Customer: Meridian Grain Co.
Renewal question. Our MSA says sixty days notice before the end of the current
term. We think the term ends 31 March 2028 but the signature page reads 1 April
2026 as the effective date, so we want to confirm the exact notice deadline
before we diary it.

TICKET-4533 | 2026-03-25 | Priority: Low
Customer: Harbourview Analytics, Inc.
Just wanted to say the new reconciliation report saved our finance team about two
days of work this month close. Whoever built it, pass on our thanks.
""")
print("wrote support_tickets.txt")
