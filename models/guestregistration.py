# guestregistration.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GuestRegistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'Hotel Guest Registration'

    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")
    
    roomname = fields.Char("Room No.", related='room_id.name')
    
    roomtname = fields.Char("Room Type", related='room_id.roomtypename')
    
    guestname = fields.Char("Guest Name", related='guest_id.name')
    
    datecreated = fields.Date("Date Created", default=lambda self: fields.Date.today())
    datefromSched = fields.Date("Scheduled Check In")
    datetoSched = fields.Date("Scheduled Check Out")
    datefromAct = fields.Date("Actual Check In")
    datetoAct = fields.Date("Actual Check Out")

    state = fields.Selection([
        ('DRAFT', 'Draft'),
        ('RESERVED', 'Reserved'),
        ('CHECKEDIN', 'Checked In'),
        ('CHECKEDOUT', 'Checked Out'),
        ('CANCELLED', 'Cancelled')
    ], string="Status", default="DRAFT")

    name = fields.Char("Guest Registration", compute='_compute_name', store=False)
    @api.depends('room_id', 'guest_id')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.roomname}, {rec.guestname}"

    def action_reserve(self):
        for rec in self:
            if not(rec.guest_id):  
                raise ValidationError('Please supply a valid guest.')            
           
            elif not(rec.roomname):    
                raise ValidationError('Please supply a valid Room Number.')    
            elif not(rec.datefromSched):    
                raise ValidationError('Please supply a valid Date From Schedule.')          
            elif not(rec.datetoSched):    
                raise ValidationError('Please supply a valid Date To Schedule.')          
            elif (rec.datetoSched<rec.datefromSched):    
                raise ValidationError('Invalid Date Range.')          
            else:
                #get the primary key value of guest registration
                pkid = rec.id
                #call the postgresql function the check for conflicts
                self._cr.execute("select * from public.fncheck_registrationconflict("+str(pkid)+")")
                result = self._cr.fetchall()
                
                #gather the query results
                result_cnt = result[0][0]
                result_msg = result[0][1]
                
                if (result_cnt==0):
                    rec.state= "RESERVED"
                else:
                    raise ValidationError(result_msg)

    def action_checkin(self):
        for rec in self:
            if not(rec.guest_id):  
                raise ValidationError('Please supply a valid guest.')            
            
            elif not(rec.roomname):    
                raise ValidationError('Please supply a valid Room Number.')            
            elif not(rec.datefromSched):    
                raise ValidationError('Please supply a valid Date From Schedule.')          
            elif not(rec.datetoSched):    
                raise ValidationError('Please supply a valid Date To Schedule.')          
            elif (rec.datetoSched<rec.datefromSched):    
                raise ValidationError('Invalid Date Range.')          

            else:
                #get the primary key value of guest registration
                pkid = rec.id
                
                #call the postgresql function the check for conflicts
                self._cr.execute("select * from public.fncheck_registrationconflict("+str(pkid)+")")
                result = self._cr.fetchall()
                
                #gather the query results
                result_cnt = result[0][0]
                result_msg = result[0][1]
                
                if (result_cnt==0):
                    rec.state= "CHECKEDIN"
                else:
                    raise ValidationError(result_msg)

    def action_checkout(self):
       for rec in self:
         if (rec.state=="CHECKEDIN"):  
            rec.state= "CHECKEDOUT"
         else:                     
            raise ValidationError("Guest is not CHECKED IN.") 

    def action_cancel(self):
       for rec in self:
         if (rec.state=="CHECKEDIN"):  
            raise ValidationError("Guest has already CHECKED IN.")           
         else:                     
            rec.state= "CANCELLED"
