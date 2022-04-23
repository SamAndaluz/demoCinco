# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
import json

class pos_config(models.Model):
    _inherit = 'pos.config' 
    
    allow_auto_parts = fields.Boolean(string="Allow Auto Parts", default=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    part_catalogue_line = fields.Many2many('part.catalogue.line',"part_catalogue_line_product","product_id","part_catalogue_line_id",string="Part")
    vehical_detail = fields.Text('vehical detail',compute='wv_vehical_detail')

    def wv_vehical_detail(self):
        for res in self:
            v_detail = []
            manufacturer = []
            model = []
            model_year = []
            model_variant = []
            for part_cat_line_id in res.part_catalogue_line:
            	manufacturer.append(part_cat_line_id.vehicle_id.mfg_brand_id.name)
            	model.append(part_cat_line_id.vehicle_id.model_id.name)
            	model_year.append(part_cat_line_id.vehicle_id.year_id.year)
            	model_variant.append(part_cat_line_id.vehicle_id.model_variant_id.name)

            res.vehical_detail = json.dumps({'mf':manufacturer,'md':model,'my':model_year,'mv':model_variant})

