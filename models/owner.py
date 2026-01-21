from odoo import fields, models , api
from datetime import date

class Owner(models.Model):
    _name = "owner"
    _description = "Owner Portal"
    


    serial_no = fields.Integer(
    string="S.No.",
    compute="_compute_serial_no",
    store=False)


    parent_id = fields.Many2one(
        'owner',
        string="Parent Owner")
    
    child_ids = fields.One2many("owner", "parent_id", string="Child Owners")



    # property_ids = fields.One2many(
    #     'estate.property',
    #     'owner_id',
    #     string="Owned Properties")
    

    name = fields.Char(string="Name", size=20)
    contact_info = fields.Integer(string="Contact Info" , copy=False , default=98877456)
    date_of_birth = fields.Datetime(string="Date of Birth")
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_inverse_age', tracking=True ,store=True ) 
    gender = fields.Selection([
        ('male',"Male"),
        ('female',"Female")
    ],string="Person's Gender" , help="Enter Your Gender")

    shared_property_ids = fields.Many2many(
        'estate.property',
        'owner_property_shared_rel',
        'owner_id',
        'property_id',
        string="Shared Properties"
    )

    reference_field = fields.Reference(selection=[('estate.property', 'Property')],string="Property Postcode Id")


    def _compute_serial_no(self):
            serial = 1
            records = self.search([], order='id')
            for rec in records:
                rec.serial_no = serial
                serial += 1

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
            rec.display_name = f"{rec.name}"



# ########################################################   ORM METHODS  ########################################################

#     @api.model_create_multi
#     def create(self, values):
#         rec = super(Owner, self).create(values)
#         print(f"------------------------------Record Created: {rec , values}*************------------------------")
#         return rec
    


    # def custom_button(self):
    #     self.env['owner'].create({
    #     'name': 'Button clicked!'
    #     })

    

#     def write(self, values):
#         print("Write Method Called")
#         res =super(Owner , self).write(values)
#         print(f"------------------------------Record Updated: {self , values}*************------------------------")
#         return res


#     def custom_write(self):
#         print("Custom Write Method Called")
#         # self.update({'name':'Updated Name from Custom Write Method'})
#         # self.write({'name':'Updated Name from Custom Write Method'})

#         record = self.search([], limit=10)
#         # record.write({'age':55})
#         for rec in record:
#             rec.write({'age':rec.id})
#         print(f"------------------------------Record Updated: {record}*************------------------------")


    def duplicate_record(self):
        print("Duplicate Method Called")
        new_record = self.copy({'name': f'copy of {self.name}'})
        print(f"------------------------------Record Duplicated: {new_record}*************------------------------")


    @api.returns('self', lambda rec: rec.id)
    def copy(self, default=None):
        rec = super(Owner, self).copy(default=default)
        return rec  
    


    def delete_record(self):
        self.unlink()
        print(f"------------------------------Record Deleted*************------------------------")


    # def search_records(self):                                                               
    #     # rec = self.env['owner'].search([],limit=1,offset =1)
    #     # rec = self.env['estate.property'].search([('owners_list','child_of',132)], )
    #     rec = self.env['estate.property'].search([('owners_list','not any',[('name','ilike','vipul')])]) 
    #     print(f"------------------------------Records Found: {rec }*************------------------------")


    
    # def count_record(self):
    #     count = self.env['owner'].search_count([])
    #     print(f"------------------------------Records Counted: {count }*************------------------------")


    def read_button(self):
        rec = self.env['owner'].search([] , limit=2)
        data = rec.read(['name','contact_info'])
        print(f'------------------------------Records Read: {data}*************------------------------')

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=7, order=None ):
        domain = ['|',('owner_id','ilike',name),('age','ilike',name)]
        rec = self._search(domain, limit=limit, order=order)
        print("------------------------------Name Search Records:", rec) 

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=7, order=None ,):
       
        domain += [
                '|',
                ('name', operator, name),
                ('age', '=', int(name)) ] if name.isdigit() else ('age', '=', -1)
        print("------------------------------Name Search Domain:", domain)
        return self._search(domain, limit=limit, order=order , )
       

    
    def button_filtered_record(self):
        rec =self.env['owner'].search([]) 
        filtered_rec = rec.filtered(lambda r : 'vip' in str(r.name)).mapped(lambda r: (r.id, r.name))

        print(f"------------------------------Filtered Records: {filtered_rec}*************------------------------")


    def button_sorted_record(self):
        rec = self.env['owner'].search([])
        soreted_rec = rec.sorted(key = lambda r: r.age, reverse = True).mapped('name')
        print(f"------------------------------Sorted Records: {soreted_rec}*************------------------------")

    def button_grouped_record(self):
        rec = self.env['owner'].search([])
        grouped_rec = rec.grouped(key ='gender')
        print(f"------------------------------Grouped Records: {grouped_rec}*************------------------------")
        for ky in grouped_rec:
            print(f" ------------------------------Key: {ky} , Values: {grouped_rec[ky]}*************------------------------")




   