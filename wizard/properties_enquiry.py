from odoo import api, fields, models

class PropertiesEnquiryWizard(models.TransientModel):
    _name = "properties.enquiry.wizard"
    _description = "Properties Enquiry Wizard"


    property_type = fields.Many2one('estate.property',string="Property Type" , store=True)
    person_name = fields.Char(string="Person Name", required=True , store=True)
    person_email = fields.Char(string="Person Email", required=True , store=True)
    contact_number = fields.Integer(string="Contact Number", required=True, max_length=5 , store=True)
    enquiry_message = fields.Text(string="Enquiry Message" , store=True)

    def action_send_enquiry(self):
        vals={
            'property_type': self.property_type.id,
            'person_name': self.person_name,
            'person_email': self.person_email,
            'contact_number': self.contact_number,
            'enquiry_message': self.enquiry_message,
        }
        self.env['properties.enquiry.wizard'].create(vals)

    def action_cancel_enquiry(self):
        pass

   


    