odoo.define('auto_part', function (require) {
    'use strict';
    var ajax = require('web.ajax');

    $(function () {
        function format(brand) {
            var img = $('<img class="brand_logo" style="width: 30px;">');
            img.attr('src', "/web/image/auto.mfg.brand/" + brand.id + "/brand_logo");
            if (!brand.id) return brand.text;
            return $('<div>').append(img.clone()).html() + brand.text;
        }

        function format_auto_type(type) {
            var img = $('<img class="type_illustration" style="width: 30px;">');
            img.attr('src', "/web/image/auto.type/" + type.id + "/illustration_image");
            if (!type.id) return type.text;
            return $('<div>').append(img.clone()).html() + type.text;
        }

        function setMany2OneField($select, data = false) {
            var select2Options = {
                data: [{ id: 5, text: 'bug' }],
                allowClear: true,
                minimumInputLength: 1,
                formatResult: function (record, resultElem, searchObj) { return $("<span/>", { text: record.name }); },
                formatSelection: function (record) { return $("<span/>", { text: record.name }).html(); },

                ajax: {
                    data: function (term, page) {
                        return { 'term': term, 'page': page };
                    },
                    transport: function (args) {
                        ajax.rpc('/filter_model', {
                            type_value: $('#auto_detail_1').val(),
                            brand_value: $('#auto_detail_2').val(),
                            year_value: $('#auto_detail_3').val(),
                            model_name: [args.data.term],
                        }).then(args.success);
                    },
                    results: function (data) {
                        var last_page = data.length !== 30
                        var new_data = [];
                        _.each(data, function (record) {
                            new_data.push({ 'id': record[0], 'name': record[1] })
                        });
                        return { 'results': new_data, 'more': !last_page };
                    },
                    quietMillis: 300,
                },
                initSelection: function (element, callback) {
                    if ($(element).data('default_id_vals')) {
                        var new_id_vals = $(element).data('default_id_vals');
                        var new_model_vals = $(element).data('default_model_vals');
                        data = []
                        data.push({ id: new_id_vals, name: new_model_vals });
                        callback(data);
                    }
                }
            };

            $select.select2('destroy');
            $select.addClass('form-control');
            $select.select2(select2Options);
            $select.off('change').on('change', function (e) {
                if (e.added) {
                    $(this).data('new_id_vals', $(this).data('new_id_vals') || {});
                    $(this).data('new_id_vals')[e.added.id] = e.added.name;
                    $(e.target).attr('title', e.added.name)
                } else if (e.removed) {
                    delete $(this).data('new_id_vals')[e.removed.id];
                    $(e.target).attr('title', '')
                }
            });
            setTimeout(function () {
                if ($select.data('select2')) {
                    $select.data('select2').clearSearch();
                }
            });
        }

        setMany2OneField($(".abcd"))

        $("#auto_detail_1").select2(
            {
                formatResult: format_auto_type,
                formatSelection: format_auto_type,
            }
        );
        $("#auto_detail_2").select2({
            formatResult: format,
            formatSelection: format,
        });
        $("#auto_detail_3").select2();
        $("#auto_detail_5").select2();
        var selected = $(".select2-choice").css('font-weight', 'bold')
        for (var i = 0; i < selected.length; i++) {
            var text = $(selected[i]).find(".select2-chosen").text()
            var lite = ['Type...', 'Manufacturer...', 'Year...', 'Model...', 'Variant...']
            if (lite.includes(text)) {
                $(selected[i]).css('font-weight', 'normal')
            }
        }

        $($(".select2-choice")[3]).css('min-height', '39px')
        var model_name = $(".model_name_store").val()
        if (model_name) {
            setTimeout(function () {
                $($(".select2-choice")[3]).find('.select2-chosen').text(model_name)
            });
        }
        $(".auto_detail").on("change", function () {
            var sequence = parseInt($(this).data('sequence'))
            for (var i = sequence; i < 5; i++) {
                $('#auto_detail_' + (i + 1)).val('')
            }

            var selected_sequence = sequence
            ajax.jsonRpc('/filter', 'call', {
                'selected_sequence': selected_sequence,
                'type_value': $('#auto_detail_1').val(),
                'brand_value': $('#auto_detail_2').val(),
                'year_value': $('#auto_detail_3').val(),
                'model_value': $('#auto_detail_4').val(),
                'variant_value': $('#auto_detail_5').val()
            })
                .then(function (data) {
                    for (var i = selected_sequence; i < 5; i++) {
                        $('#auto_detail_' + (i + 1)).select2("val", "");
                    }
                    if (selected_sequence == 1) {
                        var filtered_brands = data['filtered_brands']
                        $('#auto_detail_2').prop('selectedIndex', 0);
                        if (filtered_brands) {
                            $("#auto_detail_2").empty()
                            var brand_JSON = JSON.parse(JSON.stringify(filtered_brands))
                            $("#auto_detail_2").append('<option value="">Manufacturer...</option>');
                            for (var key in brand_JSON) {
                                $("#auto_detail_2").append('<option value="' + key + '">' + brand_JSON[key] + '</option>');
                            }
                        }
                    }

                    if (selected_sequence == 4) {
                        var variant_dict = data['filtered_variant']
                        if (variant_dict) {
                            $("#auto_detail_5").empty()
                            var variant_JSON = JSON.parse(JSON.stringify(variant_dict))
                            $("#auto_detail_5").append('<option value="">Variant...</option>');

                            for (var key in variant_JSON) {
                                $("#auto_detail_5").append('<option value="' + key + '">' + variant_JSON[key] + '</option>');
                            }
                        }
                    }
                });

            var selected = $(".select2-choice").css('font-weight', 'bold')
            for (var i = 0; i < selected.length; i++) {
                var text = $(selected[i]).find(".select2-chosen").text()
                var lite = ['Type...', 'Manufacturer...', 'Year...', 'Model...', 'Variant...']
                if (lite.includes(text)) {
                    $(selected[i]).css('font-weight', 'normal')
                }
            }
        });
    });
});