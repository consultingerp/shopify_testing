from odoo import models,fields,api
from .. import shopify
from odoo.addons.shopify_ept.shopify.pyactiveresource.util import xml_to_dict

class res_partner(models.Model):
    _inherit="res.partner"
    
    company_name_ept=fields.Char("Company Of Name")
    shopify_customer_id=fields.Char("Shopify Cutstomer Id")

    @api.multi
    def list_all_customer(self,result):
        sum_of_result=result        
        if not  sum_of_result:            
            return sum_of_result        
        new_result=shopify.Customer().find(limit=250,page=2)        
        page_no=2
        while new_result:            
            page_no += 1            
            sum_of_result=sum_of_result+new_result            
            new_result=shopify.Customer().find(limit=250,page=page_no)
        return sum_of_result
       
    @api.model    
    def import_shopify_customers(self,instance=False):
        instances=[]
        instances.append(instance)
        sale_order_obj=self.env['sale.order']        
        for instance in instances:
            instance.connect_in_shopify()
            try:
                customer_ids = shopify.Customer().search(limit=250)
            except Exception as e:
                raise Warning(e)
            if len(customer_ids)>=50:
                customer_ids=self.list_all_customer(customer_ids)
            for customer_id in customer_ids:
                result=xml_to_dict(customer_id.to_xml())
                partner=result.get('customer',{}) and sale_order_obj.create_or_update_customer(result.get('customer',{}),True,False,False,instance) or False
        return True     
                 