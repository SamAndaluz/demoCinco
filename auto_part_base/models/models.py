# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AutoBrand(models.Model):
    _name = "auto.mfg.brand"
    _description = "Auto Brand"
    _order = 'name'

    brand_logo = fields.Image()
    name = fields.Char()
    type_ids = fields.Many2many('auto.type', string='Manufactured Vehicle Type')


class BuiltYear(models.Model):
    _name = "auto.built.year"
    _description = "Automobile Built Year"
    _rec_name = "year"
    _order = 'year'

    year = fields.Char()


class AutoType(models.Model):
    _name = "auto.type"
    _description = "Automobile Type"

    name = fields.Char()
    illustration_image = fields.Image()


class AutoModelVariant(models.Model):
    _name = "auto.model.variant"
    _description = "Automobile Model Variant"
    _order = 'name'

    name = fields.Char()


class AutoModel(models.Model):
    _name = "auto.model"
    _description = "Automobile Model"
    _order = 'name'

    name = fields.Char()
    mfg_brand_id = fields.Many2one('auto.mfg.brand', string='Brand')
    type_ids = fields.Many2many('auto.type', related='mfg_brand_id.type_ids')
    variant_ids = fields.Many2many('auto.model.variant', string='Variants')
    type_id = fields.Many2one('auto.type')


class Vehicle(models.Model):
    _name = "auto.vehicle"
    _description = "Vehicle"

    name = fields.Char()
    mfg_brand_id = fields.Many2one('auto.mfg.brand', string='Brand/Manufacturer')
    model_id = fields.Many2one('auto.model')
    valid_variants = fields.Many2many('auto.model.variant', compute='set_valid_variant')
    model_variant_id = fields.Many2one('auto.model.variant')
    year_id = fields.Many2one("auto.built.year")
    auto_type_id = fields.Many2one("auto.type", related='model_id.type_id', string='Vehicle Type')
    vehicle_image = fields.Image()

    part_catalogue_ids = fields.One2many("part.catalogue.line", 'vehicle_id')

    @api.onchange('model_id')
    def model_change(self):
        if self.model_id:

            res = {
                'domain': {'model_variant_id': [('id', 'in', self.model_id.variant_ids.ids)]},
            }
            return res

    def set_valid_variant(self):
        for rec in self:
            if rec.model_id:
                rec.valid_variants = [(6, 0, rec.model_id.variant_ids.ids)]
            else:
                rec.valid_variants = []


class PartCatalogueLine(models.Model):
    _name = "part.catalogue.line"

    name = fields.Char()
    catalogue_image = fields.Image()
    vehicle_id = fields.Many2one('auto.vehicle')
    part_ids = fields.Many2many('product.product',"part_catalogue_line_product","part_catalogue_line_id","product_id",string="Part")
    

