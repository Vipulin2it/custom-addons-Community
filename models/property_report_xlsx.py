from odoo import models
import io
import base64
import qrcode
from PIL import Image


class PropertyReportXlsx(models.AbstractModel):
    _name = 'report.mycompany_custom.property_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, properties):

        for obj in properties:

            # Worksheet

            sheet_name = (obj.name or 'Property')[:31]
            sheet = workbook.add_worksheet(sheet_name)


            # Formats

            title_style = workbook.add_format({
                'bold': True,
                'font_size': 18
            })

            header_style = workbook.add_format({
                'bold': True,
                'bg_color': "#ac7474",
                'border': 1,
                'align': 'center'
            })

            cell_style = workbook.add_format({
                'border': 1,
                'valign': 'top'
            })

            bold_label = workbook.add_format({
                'bold': True
            })


            # Title

            sheet.write(0, 0, 'Property Details', title_style)


            # Property Image (Top Right) – SAFE PNG CONVERSION

            if obj.image_field_name:
                try:
                    # Decode base64
                    raw = base64.b64decode(obj.image_field_name)

                    # Open & force PNG
                    img = Image.open(io.BytesIO(raw)).convert("RGB")
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format="PNG")
                    img_buffer.seek(0)

                    sheet.insert_image(
                        2, 3,
                        "property.png",
                        {
                            'image_data': img_buffer,
                            'x_scale': 0.5,
                            'y_scale': 0.5,
                            'object_position': 1,
                        }
                    )

                    sheet.set_row(2, 30)
                    sheet.set_row(3, 30)
                    sheet.set_row(4, 30)
                    sheet.set_row(5, 30)
                    sheet.set_column(3, 3, 25)

                except Exception:
                    pass  # Skip invalid images safely

            
            # Property Basic Info
            
            sheet.write(2, 0, 'Property Owner:', bold_label)
            sheet.write(2, 1, obj.user_id.name or '')

            sheet.write(3, 0, 'Property Name:', bold_label)
            sheet.write(3, 1, obj.name or '')

            sheet.write(4, 0, 'Postcode:', bold_label)
            sheet.write(4, 1, obj.postcode or '')

            sheet.write(5, 0, 'Expected Price:', bold_label)
            sheet.write(5, 1, obj.expected_price or 0)

            
            # Status
            
            status = "Sold" if obj.selling_price > 0 else "Available"
            sheet.write(6, 0, 'Status:', bold_label)
            sheet.write(6, 1, status)

            
            # Details Table
            
            headers = [
                'Selling Price',
                'Primary Owner',
                'Shared Owner',
                'Available From'
            ]

            for col, header in enumerate(headers):
                sheet.write(9, col, header, header_style)

            sheet.write(10, 0, obj.selling_price or 0, cell_style)

            primary_owners = "\n".join(
                owner.name for owner in obj.owners_list
            )
            sheet.write(10, 1, primary_owners, cell_style)

            shared_owners = "\n".join(
                owner.name for owner in obj.shared_owner_ids
            )
            sheet.write(10, 2, shared_owners, cell_style)

            sheet.write(
                10, 3,
                str(obj.date_available or ''),
                cell_style
            )

            sheet.set_column('A:D', 20)

            
            # QR Code
            
            qr_data = (
                f"Property: {obj.name}\n"
                f"Owner: {obj.user_id.name}\n"
                f"Expected Price: {obj.expected_price}\n"
                f"Status: {status}"
            )

            qr = qrcode.QRCode(
                version=1,
                box_size=4,
                border=4
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            qr_image = qr.make_image(
                fill_color="black",
                back_color="white"
            )

            qr_buffer = io.BytesIO()
            qr_image.save(qr_buffer, format='PNG')
            qr_buffer.seek(0)

            sheet.insert_image(
                12, 3,
                "qr_code.png",
                {
                    'image_data': qr_buffer,
                    'x_scale': 0.6,
                    'y_scale': 0.6,
                    'object_position': 1,
                }
            )

            sheet.set_row(12, 35)
            sheet.set_row(13, 35)
            sheet.set_row(14, 35)
            sheet.set_row(15, 35)
            sheet.set_column(3, 4, 22)
