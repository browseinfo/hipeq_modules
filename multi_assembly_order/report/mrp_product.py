from openerp.report import report_sxw
from openerp.osv import osv
from datetime import time,date,datetime

class mrp_production_report(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context=None):
        super(mrp_production_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time' : time,
                                  'get_uniq_id': self.get_uniq_id
                                  })
                                  
    def get_uniq_id(self,object):
        pro_obj = self.pool.get('product.product')
        bom_obj = self.pool.get('mrp.bom')
        uom_obj = self.pool.get('product.uom')
        move_qty_dict = {}
        move_cmp_dict = {}
        obj_list = []
        res_list = []
        context = {}
        properties = []
        obj_list.extend(object)
        for rec in obj_list:
            for bom in rec.bom_ids:
                bom_point = bom
                bom_id = bom.id
                for product in rec.product_ids:
                    if not bom_point:
                        bom_id = bom_obj._bom_find(self.cr, self.uid, product.id, rec.product_uom.id, properties)
                        if bom_id:
                            bom_point = bom_obj.browse(self.cr, self.uid, bom_id)
                            routing_id = bom_point.routing_id.id or False
                if not bom_id:
                    raise osv.except_osv(_('Error!'), _("Cannot find a bill of material for this product."))
                factor = uom_obj._compute_qty(self.cr, self.uid, rec.product_uom.id, rec.product_qty, bom_point.product_uom.id)
                res = bom_obj._bom_explode(self.cr, self.uid, bom_point, factor , bom_point.product_qty, properties, routing_id=rec.routing_id.id)
                results = res[0]
                results2 = res[1]
                for i in results:
                    if i['product_id'] in move_qty_dict.keys():
                        move_qty_dict[i['product_id']] = move_qty_dict[i['product_id']] + i['product_qty']
                    else:
                        move_qty_dict[i['product_id']] = i['product_qty']

        for move in rec.move_lines:
            if move.product_id.bom_ids:
                for bom in move.product_id.bom_ids:
                    bom_point = bom
                    bom_id = bom.id
            
                if not bom_point:
                    bom_id = bom_obj._bom_find(self.cr, self.uid, move.product.id, move.product_uom.id, properties)
                    if bom_id:
                        bom_point = bom_obj.browse(self.cr, self.uid, bom_id)
                        routing_id = bom_point.routing_id.id or False
                if not bom_id:
                    raise osv.except_osv(_('Error!'), _("Cannot find a bill of material for this product."))
                factor = uom_obj._compute_qty(self.cr, self.uid, move.product_uom.id, move.product_qty, bom_point.product_uom.id)
                ress = bom_obj._bom_explode(self.cr, self.uid, bom_point, factor / bom_point.product_qty, properties, routing_id=rec.routing_id.id)
                resultss = ress[0]
                resultss2 = ress[1]
                for x in resultss:
                    x['product_qty'] = x['product_qty']
                for i in resultss:
                    if i['product_id'] in move_qty_dict.keys():
                        move_cmp_dict[i['product_id']] = move_qty_dict[i['product_id']] + i['product_qty']
                    else:
                        move_cmp_dict[i['product_id']] = i['product_qty']

        pro_dict = dict(move_qty_dict)
        pro_dict.update(move_cmp_dict)
        prod_ids = pro_dict.keys()
        pro_ids = pro_obj.search(self.cr,self.uid, [('id','in', prod_ids)])
        
        
        for pro in pro_obj.browse(self.cr,self.uid, pro_ids):
            sup = ''
            code = ''
            uom = pro.uom_id.name
            qty = pro_dict[pro.id]
            supplier = pro.seller_ids
            name = ''
            for x in supplier:
                sup = x.name.name
            codeing = pro.seller_ids
            for co in codeing:
                code = co.product_code
            avail = pro.qty_available
            if avail > qty:
                shortage = 0.0
            else:
                shortage = avail - qty
            res = {}
            res.update({'name' :  pro.name or ' '})
            res.update({'product_qty' : qty})
            res.update({'description' :  pro.description})
            res.update({'qty_available' :  pro.qty_available})
            res.update({'standard_price' :  pro.standard_price })
            res.update({'seller' :  sup or '' })
            res.update({'product_code' :  code or '' })
            res.update({'shortage' : shortage})
            res.update({'uom_id': uom})
            res_list.append(res)
        return res_list
                                  
                                  
        
class mrp_production_report_template_id(osv.AbstractModel):
    _name='report.multi_assembly_order.mrp_production_report_template_id'
    _inherit='report.abstract_report'
    _template='multi_assembly_order.mrp_production_report_template_id'
    _wrapped_report_class=mrp_production_report
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
