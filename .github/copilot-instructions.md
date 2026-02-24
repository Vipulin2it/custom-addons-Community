# AI Coding Assistant Instructions for MyCompany Custom Odoo 17 Addon

## Project Overview
This is a custom Odoo 17 module extending Odoo's CRM/Sales capabilities with real estate property management features. The addon manages properties, owners, and property enquiries with related reporting capabilities.

**Key Dependencies:** `base`, `sale`, `web`  
**Model Namespace:** `estate.property`, `owner`, `properties.enquiry.wizard`

## Architecture & Data Model

### Core Models (in `models/`)
- **`estate.property`**: Represents real estate properties with details like bedrooms, living area, pricing, and availability
  - Relations: `owners_list` (Many2one to owner), `shared_owner_ids` (Many2many owners)
  - Key fields: name, postcode, expected_price, selling_price, description, image_field_name, date_available
  - Multi-company support via `company_id` field
  - User tracking: `user_id` with automatic current user assignment

- **`owner`**: Represents property owners with hierarchical structure
  - Relations: parent-child via `parent_id`/`child_ids`, links to properties via `shared_property_ids` (Many2many)
  - Key fields: name, contact_info, date_of_birth, age (computed), gender
  - Tracks system user association via `user_id`

- **`properties.enquiry.wizard`** (TransientModel): Temporary model for property enquiry form submissions
  - Fields: property_type, person_name, person_email, contact_number, enquiry_message
  - Action: `action_send_enquiry()` creates enquiry records

### Field Patterns
- Use `tracking=True` on user-facing fields to enable audit trail (e.g., `age` field in owner model)
- Many2one/Many2many fields use custom relation tables (e.g., `owner_property_shared_rel`)
- Image handling via `Binary` fields with `attachment=True` (renders as avatar in views)
- Computed fields (e.g., `age` in owner) use `_compute_*` and `_inverse_*` methods
- Use `onchange` decorators for dynamic field updates (e.g., `garden` toggle shows/hides status message)

## UI Structure (in `views/`)

### View Conventions
- **Tree views** display list of records with action buttons in `<header>`
- **Form views** use `<header>`, `<sheet>`, and `<group>` structure for layout
- **Widgets**: `many2one_tags`, `many2many_tags` for relational fields; `image` for binary fields; `boolean_toggle` for toggles
- **Action Buttons** types: `type='object'` calls Python method; `type='action'` opens wizard/action
- Button `display="always"` shows even when record locked

### Key View Files
- `estate_property.xml`: Tree & form for properties with image gallery
- `owner.xml`: Owner portal with hierarchical display
- `enquiry.xml`: Property enquiry interface

## Developer Workflows

### Update Module in Development
```bash
/.odoo17-bin -c <odoo17.conf> -u mycompany_custom
```

### Key Development Patterns
1. **Model Method Actions**: Prefix with `action_` for wizards/reports (e.g., `action_send_msg()`)
2. **Transient Wizards**: Keep in `wizard/` folder, implement `action_*` methods to execute business logic
3. **Security**: Define access rules in `security/ir.model.access.csv` (currently all permissions enabled)
4. **Reports**: QWeb templates in `report/` generate PDF outputs via `ir.actions.report` records

## Common Tasks & Examples

### Adding a Field to Model
```python
# In models/estate_property.py
new_field = fields.Char(string="Label", required=True, tracking=True)  # Add tracking for audit
```

### Creating a Wizard Action
```python
def action_send_msg(self):
    return {
        'name': 'Property Enquiry',
        'type': 'ir.actions.act_window',
        'res_model': 'properties.enquiry.wizard',
        'view_mode': 'form',
        'target': 'new',
    }
```

### Accessing Related Records
```python
property_rec = self.env['estate.property'].browse(property_id)
owners = property_rec.shared_owner_ids  # Many2many access
primary_owner = property_rec.owners_list  # Many2one access
```

## Critical Conventions
- **Model Naming**: Use snake_case for `_name` (e.g., `estate.property`, `properties.enquiry.wizard`)
- **View IDs**: Follow `view_{model_name}_{view_type}` pattern (e.g., `view_estate_property_form`)
- **Module Manifest**: Always list data files in correct order (security → views → wizards → reports)
- **Relation Tables**: Custom many2many tables explicitly named (e.g., `owner_property_shared_rel`)

## Integration Points
- **Sales Module**: Addon depends on `sale` for CRM integration (potential future expansion)
- **Multi-company**: Records respect company boundaries via `company_id` field
- **User Tracking**: Automatic user association via `user_id` default function

## Known Issues/TODOs
- Commented-out models in `estate_property.py` and `owner.py` - verify if needed before uncommenting
- `button_field_get` action in form view has no implementation
- Report templates incomplete in `qweb_report.xml`
