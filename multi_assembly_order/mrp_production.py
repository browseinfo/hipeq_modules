from openerp.osv import fields, osv, orm
import time
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import tools, SUPERUSER_ID
from openerp.addons.product import _common
from openerp import netsvc


class mrp_production(osv.osv):
    _inherit = 'mrp.production'
    
    _columns = {
        'product_ids': fields.many2many('product.product','mrp_product_rel', 'mrp_id', 'product_id',string='Product', required=True),
        'bom_ids': fields.many2many('mrp.bom','mrp_bom_rel', 'mrp_id', 'bom_id',string='Bill of Material'),
        
    }
    

    def product_id_change_extend(self, cr, uid, ids, product_ids, product_qty=0, context=None):
        """ Finds UoM of changed product.
        @param product_id: Id of changed product.
        @return: Dictionary of values.
        """
        product_ids = product_ids[0][2]
        result = {}
        if not product_ids:
            return {'value': {
                'product_uom': False,
                'bom_ids': [],
                'bom_id' : False,
                'routing_id': False,
                'product_uos_qty': 0,
                'product_uos': False
            }}
        bom_list = []
        bom_obj = self.pool.get('mrp.bom')
        for product in self.pool.get('product.product').browse(cr, uid, product_ids, context=context):
            bom_list.append(bom_obj._bom_find(cr, uid, product_id=product.id, properties=[], context=context))
        routing_id = False
        if bom_list:
            for bom_point in bom_obj.browse(cr, uid, bom_list, context=context):
                routing_id = bom_point.routing_id.id or False
        product_uom_id = product.uom_id and product.uom_id.id or False

        result['value'] = {'product_uos_qty': 0, 'product_uos': False, 'product_uom': product_uom_id, 'bom_ids': [(6,0,bom_list)], 'routing_id': routing_id}
        if product.uos_id.id:
            result['value']['product_uos_qty'] = product_qty * product.uos_coeff
            result['value']['product_uos'] = product.uos_id.id
        return result
    
    def bom_id_change_extend(self, cr, uid, ids, bom_ids, context=None):
        """ Finds routing for changed BoM.
        @param product: Id of product.
        @return: Dictionary of values.
        """
        result = {}
        bom_ids = bom_ids[0][2]
        if not bom_ids:
            return {'value': {
                'routing_id': False
            }}
        for bom_point in self.pool.get('mrp.bom').browse(cr, uid, bom_ids, context=context):
            routing_id = bom_point.routing_id.id or False
            result = {
                'routing_id': routing_id
            }
        return {'value': result}
    
