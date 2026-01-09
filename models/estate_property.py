
from odoo import models , fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate Property"

    name = fields.Char(string="Property Name", required=True, size=50)
    postcode = fields.Integer(string="Postcode", required=True, help="Postal area", size=5)
    date_available = fields.Date(string="Available From")
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price' )
    
    
 
    description = fields.Text(string="Descriptions")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")





    owners_list = fields.Many2one('owner',string="Primary Owner's")

    shared_owner_ids = fields.Many2many(
        'owner',
        'owner_property_shared_rel',
        'property_id',
        'owner_id',
        string="Shared Owners")
    
    def edit_button(self):
        pass

    def create_button(self):
        pass

    def action_send_msg(self):
        return {
            'name': 'Property Enquiry',
            'type': 'ir.actions.act_window',
            'res_model': 'properties.enquiry.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
    



class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer on different property"

    price = fields.Float(string="Price Value" , digits=(4,3))
    # property_id = fields.Many2one('estate.property',string="Property")
    # partner_id = fields.Many2one('res.partner',string='Buyer')

    binary_file = fields.Binary(string="Binary File")
    html_file = fields.Html(string="Html File " , help="html field is created")
    image_file = fields.Image(max_width = 5 , max_height=10)
    currency = fields.Monetary(string="Fee",currency_field="curr_id") 
    curr_id = fields.Many2one('res_currency',string="curr id" , invisible = True )
    
    person_gender = fields.Selection([
        ('male',"Male"),
        ('female',"Female")
    ],string="Person's Gender" , help="Enter Your Gender")
    deadline_date = fields.Datetime(string="Dead Line Hour")


    def action_test(self):
        values = {
            'name':"vipul" , 
            'contact_info':98877
        }
        create_record = self.env['owner'].create(values)


      