from odoo import fields, models , api
from datetime import date

class Owner(models.Model):
    _name = "owner"
    _description = "Owner Portal"
    

    Properties_info = fields.One2many(
        'estate.property',
        'owners_list'
    )

    name = fields.Char(string="Name", size=20)
    contact_info = fields.Integer(string="Contact Info")
    date_of_birth = fields.Datetime(string="Date of Birth")
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_inverse_age', tracking=True ,store=True) 
    

    shared_property_ids = fields.Many2many(
        'estate.property',
        'owner_property_shared_rel',
        'owner_id',
        'property_id',
        string="Shared Properties"
    )

    reference_field = fields.Reference(selection=[('estate.property', 'Property')],string="Property Postcode Id")

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today= date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    def _inverse_age(self):
        for rec in self:
            today= date.today()
            if rec.age:
                rec.date_of_birth = date(today.year - rec.age, today.month, today.day)
            else:
                rec.date_of_birth = False

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name}  {rec.contact_info}"
    

    @api.model_create_multi
    def create(self, values):
        rec = super(Owner, self).create(values)
        print(f"------------------------------Record Created: {rec , values}*************------------------------")
        return rec
    


    def custom_button(self):
        data = {'name': 'Button clicked!'}
        self.env['owner'].create(data)
