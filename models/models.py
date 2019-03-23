# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
import datetime

from odoo.exceptions import ValidationError

class hoteltrivago(models.Model):
     _name = 'hoteltrivago.hoteltrivago'

     name = fields.Char()
     value = fields.Integer()
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()

     @api.depends('value')
     def _value_pc(self):
         self.value2 = float(self.value) / 100

class cities(models.Model):
     _name = 'hoteltrivago.cities'
     name = fields.Char()
     description = fields.Text()
     location = fields.Char()
     country = fields.Many2one('res.country')
     hotels = fields.One2many('hoteltrivago.hotels','city')

class clients(models.Model):
     _name='res.partner'
     _inherit = 'res.partner'
     comments = fields.One2many('hoteltrivago.comments','client')
     reservas = fields.One2many('hoteltrivago.reservas', 'client')
     ventasPendientes = fields.One2many('hoteltrivago.reservas',compute="_calc_pendientes")
     pendienteVenta = fields.Boolean(compute="_calc_bool_pendiente",default=False)
     
     @api.depends('reservas')
     @api.multi
     def _calc_pendientes(self):
       for record in self:
         if len(record.reservas) > 0:
           ventasPendientes = record.reservas.filtered(lambda r: len(r.sales) > 0)

     @api.depends('ventasPendientes')
     @api.multi
     def _calc_bool_pendiente(self):
       for record in self:
         if len(record.ventasPendientes) > 0:
           record.pendienteVenta = True
         else:
           record.pendienteVenta = False


class hotels(models.Model):
     _name = 'hoteltrivago.hotels'
     name = fields.Char()
     description = fields.Char()
     stars = fields.Selection([('1','⭐'),('2','⭐⭐'),('3','⭐⭐⭐'),('4','⭐⭐⭐⭐'),('5','⭐⭐⭐⭐⭐')],default='3')
     gallery = fields.Many2many('hoteltrivago.photos_h')
     foto_principal = fields.Binary(compute='fotoPrincipal',store=True)
     city = fields.Many2one('hoteltrivago.cities')
     country = fields.Char(string='Country',related='city.country.name',store=True,readOnly=True)
     rooms = fields.One2many('hoteltrivago.rooms','hotels')
     services = fields.Many2many('hoteltrivago.services')
     comments = fields.One2many('hoteltrivago.comments','hotels')
     avgRatings = fields.Selection([('1','⭐'),('2','⭐⭐'),('3','⭐⭐⭐'),('4','⭐⭐⭐⭐'),('5','⭐⭐⭐⭐⭐')],compute='calc_avg',store=True, default='1')
     reservas = fields.One2many('hoteltrivago.reservas', 'hotels')
     reservasPasadas = fields.One2many('hoteltrivago.reservas', 'hotels' ,compute='calc_reservas_pasadas', readOnly=True)
     reservasActuales = fields.One2many('hoteltrivago.reservas', 'hotels' ,compute='calc_reservas_presentes', readOnly=True)
     reservasFuturas = fields.One2many('hoteltrivago.reservas', 'hotels' ,compute='calc_reservas_futuras', readOnly=True)

     @api.one
     @api.depends('reservas')
     def calc_reservas_pasadas(self):
       now = datetime.datetime.now()
       if reservas:
        self.reservasPasadas = self.env['hoteltrivago.reservas'].search([('hotels.id', '=', self.id), ('fechaFinal','<',now)])
     
     @api.multi
     def reservar_habitacion(self):
       fechaInicio = self._context.get('fechaInicio')
       fechaFinal = self._context.get('fechaFinal')
       client = self._context.get('client')
       room = self.rooms.search([('stay_in','=','Free'),('hotels.id','=','self.id')])[0].id
       reserva = {'clients': client, 'rooms': room, 'fechaInicio': fechaInicio, 'fechaFinal': fechaFinal}
       self.env['hoteltrivago.reservas'].create(reserva)
       return {'type': 'ir.actions.client', 'tag': 'reload' ,}


     @api.one
     @api.depends('reservas')
     def calc_reservas_futuras(self):
       now = datetime.datetime.now()
       if reservas:
        self.reservasPasadas = self.env['hoteltrivago.reservas'].search([('hotels.id', '=', self.id), ('fechaInicio','>',now)])

     @api.one
     @api.depends('reservas')
     def calc_reservas_presentes(self):
       now = datetime.datetime.now()
       if reservas:
        self.reservasPasadas = self.env['hoteltrivago.reservas'].search([('hotels.id', '=', self.id), ('fechaFinal','>',now), ('fechaInicio','<',now)])

     @api.depends('comments')
     def calc_avg(self):
       for record in self:
         if record.comments:
           aComments = record.comments
           suma = 0
           avg = 0
           div=0
           for comment in aComments:
             suma=int(suma)+int(comment.rating)
             div=div+1
             avg=suma/div
           print(avg)
           record.avgRatings=str(int(avg))
         else:
           print("No ratings in comments!")
           record.avgRatings='1'

     @api.depends('gallery')
     def fotoPrincipal(self):
       for record in self:
         if len(record.gallery) > 0:
           record.foto_principal=record.gallery[0].photo
         else:
           print("No photos!")

class comments(models.Model):
     _name = 'hoteltrivago.comments'
     name = fields.Char()
     client = fields.Many2one("res.partner","Client's name")
     photo_cl = fields.Binary(related='client.image')
     name_cl = fields.Char(related='client.name')
     hotels = fields.Many2one('hoteltrivago.hotels','hotels')
     description = fields.Text(string="Description")
     rating = fields.Selection([('1','⭐'),('2','⭐⭐'),('3','⭐⭐⭐'),('4','⭐⭐⭐⭐'),('5','⭐⭐⭐⭐⭐')],default='3')

class rooms(models.Model):
     _name = 'hoteltrivago.rooms'
     name = fields.Char()
     beds = fields.Integer()
     photos = fields.Many2many('hoteltrivago.photos_r')
     foto_principal = fields.Binary(compute='fotoPrincipalRooms',store=True)
     price = fields.Integer()
     description = fields.Char()
     stay_in = fields.Char(compute='compDisponibility',store=True,readOnly=True)
     hotels = fields.Many2one('hoteltrivago.hotels')
     reservas = fields.One2many('hoteltrivago.reservas','rooms')

     @api.depends('reservas')
     def compDisponibility(self):
       for record in self:
         if(len(record.reservas)>0):
           for reserva in record.reservas:
             if(reserva.fechaFinal < str(datetime.datetime.today())):
               record.stay_in="Free"
             else:
               record.stay_in="Bussy"
         else:
           record.stay_in="Free"

     @api.depends('photos')
     def fotoPrincipalRooms(self):
       for record in self:
         if len(record.photos) > 0:
           record.foto_principal=record.photos[0].photo
         else:
           print("No photos!")

     @api.multi
     def reservar_habitacion(self):
       fechaInicio = self._context.get('fechaInicio')
       fechaFinal = self._context.get('fechaFinal')
       client = self._context.get('client')
       room = self.id
       reserva = {'clients': client, 'rooms': room, 'fechaInicio': fechaInicio, 'fechaFinal': fechaFinal}
       self.env['hoteltrivago.reservas'].create(reserva)
       return {'type': 'ir.actions.client', 'tag': 'reload' ,}

class reservas(models.Model):
     _name = 'hoteltrivago.reservas'
     client = fields.Many2one('res.partner')
     fechaInicio = fields.Date()
     fechaFinal = fields.Date()
     rooms = fields.Many2one('hoteltrivago.rooms')
     hotels = fields.Many2one(related='rooms.hotels',readonly=False, store=True)
     sales = fields.One2many('sale.order.line','reservas')
     estado = fields.Char(compute="_comp_estado",readonly=True,store=True)
     name = fields.Char(compute="_get_nom_reserva",readonly=True)
     numDies = fields.Integer(related="sales.numDies", store=True)
     
     @api.depends('sales')
     def _comp_estado(self):
      for record in self:
       if len(record.sales) > 0:
         record.estado = "Procesado"
       else:
         record.estado = "Pendiente"

     @api.one
     @api.depends('rooms', 'hotels', 'fechaInicio', 'fechaFinal')
     def _get_nom_reserva(self):
       for record in self:
        if record.rooms.name and record.fechaInicio and record.fechaFinal:
         record.name = str(record.rooms.name+" - "+record.fechaInicio+"->"+record.fechaFinal)
       

     @api.constrains('fechaInicio', 'fechaFinal')
     def _comprobar_reserva(self):
       for record in self:
         variable = self.search_count([('id', '!=', record.id),('rooms.id', '=', record.rooms.id),('fechaFinal', '>=', record.fechaInicio), ('fechaInicio','<=', record.fechaFinal)])
         variable2=self.search([('id', '!=', record.id),('rooms.id', '=', record.rooms.id), ('fechaFinal', '>=', record.fechaInicio), ('fechaInicio', '<=', record.fechaFinal)])
         print(variable)
         print(variable2)
         if variable > 0:
           raise ValidationError("Ya hay una reserva que incluye alguno de los días " + self.fechaInicio + " - " + self.fechaFinal + " para la habitación " + self.rooms.name)

     @api.one
     def crear_venta(self):
       producto=self.env.ref('hoteltrivago.product_reserva')
       venta=self.env['sale.order'].create({'partner_id':self.client.id})
       linia_venta={'product_id':producto.id,'order_id':venta.id,'reservas':self.id,'name':self.name,'product_uom_qty':self.numDies,'qty_delivered':1,'qty_invoiced':1,'price_unit':self.rooms.price}
       self.env['sale.order.line'].create(linia_venta)
       

     @api.one
     def crear_ventas_cliente(self):
       reservas=self.client.reservas
       producto=self.env.ref('hoteltrivago.product_reserva')
       venta=self.env['sale.order'].create({'partner_id':self.client.id})
       for r in reservas:
        linia_venta={'product_id':producto.id,'order_id':venta.id,'reservas':self.id,'name':self.name,'product_uom_qty':self.numDies,'qty_delivered':1,'qty_invoiced':1,'price_unit':self.rooms.price}
       self.env['sale.order.line'].create(linia_venta)

class photos_h(models.Model):
     _name = 'hoteltrivago.photos_h'
     name = fields.Char()
     photo = fields.Binary()
     hotels = fields.Many2many('hoteltrivago.hotels')

class services(models.Model):
     _name = 'hoteltrivago.services'
     name = fields.Char()
     icon = fields.Binary()
     hotels = fields.Many2many('hoteltrivago.hotels')

class photos_r(models.Model):
     _name = 'hoteltrivago.photos_r'
     name = fields.Char()
     photo = fields.Binary()
     rooms = fields.Many2many('hoteltrivago.rooms')

class sales(models.Model):
     _name = 'sale.order.line'
     _inherit = 'sale.order.line'
     reservas = fields.Many2one('hoteltrivago.reservas','reservas',store=True)
     nomHabitacio = fields.Char(related='reservas.rooms.name')
     nomHotel = fields.Char(related='reservas.rooms.hotels.name')
     numReserves = fields.Integer(compute='_get_num_reserves', store=True)
     numDies = fields.Integer(compute="_calc_numDies", store=True)

     @api.constrains('reservas')
     def _calc_numDies(self):
       for record in self:
         if record.reservas != None:
           DATETIME_FORMAT = "%Y-%m-%d"
           timedelta = datetime.datetime.strptime(record.reservas.fechaFinal, DATETIME_FORMAT) - datetime.datetime.strptime(record.reservas.fechaInicio, DATETIME_FORMAT)
           record.numDies = timedelta.days + float(timedelta.seconds) / 86400

     @api.multi
     @api.depends('reservas')
     def _get_num_reserves(self):
       for s in self:
         s.numReserves = len(s.reservas)

class reserva_wizard(models.TransientModel):
     _name = 'hoteltrivago.reserva_wizard'
     
     def _default_services(self):
       return self.env['hoteltrivago.services'].search([])

     def _default_hotels(self):
       return self.env['hoteltrivago.hotels'].search([])

     def _default_countries(self):
       return self.env['hoteltrivago.hotels'].search([]).mapped('city').mapped('country').ids
     
     def _default_rooms(self):
       return self.hotels.search([]).mapped('rooms').ids

     clients = fields.Many2one('res.partner')
     cities = fields.Many2one('hoteltrivago.cities')
     countries = fields.Many2many('res.country', default=_default_countries)
     country = fields.Many2one('res.country')
     imagenpais = fields.Binary(related='country.image')
     hotels = fields.Many2many('hoteltrivago.hotels', default=_default_hotels)
     services = fields.Many2many('hoteltrivago.services', default=_default_services)
     min_stars = fields.Selection([('1','⭐'),('2','⭐⭐'),('3','⭐⭐⭐'),('4','⭐⭐⭐⭐'),('5','⭐⭐⭐⭐⭐')],default='1')
     max_stars = fields.Selection([('1','⭐'),('2','⭐⭐'),('3','⭐⭐⭐'),('4','⭐⭐⭐⭐'),('5','⭐⭐⭐⭐⭐')],default='5')
     beds = fields.Selection([('1','Unitaria'),('2','Matrimonio'),('3','Familiar I'),('4','Familiar II'),('5','Grupo')],default='1')
     prices = fields.Integer()
     rooms = fields.Many2many('hoteltrivago.rooms', default=_default_rooms)
     fechaInicio = fields.Date()
     fechaFinal = fields.Date()
     state = fields.Selection([('location', 'Selecciona la localización'),('hotels', 'Selecciona el hotel'),('rooms', 'Selecciona la habitación'),('fin', 'Fin')], default='location')
     
     @api.onchange('city','clients')
     def _oc_city(self):
       if self.cities and self.clients:
         self.aplicar_filtros()
         return {}

     @api.onchange('country')
     def _oc_country(self):
       if self.country:
         self.aplicar_filtros()
         return {}
     
     @api.onchange('beds')
     def _oc_beds(self):
       if self.beds:
         self.aplicar_filtros()
         return {}
     
     @api.onchange('prices')
     def _oc_prices(self):
       if self.prices:
         self.aplicar_filtros()
         return {}
     
     @api.onchange('min_stars')
     def _oc_min_stars(self):
       if self.min_stars:
         self.aplicar_filtros()
         return {}
     
     @api.onchange('max_stars')
     def _oc_max_stars(self):
       if self.max_stars:
         self.aplicar_filtros()
         return {}
     
     #@api.onchange('services')
     #def _oc_services(self):
     #  if self.services:
     #    self.aplicar_filtros()
     #    return {}
     
     def aplicar_filtros(self):
       domains=[]
       if len(self.cities) != 0:
         domains.append(('city.id','=',str(self.cities.id)))

       if len(self.country) != 0:
         domains.append(('city.country.id','=',str(self.country.id)))
       
       if self.beds:
         domains.append(('rooms.beds','=',str(self.beds)))
       
       if self.prices != 0:
         domains.append(('rooms.price','<',self.prices))
       
       if self.min_stars != 0:
         domains.append(('stars','>=',self.min_stars))
       
       if self.max_stars != 0:
         domains.append(('stars','<=',self.max_stars))
       
       print(domains)
       WizHotels = self.env['hoteltrivago.hotels'].search(domains)
       
       if len(self.services) > 0:
         WizHotels = WizHotels.filtered(lambda r:len(r.services & self.services) == len(self.services))
       self.hotels = WizHotels

       if self.fechaInicio and self.fechaFinal:
         habitacionesLibres = self.rooms.search([('stay_in','=','Free')])
         if self.beds != '0':
           habitacionesLibres=habitacionesLibres.filtered(lambda r:r.beds==self.camas)
         self.hotels=habitacionesLibres.mapped('hotels').sorted(key=lambda r: r.stars, reverse=True).ids
       
         if self.prices != 0:
           habitacionesLibres=habitacionesLibres.filtered(lambda r:r.prices <= self.prices)
         self.rooms = habitacionesLibres
       
       
       
     @api.multi
     def siguiente_paso(self):
       if self.state == "location":
         self.state = "hotels"
         return {"type": "ir.actions.do_nothing", }
       elif self.state == "hotels":
         self.state = "rooms"
         return {"type": "ir.actions.do_nothing", }
       elif self.state == "rooms":
         self.state = "fin"
         return {"type": "ir.actions.do_nothing", }
     
     
     
class select_booking_wizard(models.TransientModel):
     _name='select.wizard'

     def _default_client(self):
       return self.env['res.partner'].browse(self._context.get('active_id'))

     def _default_rp(self):
       return self.env['res.partner'].browse(self._context.get('active_id')).ventasPendientes
     

     client = fields.Many2one('res.partner', default=_default_client)
     reservasPendientes = fields.Many2many('hoteltrivago.reservas', default=_default_rp)
     name = fields.Char(related='reservasPendientes.name')
     fechaInicio = fields.Date(related='reservasPendientes.fechaInicio')
     fechaFinal = fields.Date(related='reservasPendientes.fechaFinal')
     numDies = fields.Integer(related='reservasPendientes.numDies')
     
     @api.multi
     def launch(self):
       producto = self.env.ref('product_reserva')
       idVenta = self.env['sale.order'].create({'partner.id': self.client.id})
       
       for reserva in self.reservasPendientes:
         venta = {'product_id': producto.id, 'order_id': idVenta.id, 'name': reserva.name, 'reservas': reserva.id, 'product_uom_qty': reserva.numDies, 'qty_delivered': 1, 'qty_invoiced': 1, 'price_unit': reserva.rooms.price}
         self.env['sale.order.line'].create(venta)
         self.reservasPendientes = self.reservasPendientes - reserva
       

       return {}

     

