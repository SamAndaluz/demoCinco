odoo.define('sparepart_extension', function(require){
    var models = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const db = require('point_of_sale.DB');
    const { useListener } = require('web.custom_hooks');

    const ProductsWidgetControlPanel = require('point_of_sale.ProductsWidgetControlPanel');
    const ProductsWidget = require('point_of_sale.ProductsWidget');

    models.load_fields("product.product","vehical_detail");
    
    const ProductsWidget2 = (ProductsWidget) => 
        class extends ProductsWidget { 
            constructor() {
                super(...arguments);
                this.search1 = '';
                this.search2 = '';
                this.search3 = '';
                this.search4 = '';
                useListener('update-auto-parts', this._autoPartSearch);
            }
            perform_search2(searchbox1,searchbox2,searchbox3,searchbox4){
                var products;
                var product_list = [];
                var query = '123'
                if(query){
                    var newpro1 = [];
                    products = this.env.pos.db.get_product_by_category(this.selectedCategoryId);
                    if(searchbox1 != ''){
                        _.each(products, function(product){
                            var vehical_detail = JSON.parse(product['vehical_detail']);
                            var temp = false;
                            _.each(vehical_detail.md, function(model){
                                var model_n = model.toLowerCase();
                                if(model_n.indexOf(searchbox1.toLowerCase()) >= 0){
                                    temp = true;
                                }
                            });
                            if(temp){
                                newpro1.push(product)
                            }
                        });
                    }
                    else{
                        newpro1 = products;
                    }
                    var newpro2 = [];
                    if(searchbox2 != ''){
                        _.each(newpro1, function(product){
                            var vehical_detail = JSON.parse(product['vehical_detail']);
                            var temp = false;
                            _.each(vehical_detail.mf, function(manif){
                                var manif_n = manif.toLowerCase();
                                if(manif_n.indexOf(searchbox2.toLowerCase()) >= 0){
                                    temp = true;
                                }
                            });
                            if(temp){
                                newpro2.push(product)
                            }
                        });
                    }
                    else{
                        newpro2 = newpro1;
                    }
                    var newpro3 = [];
                    if(searchbox3 != ''){
                        _.each(newpro2, function(product){
                            var vehical_detail = JSON.parse(product['vehical_detail']);
                            var temp = false;
                            _.each(vehical_detail.my, function(manify){
                                var manify_n = manify.toLowerCase();
                                if(manify_n.indexOf(searchbox3.toLowerCase()) >= 0){
                                    temp = true;
                                }
                            });
                            if(temp){
                                newpro3.push(product)
                            }
                        });
                    }
                    else{
                        newpro3 = newpro2;
                    }
                    var newpro4 = [];
                    if(searchbox4 != ''){
                        _.each(newpro3, function(product){
                            var vehical_detail = JSON.parse(product['vehical_detail']);
                            var temp = false;
                            _.each(vehical_detail.mv, function(num_e){
                                var eng_num = num_e.toLowerCase();
                                if(eng_num.indexOf(searchbox4.toLowerCase()) >= 0){
                                    temp = true;
                                }
                            });
                            if(temp){
                                newpro4.push(product)
                            }
                        });
                    }
                    else{
                        newpro4 = newpro3;
                    }
                    products = newpro4
                    return products;

                }else{
                    products = this.env.pos.db.get_product_by_category(this.selectedCategoryId);
                    return products;
                }
            }
            _autoPartSearch(event){
                var auto = event.detail;
                this.search1 = auto[0];
                this.search2 = auto[1];
                this.search3 = auto[2];
                this.search4 = auto[3];
                this.render();
            }
            get productsToDisplay() {
                console.log("Testing>>>>>>Search>>22>>>>>>",this.search1,this.search2,this.search3,this.search4);

                if(this.search1 != '' || this.search2 != '' || this.search3 != '' || this.search4 != ''){

                    var products = this.perform_search2(this.search1,this.search2,this.search3,this.search4);
                    this.search1 = '';
                    this.search2 = '';
                    this.search3 = '';
                    this.search4 = '';
                    return products;
                }
                if (this.searchWord !== '') {
                    return this.env.pos.db.search_product_in_category(
                        this.selectedCategoryId,
                        this.searchWord
                    );
                } else {
                    return this.env.pos.db.get_product_by_category(this.selectedCategoryId);
                }
            }
        }
    
    Registries.Component.extend(ProductsWidget, ProductsWidget2);
           

    const ProductsWidgetControlPanel2 = (ProductsWidgetControlPanel) => 
        class extends ProductsWidgetControlPanel {
            get selectedCategoryId() {
                return this.env.pos.get('selectedCategoryId');
            }
            updatePartnerSearch(event) {
                var searchbox2 = $(".em_manufacturer").val();
                var searchbox1 = $(".em_model").val();
                var searchbox3 = $(".em_manufacturer_year").val();
                var searchbox4 = $(".em_variant").val();
                this.trigger('update-auto-parts', [searchbox1,searchbox2,searchbox3,searchbox4]);
            }
            clearSearch1(){
                $(".em_manufacturer").val('');
                var searchbox2 = $(".em_manufacturer").val();
                var searchbox1 = $(".em_model").val();
                var searchbox3 = $(".em_manufacturer_year").val();
                var searchbox4 = $(".em_variant").val();
                this.trigger('update-auto-parts', [searchbox1,searchbox2,searchbox3,searchbox4]);
            }
            clearSearch2(){
                $(".em_manufacturer_year").val('');
                var searchbox2 = $(".em_manufacturer").val();
                var searchbox1 = $(".em_model").val();
                var searchbox3 = $(".em_manufacturer_year").val();
                var searchbox4 = $(".em_variant").val();
                this.trigger('update-auto-parts', [searchbox1,searchbox2,searchbox3,searchbox4]);
            }
            clearSearch3(){
                $(".em_model").val('');
                var searchbox2 = $(".em_manufacturer").val();
                var searchbox1 = $(".em_model").val();
                var searchbox3 = $(".em_manufacturer_year").val();
                var searchbox4 = $(".em_variant").val();
                this.trigger('update-auto-parts', [searchbox1,searchbox2,searchbox3,searchbox4]);
            }
            clearSearch4(){
                $(".em_variant").val('');
                var searchbox2 = $(".em_manufacturer").val();
                var searchbox1 = $(".em_model").val();
                var searchbox3 = $(".em_manufacturer_year").val();
                var searchbox4 = $(".em_variant").val();
                this.trigger('update-auto-parts', [searchbox1,searchbox2,searchbox3,searchbox4]);
            }
        }
    

    Registries.Component.extend(ProductsWidgetControlPanel, ProductsWidgetControlPanel2);
           
});
