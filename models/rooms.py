from odoo import models, fields, api

class Rooms(models.Model):
    _name = 'hotel.rooms'
    _description = 'rooms master list'
    _order = 'name'

    name = fields.Char("Rooms No.")
    description = fields.Char("Rooms Description")
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Room Type")
    roomtypename=fields.Char("Room Type",related='roomtype_id.name')
