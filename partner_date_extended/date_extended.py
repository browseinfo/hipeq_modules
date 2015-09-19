# -*- coding: utf-8 -*-
##############################################################################
#
#    Sales and Account Invoice Discount Management
#    Copyright (C) 2013-2014 BrowseInfo(<http://www.browseinfo.in>).
#    $autor:
#   
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, date
from openerp.osv import osv, fields
from openerp.addons.base.res.res_partner import format_address
from openerp import tools, api
from openerp.tools.translate import _

class res_partner(osv.Model, format_address):
    _inherit="res.partner"
    
    @api.multi    
    def write(self, vals):
        today_date = datetime.now()
        vals.update({'date_ext':today_date}) 
        return super(res_partner, self).write(vals)

    @api.model
    def create(self, vals):
        if not vals.get('date_ext'):
            today_date = datetime.now()
            vals['date_ext'] = today_date
        return super(res_partner, self).create(vals)


    _columns={
        'date_ext':fields.date("Modified Date"),
        }
    _order = "date_ext"

class crm_lead(format_address, osv.osv):
    _inherit="crm.lead"

    def write(self, cr, uid, ids, vals, context=None):
        today_date = datetime.now()
        vals.update({'date_ext':today_date})        
        return super(crm_lead, self).write(cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context=None):
        if not vals.get('date_ext'):
            today_date = datetime.now()
            vals['date_ext'] = today_date
        return super(crm_lead, self).create(cr, uid, vals, context=context)

    _columns={
        'date_ext':fields.date("Modified Date"),
    }
    _order = "date_ext desc"    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
