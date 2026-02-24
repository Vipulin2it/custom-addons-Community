from odoo import models,fields,api 

## extentension of owner model to add additional info field
class ExtendedModelOwner(models.Model):
    _inherit='owner'

    # Additional field for extended model
    additional_info = fields.Char(string="Additional Info")
    


## deligation method to get additional info from owner model

class Address(models.Model):
    _name = 'address'
    _inherits = {'owner': 'owner_id'}

    owner_id = fields.Many2one('owner', required=True, ondelete='cascade')
    Owner_city= fields.Char(string="Owner City", store=True)
    Owner_pincode= fields.Char(string="Owner Pincode", store=True)
    Owner_additional_info = fields.Char(string="Owner Additional Info",  store=True)
    
    
class EstatePropertyOffer(models.Model):
    _inherit ='estate.property.offer'
    
    
  
    
    person_gender = fields.Selection(
        [
      
         ("new", "New"),
        ("in_progress", "In Progress"),
        ("changes_requested", "Changes Requested"),
        ("approved", "Approved"),
        ("cancel", "Canceled"),
        ("done", "Done"),
        ],
    )
    
    person_name = fields.Selection(
        [('vipul', "Vipul"), ('sachin', "Sachin"),('rahul', "Rahul"),   ('rohit', "Rohit") , ('suresh', "Suresh")],
        string="Person's Name",
        help="Enter Your Name"
    )



    
    
    