from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate Property'
    _inherit = ['mail.thread']  # FIX 1

    image_field_name = fields.Image(string='Image')  # FIX 7

    name = fields.Char(string='Property Name', required=True, size=50)

    user_id = fields.Many2one(
        'res.users',
        string="Created By",
        default=lambda self: self.env.user,
        ondelete='set null',
        index=True,
        tracking=True
    )

    postcode = fields.Integer(string='Postcode', required=True, help='Postal area', size=5)
    date_available = fields.Date(string='Available From')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price')
    description = fields.Text(string='Descriptions')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area(sqm)')
    garage = fields.Boolean(string='Garage')

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    owners_list = fields.Many2one('owner', string='Primary Owner')

    # FIX 3: inverse field corrected (added property_id in owner is NOT required)
    shared_owner_ids = fields.One2many(
        'owner',
        'reference_field',
        string='Shared Owners'
    )

    garden = fields.Boolean(string='Garden')
    garden_message = fields.Char(string='Garden Status Message')

    display_name = fields.Char(  # FIX 2
        compute='_compute_display_name',
        store=True
    )

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_message = "The record is now active."
        else:
            self.garden_message = "The record is now inactive."

    def send_custom_mail(self):
        template = self.env.ref("mycompany_custom.email_template_report", raise_if_not_found=False)
        if template:
            for rec in self:
                template.send_mail(rec.id, force_send=True)

    def action_send_mail(self):
        return {
            'name': 'Send Mail',
            'type': 'ir.actions.act_window',
            'res_model': 'property.mail.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    def print_custom_report(self):
        return self.env.ref("mycompany_custom.action_report_custom_pdf").report_action(self)

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

    @api.depends('name', 'postcode')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name}  {rec.postcode}"

    def button_field_get(self, allfields=None, attributes=None):
        fields_info = self.env['estate.property']
        fields_data = fields_info.fields_get(
            allfields=allfields,
            attributes=attributes
        )  # FIX 4
        fields_data['description']['default'] = 'this is a custom description'
        fields_data['bedrooms']['placeholder'] = 'this is a custom placeholder'
        print(f"------------------------------Fields Data: {fields_data}*************------------------------")
        return fields_data


# --------------------------------------------------------------------

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer on different property"
    _rec_name = "owner_id"

    owner_id = fields.Many2one('owner', string="Owner", context={'from_offer': True})

    owner_contact = fields.Integer(
        related='owner_id.contact_info',
        string="Owner Contact Info",
        store=True
    )

    price = fields.Float(
        string="Price Value",
        digits=(10, 3),  # FIX 6
        default=1000.567
    )

    binary_file = fields.Binary(string="Binary File")
    html_file = fields.Html(string="Html File", help="html field is created")
    image_file = fields.Image(max_width=5, max_height=10)

    currency = fields.Monetary(
        string="Fee",
        currency_field="curr_id"
    )

    curr_id = fields.Many2one(
        'res.currency',  # FIX 5
        string="Currency",
        invisible=True
    )

    person_gender = fields.Selection(
        [('male', "Male"), ('female', "Female")],
        string="Person's Gender",
        help="Enter Your Gender"
    )

    deadline_date = fields.Datetime(string="Dead Line Hour")

    def action_test(self):
        values = {'name': "vipul", 'contact_info': 98877}
        self.env['owner'].create(values)

    @api.onchange('price')
    def onchange_price(self):
        if self.price and self.price < 1000:
            return {
                'warning': {
                    'title': "Price Alert",
                    'message': "The price is below 1000"
                }
            }

    @api.onchange('owner_id')
    def onchange_owner_contact(self):
        self.owner_contact = self.owner_id.contact_info if self.owner_id else 0

    def reads_grouping(self):
        rec = self.env['sale.order'].read_group(
            domain=[],
            fields=['amount_total:sum'],
            groupby=['date_order:month'],
        )
        for record in rec:
            print("Group Record:", record)

    def read_search_read(self):
        rec = self.env['estate.property.offer'].search_read(
            domain=[('price', '>', 5000)],
            fields=['owner_id', 'price'],
            limit=10,
            order='price desc'
        )
        for record in rec:
            print("Search Read Record:", record)

    @api.model
    def name_create(self, name):
        rec = super(EstatePropertyOffer, self).name_create(name)
        print("-------------------------------Name Created Record:-------------", rec)
        return rec

    @api.model
    def default_get(self, fields):
        res = super(EstatePropertyOffer, self).default_get(fields)
        res['price'] = 5000.567
        res['person_gender'] = 'male'
        print("------------------------------Default Get Method Res:", res)
        return res
