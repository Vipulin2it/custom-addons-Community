from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError


class Owner(models.Model):
    _name = "owner"
    _description = "Owner Portal"
    _inherit = ['mail.thread']   # FIX 1: needed because tracking=True is used
    _rec_name = 'display_name'   # FIX 2: avoid name/display issues

    user_id = fields.Many2one(
        'res.users',
        string="System User",
        ondelete='cascade',
        default=lambda self: self.env.user
    )

    property_id = fields.Many2one(
        'estate.property',
        string='Property List',
    )
   


    name = fields.Char(string="Name", size=20)

    contact_info = fields.Integer(
        string="Contact Info",
        copy=False,
        default=98877456
    )

    date_of_birth = fields.Datetime(string="Date of Birth")

    age = fields.Integer(
        string="Age",
        compute='_compute_age',
        inverse='_inverse_age',
        tracking=True,
        store=True
    )

    gender = fields.Selection(
        [
            ('male', "Male"),
            ('female', "Female")
        ],
        string="Person's Gender",
        help="Enter Your Gender"
    )

    active = fields.Boolean(
        string="Active Owner",
        default=True
    )

    reference_field = fields.Reference(
        selection=[('estate.property', 'Property')],
        string="Property Postcode Id"
    )

    # FIX 3: display_name field was missing
    display_name = fields.Char(
        compute='_compute_display_name',
        store=True
    )



    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                dob = rec.date_of_birth.date()  # FIX 4: Datetime → date
                today = date.today()
                rec.age = today.year - dob.year
            else:
                rec.age = 0

    def _inverse_age(self):
        for rec in self:
            if rec.age:
                today = date.today()
                rec.date_of_birth = date(
                    today.year - rec.age,
                    today.month,
                    today.day
                )
            else:
                rec.date_of_birth = False

    @api.depends('name')  # FIX 5: missing depends
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name}"

    # -------------------------------------------------
    # BUTTON / ORM DEMO METHODS (UNCHANGED)
    # -------------------------------------------------

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

    def read_button(self):
        rec = self.env['owner'].search([], limit=2)
        data = rec.read(['name', 'contact_info'])
        print(f'------------------------------Records Read: {data}*************------------------------')

    def button_filtered_record(self):
        rec = self.env['owner'].search([])
        filtered_rec = rec.filtered(
            lambda r: 'vip' in str(r.name)
        ).mapped(lambda r: (r.id, r.name))
        print(f"------------------------------Filtered Records: {filtered_rec}*************------------------------")

    def button_sorted_record(self):
        rec = self.env['owner'].search([])
        soreted_rec = rec.sorted(
            key=lambda r: r.age,
            reverse=True
        ).mapped('name')
        print(f"------------------------------Sorted Records: {soreted_rec}*************------------------------")

    def button_grouped_record(self):
        rec = self.env['owner'].search([])
        grouped_rec = rec.grouped(key='gender')
        print(f"------------------------------Grouped Records: {grouped_rec}*************------------------------")
        for ky in grouped_rec:
            print(
                f" ------------------------------Key: {ky} , Values: {grouped_rec[ky]}*************------------------------"
            )
