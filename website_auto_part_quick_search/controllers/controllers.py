# -*- coding: utf-8 -*-

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


class WebsiteSales(WebsiteSale):
    def sitemap_shop(env, rule, qs):
        if not qs or qs.lower() in '/shop':
            yield {'loc': '/shop'}

        Category = env['product.public.category']
        dom = sitemap_qs2dom(qs, '/shop/category', Category._rec_name)
        dom += env['website'].get_current_website().website_domain()
        for cat in Category.search(dom):
            loc = '/shop/category/%s' % slug(cat)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        ############################
        auto_type_id = post.get('type', False)
        auto_brand_id = post.get('brand', False)
        auto_model_id = post.get('model', False)
        auto_variant_id = post.get('variant', False)
        auto_year_id = post.get('year', False)
        ###################################

        keep = QueryURL('/shop', category=category and int(category), search=search, type=auto_type_id,
                        brand=auto_brand_id, model=auto_model_id, variant=auto_variant_id, year=auto_year_id,
                        attrib=attrib_list,
                        order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        search_product = Product.search(domain, order=self._get_search_order(post))
        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search(
                [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset: offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        ###########################################

        all_fields = {'auto_type_id': auto_type_id, 'mfg_brand_id': auto_brand_id, 'model_id': auto_model_id,
                      'model_variant_id': auto_variant_id, 'year_id': auto_year_id}
        domain = []

        for key, value in all_fields.items():
            if value:
                domain.append((key, '=', int(value)))
        filtered_products = []
        if domain:
            vehicles = request.env['auto.vehicle'].search(domain)
            for vehicle_id in vehicles:
                if vehicle_id.part_catalogue_ids:
                    for part_catalogue_id in vehicle_id.part_catalogue_ids:
                        product_ids = part_catalogue_id.part_ids
                        for product_id in product_ids:
                            if product_id.product_tmpl_id.id not in filtered_products:
                                filtered_products.append(product_id.product_tmpl_id.id)

            if filtered_products:
                product_count = len(filtered_products)
                pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7,
                                              url_args=post)
                products = Product.search([('id', 'in', filtered_products)], limit=ppg, offset=pager['offset'],
                                          order=self._get_search_order(post))
            else:
                product_count = len(filtered_products)
                pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7,
                                              url_args=post)
                products = Product.search([('id', 'in', filtered_products)], limit=ppg, offset=pager['offset'],
                                          order=self._get_search_order(post))

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if category:
            values['main_object'] = category

        # Extend ########

        values['type'] = int(auto_type_id) if auto_type_id else False
        values['brand'] = int(auto_brand_id) if auto_brand_id else False
        values['model'] = int(auto_model_id) if auto_model_id else False
        values['variant'] = int(auto_variant_id) if auto_variant_id else False
        values['year'] = int(auto_year_id) if auto_year_id else False

        all_auto_types = request.env['auto.type'].search([])
        all_auto_brands = request.env['auto.mfg.brand'].search([])
        all_auto_models = request.env['auto.model'].search([])
        selected_auto_model = False
        all_auto_variants = False
        if values['model']:
            selected_auto_model = request.env['auto.model'].search([('id', '=', values['model'])])
        if selected_auto_model:
            all_auto_variants = request.env['auto.model.variant'].search(
                [('id', 'in', selected_auto_model.variant_ids.ids)])
        all_auto_years = request.env['auto.built.year'].search([])
        values['all_auto_types'] = all_auto_types
        values['all_auto_brands'] = all_auto_brands
        values['all_auto_models'] = all_auto_models

        values['all_auto_variants'] = all_auto_variants if all_auto_variants else False
        values['all_auto_years'] = all_auto_years
        return request.render("website_sale.products", values)

    def _prepare_product_values(self, product, category, search, **kwargs):
        result = super(WebsiteSales, self)._prepare_product_values(product, category, search, **kwargs)

        attrib_list = request.httprequest.args.getlist('attrib')
        auto_type_id = kwargs.get('type', False)
        auto_brand_id = kwargs.get('brand', False)
        auto_model_id = kwargs.get('model', False)
        auto_variant_id = kwargs.get('variant', False)
        auto_year_id = kwargs.get('year', False)
        ###################################
        keep = QueryURL('/shop', category=result['category'] and result['category'].id, search=search,
                        type=auto_type_id,
                        brand=auto_brand_id, model=auto_model_id, variant=auto_variant_id, year=auto_year_id,
                        attrib=attrib_list)

        result['keep'] = keep
        return result


class AutoPartFilter(http.Controller):
    @http.route('/filter', type='json', auth="public", website=True)
    def filter_out(self, **kwargs):
        selected_sequence = kwargs.get('selected_sequence')
        type_value = kwargs.get('type_value')
        model_value = kwargs.get('model_value')
        filtered_brands = {}
        variant_dict = {}

        if selected_sequence:
            selected_sequence = int(selected_sequence)
            if selected_sequence == 1:
                brand_ids = request.env['auto.mfg.brand'].search([])
                if type_value:
                    for brand_id in brand_ids:
                        if int(type_value) in brand_id.type_ids.ids:
                            filtered_brands[brand_id.id] = brand_id.name
                else:
                    for brand_id in brand_ids:
                        filtered_brands[brand_id.id] = brand_id.name
            if int(selected_sequence) == 4:
                if model_value:
                    variant_ids = request.env['auto.model'].search([('id', '=', int(model_value))]).variant_ids
                    for variant in variant_ids:
                        variant_dict[variant.id] = variant.name
                else:
                    variant_ids = request.env['auto.model.variant'].search([])
                    for variant in variant_ids:
                        variant_dict[variant.id] = variant.name
        return {
            'filtered_brands': filtered_brands,
            'filtered_variant': variant_dict
        }

    @http.route('/filter_model', type='json', auth="public", website=True)
    def filter_model(self, **kwargs):
        type_value = kwargs.get('type_value')
        brand_value = kwargs.get('brand_value')
        model_name = kwargs.get('model_name')

        if type_value and brand_value:
            model_ids = request.env['auto.model'].search([('type_id', '=', int(type_value)),
                                                          ('mfg_brand_id', '=', int(brand_value)),
                                                          ('name', 'ilike', model_name[0])], limit=50)
        elif type_value:
            model_ids = request.env['auto.model'].search([('type_id', '=', int(type_value)),
                                                          ('name', 'ilike', model_name[0])], limit=50)
        elif brand_value:
            model_ids = request.env['auto.model'].search([('mfg_brand_id', '=', int(brand_value)),
                                                          ('name', 'ilike', model_name[0])], limit=50)
        else:
            model_ids = request.env['auto.model'].search([('name', 'ilike', model_name[0])], limit=50)
        model_list = []
        for model_id in model_ids:
            model_list.append([model_id.id, model_id.name])
        return model_list
