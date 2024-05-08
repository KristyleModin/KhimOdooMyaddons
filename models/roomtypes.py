# -*- coding: utf-8 -*-

#roomtypes.py

from odoo import models, fields, api

class roomtypes(models.Model):
    _name = 'hotel.roomtypes'
    _description = 'hotel roomtypes master list'
    _order = "name"

    name = fields.Char("Room Type Name")
    description = fields.Char("Room Type Description")
    imageroom = fields.Image("Room");
    imagebathroom = fields.Image("Bathroom");
    dailycharges_ids = fields.One2many('hotel.dailycharges', 'roomtype_id', string='Daily Charges')
    room_ids = fields.One2many('hotel.rooms', 'roomtype_id', string='Rooms')


class dailycharges(models.Model):
    _name = 'hotel.dailycharges'
    _description = 'hotel roomtype daily charges list'

    charge_id = fields.Many2one('hotel.charges', string="Charge Title")
    amount = fields.Float("Daily Amount", digits=(10, 2), options={'always_reload': True})
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Roomtype")
