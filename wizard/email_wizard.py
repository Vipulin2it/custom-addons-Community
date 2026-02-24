from odoo import models, fields, api

class PropertyMailWizard(models.TransientModel):
    _name = 'property.mail.wizard'
    _description = 'Send Property Email Wizard'

    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
        readonly=True
    )

    email_to = fields.Char(
        string='To',
        required=True
    )

    subject = fields.Char(string='Subject', required=True)
    body_html = fields.Html(string='Body', required=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        property_id = self.env.context.get('active_id')
        if property_id:
            prop = self.env['estate.property'].browse(property_id)
            res.update({
                'property_id': prop.id,
                'email_to': prop.user_id.email or '',
                'subject': f'Property Notification - {prop.name}',
                'body_html': f"""
                    <p>Dear Owner,</p>
                    <p>This is regarding property <b>{prop.name}</b>.</p>
                """
            })
        return res

    def action_send_mail(self):
        self.ensure_one()

        mail = self.env['mail.mail'].create({
            'subject': self.subject,
            'body_html': self.body_html,
            'email_to': self.email_to,
            'email_from': self.env.user.email_formatted or self.env.company.email,
        })

        mail.send()
        return {'type': 'ir.actions.act_window_close'}
