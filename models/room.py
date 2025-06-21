from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Room(models.Model):
    _name = 'hospitalme.room'
    _description = 'Hospital Room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    
# Fields
    name = fields.Char(string='Room Number/Name', required=True, tracking=True)
    bed_count = fields.Integer(string='Total Beds', default=1, tracking=True)
    occupied_bed_count = fields.Integer(string='Occupied Beds', default=0, tracking=True)

    state = fields.Selection([
        ('available', 'Available'),
        ('full', 'Full'),
        ('maintenance', 'Maintenance'),
    ], string='Room Status', default='available', tracking=True)

    # Optional: Link to department (uncomment if used)
    department_id = fields.Many2one('hospital.department', string='Department', tracking=True)

    @api.constrains('bed_count', 'occupied_bed_count')
    def _check_bed_counts(self):
        for room in self:
            if room.bed_count < 0 or room.occupied_bed_count < 0:
                raise ValidationError(_('Bed counts cannot be negative.'))
            if room.occupied_bed_count > room.bed_count:
                raise ValidationError(_('Occupied beds cannot exceed total beds.'))

    @api.onchange('occupied_bed_count', 'bed_count')
    def _onchange_bed_counts(self):
        """Automatically updates room state based on bed counts."""
        for room in self:
            if room.state == 'maintenance':
                continue
            if room.occupied_bed_count >= room.bed_count and room.bed_count > 0:
                room.state = 'full'
            elif room.occupied_bed_count == 0:
                room.state = 'available'
            else:
                room.state = 'available'

    def set_room_available(self):
        for room in self:
            if room.state != 'maintenance':
                room.state = 'available'

    def set_room_maintenance(self):
        for room in self:
            room.state = 'maintenance'

    def set_room_full(self):
        for room in self:
            room.state = 'full'

    def name_get(self):
        """Customize display name with occupancy."""
        result = []
        for room in self:
            display_name = f"{room.name} ({room.occupied_bed_count}/{room.bed_count} beds)"
            result.append((room.id, display_name))
        return result
