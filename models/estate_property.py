
# from odoo import models , fields ,api

# class EstateProperty(models.Model):
#     _name = "estate.property"
#     _description = "Real estate Property"


#     name = fields.Char(string="Property Name", required=True, size=50)
#     postcode = fields.Integer(string="Postcode", required=True, help="Postal area", size=5)
#     date_available = fields.Date(string="Available From")
#     expected_price = fields.Float(string='Expected Price')
#     selling_price = fields.Float(string='Selling Price' )
    
    
 
#     description = fields.Text(string="Descriptions")
#     bedrooms = fields.Integer(string="Bedrooms")
#     living_area = fields.Integer(string="Living Area(sqm)")
#     garage = fields.Boolean(string="Garage")
#     garden = fields.Boolean(string="Garden")





#     owners_list = fields.Many2one('owner',string="Primary Owner's")

#     shared_owner_ids = fields.Many2many(
#         'owner',
#         'owner_property_shared_rel',
#         'property_id',
#         'owner_id',
#         string="Shared Owners")
    
#     def edit_button(self):
#         pass

#     @api.model
#     def create_button(self,values):
#         rec =  super(EstateProperty, self ).create(values)
#         print("Record Created:", rec)
#         return rec
from odoo import models , fields , api

class EstateProperty(models.Model):
    # Correcting the _name value with quotes
    _name = 'estate.property'
    _description = 'Real estate Property'
    
    name = fields.Char(string='Property Name', required=True, size=50)
    postcode = fields.Integer(string='Postcode', required=True, help='Postal area', size=5)
    date_available = fields.Date(string='Available From')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price')
    description = fields.Text(string='Descriptions')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area(sqm)')
    garage = fields.Boolean(string='Garage')
    
    # Assuming 'owner' is another model name you've defined
    owners_list = fields.Many2one('owner', string='Primary Owner')
    shared_owner_ids = fields.Many2many(
        'owner', 
        'owner_property_shared_rel', 
        'property_id', 
        'owner_id', 
        string='Shared Owners'
    )


    garden = fields.Boolean(string='Garden',)
    garden_message = fields.Char(string='Garden Status Message')
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_message = "The record is now active."
        else:
            self.garden_message = "The record is now inactive."



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
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name}  {rec.postcode}"


    def button_field_get(self , allfields = None , attributes = None ):

        fields_info =self.env['estate.property']
        fields_data  =  fields_info.fields_get(attributes=attributes , allfields=allfields )
        fields_data['description']['default'] = 'this is a custom description'
        fields_data['bedrooms']['placeholder'] = 'this is a custom placeholder '
        print(f"------------------------------Fields Data: {fields_data}*************------------------------")
        return fields_data




class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer on different property"
    _rec_name="owner_id"
    

    owner_id = fields.Many2one('owner',string="Owner" , context={'from_offer': True})
    owner_contact = fields.Integer(related='owner_id.contact_info', string ="Owner Contact Info", default=456789 )

    price = fields.Float(string="Price Value" , digits=(4,3), default=1000.567)
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


    @api.onchange('price')
    def onchange_price(self):
        for rec in self:
            if rec.price < 1000:
                return {
                    'warning':{
                        'title':"Price Alert",
                        'message':"The price is below 1000"
                    }
                }
            
    @api.onchange('owner_id')
    def onchange_owner_contact(self):
        for rec in self:
            if rec.owner_id:
                rec.owner_contact = rec.owner_id.contact_info
            else:
                rec.owner_contact = 0

    
    def reads_grouping(self):
        # rec = self.env['estate.property.offer'].read_group( domain=[('person_gender','=','male')], fields=['total_price:sum(price)'], groupby=['person_gender'])
        # # print("Grouped Records:", rec)
        # print("--------------------------------------------------")
        
        rec = self.env['sale.order'].read_group(domain=[],
                                                 fields=['amount_total:sum'],
                                                 groupby=['date_order:month'],
                                                 )
        
        
        print("-----------------------------------Grouped Records:")
        for record in rec:
            print("Group Record:", record)


    def read_search_read(self):
        rec = self.env['estate.property.offer'].search_read(domain=[('price','>',5000)], fields=['owner_id','price'] , limit  = 10 , offset=0 , order='price desc' )
        
        
        print("-----------------------------------Search Read Records:")
        for record in rec:
            print("Search Read Record:", record) 

        
    @api.model
    def name_create(self, name):
        rec = super(EstatePropertyOffer, self).name_create(name)
        print("-------------------------------Name Created Record:-------------", rec)
        return rec
    

    # @api.model
    # def button_name_create(self, name):
    #     rec = self.env['estate.property.offer'].create({
    #         'owner_id': name,
    #     })
    #     print("--------------------------------Name Created Record:-------------", rec)
    #     return rec

    @api.model
    def default_get(self, fields):
        res = super(EstatePropertyOffer, self).default_get(fields)
        res['price'] = 5000.567
        res['person_gender'] ='male'
        print("------------------------------Default Get Method Res:", res)
        return res

   
    
# class SaleOrder(models.Model):
#    _inherit = 'sale.order'


#    postcode = fields.Char(string="Customer Postcode")
